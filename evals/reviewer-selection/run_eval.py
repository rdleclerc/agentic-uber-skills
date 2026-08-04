#!/usr/bin/env python3
"""Run four isolated reviewer-selection subject/grader evals."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SUITE_PATH = Path(__file__).with_name("suite.json")
HARNESS_PATH = Path(__file__).resolve()
SUITE_RELATIVE = Path("evals/reviewer-selection/suite.json")
RESULT_DIR_RELATIVE = Path("evals/reviewer-selection/results")
RAW_ARTIFACT_ROOT_RELATIVE = Path(".uberlearn-local/reviewer-selection-v1")
EXPECTED_SUITE_SHA256 = "sha256:9f5bef7e1f96f4a4fa282ffe65c0f7d92f2fabcede7384efff36e3c402705142"
EXPECTED_BASE_SHA256 = "sha256:29ef5d6aea15c18143187c79df4d57e104df1a5b848cdfa427b0275be2e0a914"
EXPECTED_INPUT_MANIFEST_SHA256 = "sha256:8c8cea332c37707db2934899039eaae26c153878e762417c76c9bf299f7dbcf4"
EXPECTED_CASE_IDS = {"generic-cross-model", "required-sol-ultra-unavailable", "explicit-claude-by-name", "gaia-adversarial-review"}
EXPECTED_POLICY_INPUT_PATHS = {
    "AGENTS.md", "references/drift-fingerprints.toml", "uberaccept/SKILL.md", "ubergoal/SKILL.md", "uberplan/SKILL.md",
}
DARWIN_CODEX_REQUIREMENT = '=identifier "codex" and anchor apple generic and certificate leaf[subject.OU] = "2DC432GLL2"'
ALLOWED_ITEMS = {"agent_message", "reasoning"}
DISABLED_FEATURES = (
    "apps", "auth_elicitation", "browser_use", "browser_use_external", "browser_use_full_cdp_access",
    "chronicle", "code_mode_host", "computer_use", "default_mode_request_user_input", "goals", "guardian_approval", "hooks",
    "image_generation", "in_app_browser", "in_app_updates", "memories", "multi_agent", "plugin_sharing", "plugins",
    "remote_plugin", "shell_snapshot", "shell_tool", "skill_mcp_dependency_install", "skill_search", "standalone_web_search",
    "tool_call_mcp_elicitation", "tool_suggest", "unified_exec", "workspace_dependencies",
)


class EvalFailure(RuntimeError):
    def __init__(self, phase: str, reason: str):
        super().__init__(reason)
        self.phase = phase


def packed(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def pretty_json(value: Any) -> bytes:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False).encode() + b"\n"


def sha(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def json_object(data: bytes, label: str) -> dict[str, Any]:
    if not isinstance(value := json.loads(data.decode("utf-8")), dict):
        raise ValueError(f"{label} must contain a JSON object")
    return value


def input_manifest_digest(paths: list[str], snapshots: dict[str, bytes]) -> str:
    entries = [
        {"path": path, "sha256": sha(snapshots[path])}
        for path in sorted(set(paths))
    ]
    return sha(packed(entries))


def load_json(path: Path) -> dict[str, Any]:
    if not isinstance(value := json.loads(path.read_text(encoding="utf-8")), dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def safe_path(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError(f"unsafe or missing input: {relative}")
    return path


class AnchoredDirectory:
    """A real directory held by fd and revalidated against its canonical repo name."""

    def __init__(self, repo: Path, relative: Path, *, create: bool = False):
        self.repo = repo.resolve()
        self.relative = Path(relative)
        self.parts = self.relative.parts
        if not self.parts or self.relative.is_absolute() or any(part in {"", ".", ".."} for part in self.parts):
            raise EvalFailure("preflight", f"invalid canonical directory: {relative}")
        self.root_fd = os.open(self.repo, os.O_RDONLY | os.O_DIRECTORY)
        try:
            self.fd = self._open(create=create)
        except Exception:
            os.close(self.root_fd)
            raise

    def _open(self, *, create: bool) -> int:
        current = os.dup(self.root_fd)
        try:
            for part in self.parts:
                if create:
                    try:
                        os.mkdir(part, dir_fd=current)
                    except FileExistsError:
                        pass
                info = os.stat(part, dir_fd=current, follow_symlinks=False)
                if not stat.S_ISDIR(info.st_mode):
                    raise EvalFailure("preflight", f"canonical directory component is not a real directory: {self.relative}")
                next_fd = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=current)
                os.close(current)
                current = next_fd
            return current
        except Exception:
            os.close(current)
            raise

    def revalidate(self) -> None:
        check = self._open(create=False)
        try:
            expected = os.fstat(self.fd)
            actual = os.fstat(check)
            if (expected.st_dev, expected.st_ino) != (actual.st_dev, actual.st_ino):
                raise EvalFailure("output", f"canonical directory changed during run: {self.relative}")
        finally:
            os.close(check)

    def close(self) -> None:
        os.close(self.fd)
        os.close(self.root_fd)

    def __enter__(self) -> AnchoredDirectory:
        return self

    def __exit__(self, *_args: object) -> None:
        self.close()

    def child(self, name: str) -> AnchoredDirectory:
        if Path(name).name != name:
            raise EvalFailure("output", f"unsafe output directory name: {name}")
        self.revalidate()
        try:
            os.mkdir(name, dir_fd=self.fd)
        except FileExistsError:
            raise EvalFailure("output", f"output directory already exists: {name}")
        return AnchoredDirectory(self.repo, self.relative / name)

    def names(self) -> list[str]:
        self.revalidate()
        return sorted(os.listdir(self.fd))

    def anchored_names(self) -> list[str]:
        """List only the directory held by fd, including after canonical-name drift."""
        return sorted(os.listdir(self.fd))

    def unlink(self, name: str, *, missing_ok: bool = True) -> None:
        if Path(name).name != name:
            raise EvalFailure("output", f"unsafe output filename: {name}")
        self.revalidate()
        try:
            os.unlink(name, dir_fd=self.fd)
        except FileNotFoundError:
            if not missing_ok:
                raise

    def anchored_unlink(self, name: str, *, missing_ok: bool = True) -> None:
        """Remove from only the directory held by fd during failure cleanup."""
        if Path(name).name != name:
            raise EvalFailure("output", f"unsafe output filename: {name}")
        try:
            os.unlink(name, dir_fd=self.fd)
        except FileNotFoundError:
            if not missing_ok:
                raise

    def write_bytes(self, name: str, data: bytes) -> None:
        if Path(name).name != name:
            raise EvalFailure("output", f"unsafe output filename: {name}")
        self.revalidate()
        temp_name = f".{name}.{uuid.uuid4().hex}.tmp"
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
        fd = os.open(temp_name, flags, 0o600, dir_fd=self.fd)
        try:
            with os.fdopen(fd, "wb", closefd=False) as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            self.revalidate()
            os.replace(temp_name, name, src_dir_fd=self.fd, dst_dir_fd=self.fd)
        finally:
            os.close(fd)
            try:
                os.unlink(temp_name, dir_fd=self.fd)
            except FileNotFoundError:
                pass

    def write_json(self, name: str, value: Any) -> None:
        self.write_bytes(name, pretty_json(value))

    def read_bytes(self, name: str) -> bytes:
        if Path(name).name != name:
            raise EvalFailure("output", f"unsafe output filename: {name}")
        self.revalidate()
        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=self.fd)
        try:
            with os.fdopen(fd, "rb", closefd=False) as stream:
                return stream.read()
        finally:
            os.close(fd)


def snapshot_logical(
    repo: Path, anchor: Path, relative: str, snapshots: dict[str, bytes],
) -> str:
    requested = Path(relative)
    if requested.is_absolute() or any(part in {"", ".", ".."} for part in requested.parts):
        raise ValueError(f"unsafe input path: {relative}")
    lexical = Path(os.path.abspath(anchor / requested))
    if not lexical.is_relative_to(repo):
        raise ValueError(f"input path escapes repository: {relative}")
    logical = str(lexical.relative_to(repo))
    if logical not in snapshots:
        snapshots[logical] = safe_path(anchor, relative).read_bytes()
    return logical


def native_magic(data: bytes) -> bool:
    return data.startswith((b"\x7fELF", b"MZ", b"\xfe\xed\xfa\xce", b"\xfe\xed\xfa\xcf", b"\xce\xfa\xed\xfe", b"\xcf\xfa\xed\xfe"))


def attest_darwin_signature(path: Path) -> None:
    verified = subprocess.run(
        [
            "/usr/bin/codesign", "--verify", "--strict", "--test-requirement",
            DARWIN_CODEX_REQUIREMENT, str(path),
        ],
        capture_output=True, text=True, check=False,
    )
    details = subprocess.run(
        ["/usr/bin/codesign", "-dv", "--verbose=4", str(path)], capture_output=True, text=True, check=False,
    )
    signature = details.stdout + details.stderr
    if (
        verified.returncode
        or "Identifier=codex" not in signature.splitlines()
        or "Authority=Developer ID Application: OpenAI OpCo, LLC (2DC432GLL2)" not in signature
        or "TeamIdentifier=2DC432GLL2" not in signature
    ):
        raise EvalFailure("preflight", "canonical runner lacks the Codex designated code-signing identity")


def file_identity(info: os.stat_result) -> tuple[int, int, int, int, int]:
    return info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, stat.S_IMODE(info.st_mode)


class PreparedRunner:
    """An explicit test fake or a private immutable copy of an attested native runner."""

    def __init__(self, source: Path, source_bytes: bytes, provenance: dict[str, Any], *, test_runner: bool):
        self._temporary: tempfile.TemporaryDirectory[str] | None = None
        self._directory_fd: int | None = None
        if test_runner:
            self.path = source
            self.provenance = provenance
            return
        temporary_root = Path(tempfile.gettempdir()).resolve()
        self._temporary = tempfile.TemporaryDirectory(prefix="uber-eval-verified-codex-", dir=temporary_root)
        directory = Path(self._temporary.name)
        os.chmod(directory, 0o700)
        directory_info = os.lstat(directory)
        if directory != directory.resolve() or not stat.S_ISDIR(directory_info.st_mode) or stat.S_IMODE(directory_info.st_mode) != 0o700:
            raise EvalFailure("preflight", "private runner directory is not a secure real directory")
        self._directory_fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        name = "codex"
        fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o500, dir_fd=self._directory_fd)
        try:
            with os.fdopen(fd, "wb", closefd=False) as stream:
                stream.write(source_bytes)
                stream.flush()
                os.fsync(stream.fileno())
            os.fchmod(fd, 0o500)
        finally:
            os.close(fd)
        self.path = directory / name
        copied_fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=self._directory_fd)
        try:
            copied_info = os.fstat(copied_fd)
            with os.fdopen(copied_fd, "rb", closefd=False) as stream:
                copied_bytes = stream.read()
        finally:
            os.close(copied_fd)
        if not stat.S_ISREG(copied_info.st_mode) or stat.S_IMODE(copied_info.st_mode) != 0o500 or sha(copied_bytes) != sha(source_bytes):
            raise EvalFailure("preflight", "private runner copy failed byte or mode verification")
        attest_darwin_signature(self.path)
        self._copy_identity = file_identity(copied_info)
        self.provenance = {
            **provenance,
            "verified_source_sha256": sha(source_bytes),
            "executed_copy_sha256": sha(copied_bytes),
            "sha256": sha(copied_bytes),
            "execution": "private_secure_immutable_copy",
            "executed_copy_mode": "0500",
            "private_directory_mode": "0700",
            "code_requirement": DARWIN_CODEX_REQUIREMENT,
        }

    def revalidate(self) -> None:
        if self._directory_fd is None:
            if not self.path.is_file() or sha(self.path.read_bytes()) != self.provenance["sha256"]:
                raise EvalFailure("preflight", "test runner changed after preflight")
            return
        info = os.stat("codex", dir_fd=self._directory_fd, follow_symlinks=False)
        if not stat.S_ISREG(info.st_mode) or file_identity(info) != self._copy_identity:
            raise EvalFailure("preflight", "private runner copy changed after verification")

    def close(self) -> None:
        if self._directory_fd is not None:
            os.close(self._directory_fd)
            self._directory_fd = None
        if self._temporary is not None:
            self._temporary.cleanup()
            self._temporary = None


def resolve_runner(codex_bin: str, test_runner: bool) -> PreparedRunner:
    supplied = Path(codex_bin)
    if not supplied.is_absolute():
        raise EvalFailure("preflight", "an explicit absolute Codex executable path is required")
    resolved = supplied.resolve()
    if (not test_runner and supplied != resolved) or not resolved.is_file() or not os.access(resolved, os.X_OK):
        raise EvalFailure("preflight", "runner path must be a resolved executable file")
    if test_runner:
        runner_bytes = resolved.read_bytes()
        provenance = {
            "mode": "test_fake", "path": str(resolved), "sha256": sha(runner_bytes),
            "executed_copy_sha256": sha(runner_bytes),
            "attestation": "explicit_test_only_path",
        }
        return PreparedRunner(resolved, runner_bytes, provenance, test_runner=True)
    if sys.platform != "darwin":
        raise EvalFailure("preflight", "trusted canonical Codex OS attestation is unavailable outside Darwin")
    probe_fd = os.open(resolved, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        probe = os.read(probe_fd, 4)
    finally:
        os.close(probe_fd)
    if resolved.name != "codex" or not native_magic(probe):
        raise EvalFailure("preflight", "canonical runner must be the native Codex executable")
    try:
        package_path = resolved.parents[3] / "package.json"
        package_bytes = package_path.read_bytes()
        package = json_object(package_bytes, str(package_path))
    except (IndexError, OSError, ValueError, json.JSONDecodeError) as exc:
        raise EvalFailure("preflight", "canonical runner lacks OpenAI Codex package provenance") from exc
    repository = package.get("repository")
    if package.get("name") != "@openai/codex" or not isinstance(repository, dict) or repository.get("url") != "git+https://github.com/openai/codex.git":
        raise EvalFailure("preflight", "canonical runner package provenance is not OpenAI Codex")
    before = os.stat(resolved, follow_symlinks=False)
    attest_darwin_signature(resolved)
    runner_fd = os.open(resolved, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        during = os.fstat(runner_fd)
        with os.fdopen(runner_fd, "rb", closefd=False) as stream:
            runner_bytes = stream.read()
    finally:
        os.close(runner_fd)
    attest_darwin_signature(resolved)
    after = os.stat(resolved, follow_symlinks=False)
    if file_identity(before) != file_identity(during) or file_identity(during) != file_identity(after) or not native_magic(runner_bytes[:4]):
        raise EvalFailure("preflight", "canonical runner changed during signature and byte verification")
    provenance = {
        "mode": "canonical_native_codex", "verified_source_path": str(resolved),
        "untrusted_package_metadata": {
            "manifest": str(package_path), "manifest_sha256": sha(package_bytes),
            "version": package.get("version"),
        },
        "attestation": "openai_developer_id_codex_designated_requirement",
    }
    return PreparedRunner(resolved, runner_bytes, provenance, test_runner=False)


def tree_snapshot(root: Path, excluded: set[str] | None = None) -> dict[str, str]:
    excluded = excluded or set()
    result: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if path.is_file() and not any(part in excluded for part in rel.parts):
            result[str(rel)] = sha(path.read_bytes())
    return result


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(pretty_json(value))


def revalidate_input_snapshots(repo: Path, snapshots: dict[str, bytes]) -> None:
    for logical, expected in sorted(snapshots.items()):
        try:
            current = safe_path(repo, logical).read_bytes()
        except (OSError, ValueError) as exc:
            raise EvalFailure("output", f"input became unsafe or unavailable during run: {logical}") from exc
        if current != expected:
            raise EvalFailure("output", f"input changed during run: {logical}")


def copy_subject_bundle(
    case: dict[str, Any], case_bytes: bytes, snapshots: dict[str, bytes], bundle: Path,
) -> tuple[dict[str, bytes], list[dict[str, Any]]]:
    bundle.mkdir(parents=True)
    files: dict[str, bytes] = {}
    copied: list[dict[str, Any]] = []
    for relative in case.get("context_files", []):
        relative = str(Path(str(relative)))
        data = snapshots[relative]
        target = bundle / str(relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        files[relative] = data
        copied.append({"path": relative, "sha256": sha(data)})
    target_case = bundle / "case.json"
    target_case.write_bytes(case_bytes)
    files["case.json"] = case_bytes
    copied.append({"path": "case.json", "sha256": sha(case_bytes)})
    expected = {str(Path(str(item))) for item in case.get("context_files", [])} | {"case.json"}
    if set(tree_snapshot(bundle)) != expected:
        raise ValueError("subject bundle allowlist mismatch")
    return files, copied


def inline_payload(snapshot: dict[str, bytes], phase: str) -> tuple[str, list[dict[str, Any]]]:
    files = []
    bindings = []
    for relative, data in sorted(snapshot.items()):
        files.append({"path": relative, "content": data.decode("utf-8")})
        bindings.append({"path": relative, "sha256": sha(data)})
    payload = {"phase": phase, "context_delivery": "harness_inlined_exact_bytes", "files": files}
    if phase == "subject":
        instructions = (
            "Return one JSON object only with keys case_id, decision, authorized_route, selected_model, selected_effort, attempted_model_route, invocation_attempted, approval_or_stop, reason, failures. "
            "decision must be stop, authorize, or select; approval_or_stop must be stopped, authorized_not_invoked, or approved_not_invoked. Routes/models must be null, claude, or gpt-5.6-sol; effort must be null or ultra. When stopped, route/model/effort must be null. "
            "attempted_model_route must be null and invocation_attempted false; they record actual process attempts. Do not call tools or reviewers."
        )
    else:
        instructions = "Grade only against rubric.json. Return one JSON object only with keys case_id, passed, failures, evidence. Do not call tools or change files."
    return instructions + "\nINPUT_JSON=" + packed(payload).decode(), bindings


def command(codex_bin: str, model: str, effort: str, bundle: Path) -> list[str]:
    disabled = [item for feature in DISABLED_FEATURES for item in ("--disable", feature)]
    return [codex_bin, "exec", "--ephemeral", "--ignore-user-config", "--ignore-rules", "--skip-git-repo-check", *disabled,
            "-m", model, "-c", f'model_reasoning_effort="{effort}"', "-c", 'web_search="disabled"', "--sandbox", "read-only",
            "-C", str(bundle), "--json", "-"]


def parse_trace(raw: bytes, phase: str) -> tuple[dict[str, Any], list[dict[str, Any]], str]:
    if not raw.strip():
        raise EvalFailure(phase, "missing trace")
    events, messages, tool_choices, thread_ids = [], [], [], []
    for number, line in enumerate(raw.splitlines(), 1):
        try:
            event = json.loads(line)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise EvalFailure(phase, f"malformed trace line {number}: {exc}") from exc
        if not isinstance(event, dict):
            raise EvalFailure(phase, f"malformed trace line {number}: not an object")
        events.append(event)
        if event.get("type") == "thread.started" and isinstance(event.get("thread_id"), str):
            thread_ids.append(event["thread_id"])
        item = event.get("item")
        if isinstance(item, dict) and item.get("type"):
            item_type = str(item["type"])
            if item_type == "error":
                raise EvalFailure(phase, "process trace error: " + str(item.get("message", "unknown")))
            if item_type not in ALLOWED_ITEMS:
                tool_choices.append(item_type)
            if event.get("type") == "item.completed" and item_type == "agent_message":
                messages.append(str(item.get("text", "")))
    if tool_choices:
        raise EvalFailure(phase, "tool execution attempted: " + ", ".join(tool_choices))
    if len(thread_ids) != 1 or not thread_ids[0].strip():
        raise EvalFailure(phase, "missing or malformed fresh runtime context id")
    if not messages:
        raise EvalFailure(phase, "missing final agent message")
    try:
        output = json.loads(messages[-1])
    except json.JSONDecodeError as exc:
        raise EvalFailure(phase, f"malformed final output: {exc}") from exc
    if not isinstance(output, dict):
        raise EvalFailure(phase, "malformed final output: not an object")
    return output, events, thread_ids[0]


def validate_output(output: dict[str, Any], case_id: str, phase: str) -> None:
    required = ({"case_id", "passed", "failures", "evidence"} if phase == "grader" else {
        "case_id", "decision", "authorized_route", "selected_model", "selected_effort",
        "attempted_model_route", "invocation_attempted", "approval_or_stop", "reason", "failures",
    })
    missing = sorted(required - output.keys())
    if missing or output.get("case_id") != case_id:
        raise EvalFailure(phase, f"malformed output schema: missing={missing} case_id={output.get('case_id')!r}")
    if not isinstance(output.get("failures"), list):
        raise EvalFailure(phase, "malformed output schema: failures must be a list")
    if phase == "subject":
        if output.get("decision") not in {"stop", "authorize", "select"} or output.get("approval_or_stop") not in {"stopped", "authorized_not_invoked", "approved_not_invoked"}:
            raise EvalFailure(phase, "malformed output schema: invalid decision or approval_or_stop")
        if output.get("authorized_route") not in {None, "claude", "gpt-5.6-sol"} or output.get("selected_model") not in {None, "claude", "gpt-5.6-sol"} or output.get("selected_effort") not in {None, "ultra"}:
            raise EvalFailure(phase, "malformed output schema: invalid route, model, or effort")
        if output.get("decision") == "stop" and any(output.get(key) is not None for key in ("authorized_route", "selected_model", "selected_effort")):
            raise EvalFailure(phase, "malformed output schema: stopped route fields must be null")
        if output.get("attempted_model_route") is not None or output.get("invocation_attempted") is not False:
            raise EvalFailure(phase, "reviewer invocation or model-route attempt is forbidden in this eval")
    elif output.get("passed") is not True or output.get("failures"):
        raise EvalFailure(phase, "hidden-rubric grader rejected subject output: " + repr(output.get("failures")))


def validate_subject_against_rubric(subject: dict[str, Any], rubric: dict[str, Any]) -> None:
    mismatches = [key for key, expected in rubric.get("expected", {}).items() if subject.get(key) != expected]
    if mismatches:
        raise EvalFailure("subject", "subject output disagrees with hidden rubric: " + ", ".join(sorted(mismatches)))


def invoke(
    repo: Path, raw_dir: AnchoredDirectory, bundle: Path, phase: str, case_id: str,
    runner: PreparedRunner, model: str, effort: str, timeout: int, prompt: str, delivered_files: list[str],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, str]]:
    invocation_id = str(uuid.uuid4())
    cmd = command(str(runner.path), model, effort, bundle)
    repo_before = tree_snapshot(repo, {".git", ".uberlearn-local"})
    bundle_before = tree_snapshot(bundle)
    started = time.time()
    timed_out = False
    with tempfile.TemporaryDirectory(prefix="uber-eval-codex-home-") as temp_home:
        auth = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "auth.json"
        if auth.is_file():
            (Path(temp_home) / "auth.json").symlink_to(auth)
        keep = ("PATH", "TMPDIR", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY")
        env = {key: os.environ[key] for key in keep if key in os.environ}
        env.update(CODEX_HOME=temp_home, PYTHONDONTWRITEBYTECODE="1")
        try:
            runner.revalidate()
            proc = subprocess.run(cmd, cwd=bundle, input=prompt, text=True, capture_output=True, timeout=timeout, env=env, check=False)
            stdout, stderr, returncode = proc.stdout.encode(), proc.stderr.encode(), proc.returncode
        except subprocess.TimeoutExpired as exc:
            stdout = (exc.stdout or b"") if isinstance(exc.stdout, bytes) else (exc.stdout or "").encode()
            stderr = (exc.stderr or b"") if isinstance(exc.stderr, bytes) else (exc.stderr or "").encode()
            returncode, timed_out = -1, True
    raw_dir.write_bytes(f"{phase}.stdout.jsonl", stdout)
    raw_dir.write_bytes(f"{phase}.stderr.log", stderr)
    raw_dir.write_bytes(f"{phase}.prompt.sha256", (sha(prompt.encode()) + "\n").encode())
    if tree_snapshot(bundle) != bundle_before:
        raise EvalFailure(phase, "unexpected write in disposable bundle")
    if tree_snapshot(repo, {".git", ".uberlearn-local"}) != repo_before:
        raise EvalFailure(phase, "unexpected repository write")
    if timed_out:
        raise EvalFailure(phase, f"timeout after {timeout}s")
    if returncode:
        raise EvalFailure(phase, f"nonzero exit {returncode}")
    output, events, runtime_thread_id = parse_trace(stdout, phase)
    validate_output(output, case_id, phase)
    trace = {
        "schema_version": 1, "phase": phase, "case_id": case_id,
        "invocation_id": invocation_id, "runtime_thread_id": runtime_thread_id, "model": model, "reasoning_effort": effort,
        "context_delivery": "harness_inlined_exact_bytes", "isolated_codex_home": True,
        "delivered_context_files": sorted(delivered_files), "files_read": [],
        "tool_choices": [], "attempted_model_route": output.get("attempted_model_route"),
        "decision": output.get("decision"), "authorized_route": output.get("authorized_route"),
        "selected_model": output.get("selected_model"), "selected_effort": output.get("selected_effort"),
        "approval_or_stop": output.get("approval_or_stop"), "reported_failures": output.get("failures"), "side_effects": [],
        "event_count": len(events), "raw_trace_sha256": sha(stdout),
        "prompt_sha256": sha(prompt.encode()), "duration_ms": round((time.time() - started) * 1000),
        "command_shape": command("codex", model, effort, Path("$BUNDLE")),
    }
    bindings = {"raw_trace_sha256": sha(stdout), "stderr_sha256": sha(stderr), "trace_sha256": sha(packed(trace))}
    return output, trace, bindings


def run_suite(repo: Path, suite_path: Path, codex_bin: str, model: str, effort: str, test_runner: bool = False) -> dict[str, Any]:
    repo = repo.resolve()
    suite_path = suite_path.resolve()
    suite: dict[str, Any] = {}
    run_id = str(uuid.uuid4())
    outputs_validated = False
    calls = {"subject": 0, "grader": 0}
    receipts: list[dict[str, Any]] = []
    runtime_ids: set[str] = set()
    current_case = current_phase = "preflight"
    published_names: list[str] = []
    results_dir: AnchoredDirectory | None = None
    raw_dir: AnchoredDirectory | None = None
    run_raw_root: AnchoredDirectory | None = None
    runner: PreparedRunner | None = None
    try:
        if suite_path != (repo / SUITE_RELATIVE).resolve():
            raise EvalFailure("preflight", "canonical suite path is required")
        input_bytes_by_logical_path: dict[str, bytes] = {}
        suite_logical = snapshot_logical(repo, repo, str(SUITE_RELATIVE), input_bytes_by_logical_path)
        suite_bytes = input_bytes_by_logical_path[suite_logical]
        suite = json_object(suite_bytes, str(suite_path))
        suite_digest = sha(suite_bytes)
        fixed_bindings = {
            "suite_id": "reviewer-selection-v1",
            "base_manifest": "base.json",
            "model": "gpt-5.6-sol",
            "reasoning_effort": "ultra",
            "raw_artifact_root": str(RAW_ARTIFACT_ROOT_RELATIVE),
            "result_dir": str(RESULT_DIR_RELATIVE),
            "current_evaluation_status": "results/current-eval-status.json",
        }
        mismatched = [key for key, expected in fixed_bindings.items() if suite.get(key) != expected]
        if mismatched:
            raise EvalFailure("preflight", "fixed suite binding mismatch: " + ", ".join(sorted(mismatched)))
        if Path(str(suite["result_dir"])) != RESULT_DIR_RELATIVE:
            raise EvalFailure("preflight", "canonical result path is required")
        if Path(str(suite["raw_artifact_root"])) != RAW_ARTIFACT_ROOT_RELATIVE:
            raise EvalFailure("preflight", "canonical raw artifact path is required")
        results_dir = AnchoredDirectory(repo, RESULT_DIR_RELATIVE)
        outputs_validated = True
        if (model, effort) != (suite.get("model"), suite.get("reasoning_effort")):
            raise EvalFailure("preflight", f"model binding mismatch: requested {model}/{effort}")
        base_logical = snapshot_logical(
            repo, suite_path.parent, str(suite["base_manifest"]), input_bytes_by_logical_path,
        )
        base_bytes = input_bytes_by_logical_path[base_logical]
        base_digest = sha(base_bytes)
        if not test_runner and (suite_digest, base_digest) != (EXPECTED_SUITE_SHA256, EXPECTED_BASE_SHA256):
            raise EvalFailure("preflight", "suite or base manifest digest mismatch")
        case_logical_paths = [
            snapshot_logical(repo, suite_path.parent, str(item), input_bytes_by_logical_path)
            for item in suite.get("cases", [])
        ]
        if not case_logical_paths or len(case_logical_paths) > 4:
            raise EvalFailure("preflight", "suite must contain one to four cases")
        case_objects_by_id: dict[str, dict[str, Any]] = {}
        case_bytes_by_id: dict[str, bytes] = {}
        case_ids: list[str] = []
        for logical in case_logical_paths:
            case_bytes = input_bytes_by_logical_path[logical]
            case = json_object(case_bytes, logical)
            case_id = str(case["case_id"])
            case_ids.append(case_id)
            case_objects_by_id[case_id] = case
            case_bytes_by_id[case_id] = case_bytes
        if len(set(case_ids)) != len(case_ids) or any(Path(case_id).name != case_id for case_id in case_ids):
            raise EvalFailure("preflight", "case ids must be unique safe filenames")
        if not test_runner and set(case_ids) != EXPECTED_CASE_IDS:
            raise EvalFailure("preflight", "canonical suite case set mismatch")
        manifest_logical_paths = [base_logical, suite_logical, *case_logical_paths]
        rubric_bytes_by_case_id: dict[str, bytes] = {}
        rubric_objects_by_case_id: dict[str, dict[str, Any]] = {}
        for case_id in case_ids:
            logical = snapshot_logical(
                repo, suite_path.parent, str(suite["rubrics"][case_id]), input_bytes_by_logical_path,
            )
            rubric_bytes = input_bytes_by_logical_path[logical]
            rubric_bytes_by_case_id[case_id] = rubric_bytes
            rubric_objects_by_case_id[case_id] = json_object(rubric_bytes, logical)
            manifest_logical_paths.append(logical)
        for case_id in case_ids:
            for relative in case_objects_by_id[case_id].get("context_files", []):
                logical = snapshot_logical(repo, repo, str(relative), input_bytes_by_logical_path)
                manifest_logical_paths.append(logical)
        status_logical = snapshot_logical(
            repo, suite_path.parent, str(suite["current_evaluation_status"]), input_bytes_by_logical_path,
        )
        status = json_object(input_bytes_by_logical_path[status_logical], status_logical)
        manifest_logical_paths.append(status_logical)
        if status.get("suite_id") != suite["suite_id"] or set(status.get("skills", {})) != {"uberaccept", "ubergoal", "uberplan"}:
            raise EvalFailure("preflight", "current evaluation status binding mismatch")
        if any(
            item.get("evaluation_state") != "fresh_eval_required" or item.get("promotion_state") != "not_promoted"
            for item in status["skills"].values()
        ):
            raise EvalFailure("preflight", "current evaluation status must remain fresh_eval_required/not_promoted")
        input_digest = input_manifest_digest(manifest_logical_paths, input_bytes_by_logical_path)
        if not test_runner:
            policy_inputs = set(manifest_logical_paths) & EXPECTED_POLICY_INPUT_PATHS
            if policy_inputs != EXPECTED_POLICY_INPUT_PATHS:
                raise EvalFailure("preflight", "canonical policy input set mismatch")
            if input_digest != EXPECTED_INPUT_MANIFEST_SHA256:
                raise EvalFailure("preflight", "case, rubric, or context manifest digest mismatch")
        harness_sha256 = sha(HARNESS_PATH.read_bytes())
        runner = resolve_runner(codex_bin, test_runner)
        runner_provenance = runner.provenance
        raw_dir = AnchoredDirectory(repo, RAW_ARTIFACT_ROOT_RELATIVE, create=True)
        for stale in results_dir.names():
            if stale in {"targeted-run.json", "last-failure.json"} or stale.endswith(".receipt.json"):
                results_dir.unlink(stale)
        run_raw_root = raw_dir.child(run_id)
        for current_case in case_ids:
            case = case_objects_by_id[current_case]
            case_bytes = case_bytes_by_id[current_case]
            rubric = rubric_objects_by_case_id[current_case]
            rubric_bytes = rubric_bytes_by_case_id[current_case]
            marker = str(rubric["secrecy_marker"])
            with run_raw_root.child(current_case) as case_raw:
                with tempfile.TemporaryDirectory(prefix=f"uber-eval-{current_case}-") as temp_bundle:
                    subject_bundle = Path(temp_bundle) / "subject"
                    grader_bundle = Path(temp_bundle) / "grader"
                    subject_files, context_bindings = copy_subject_bundle(
                        case, case_bytes, input_bytes_by_logical_path, subject_bundle,
                    )
                    subject_prompt, _ = inline_payload(subject_files, "subject")
                    if marker in subject_prompt or rubric_bytes.decode("utf-8") in subject_prompt:
                        raise EvalFailure("subject", "hidden rubric leaked into subject context")
                    current_phase = "subject"
                    calls["subject"] += 1
                    subject, subject_trace, subject_raw = invoke(
                        repo, case_raw, subject_bundle, "subject", current_case, runner, model, effort,
                        int(suite["timeout_seconds"]), subject_prompt, list(subject_files),
                    )
                    if subject_trace["runtime_thread_id"] in runtime_ids:
                        raise EvalFailure("subject", "fresh runtime context id was reused")
                    runtime_ids.add(subject_trace["runtime_thread_id"])
                    if marker in case_raw.read_bytes("subject.stdout.jsonl").decode(errors="replace"):
                        raise EvalFailure("subject", "hidden rubric marker leaked into subject trace")
                    validate_subject_against_rubric(subject, rubric)
                    grader_files = {
                        "rubric.json": rubric_bytes,
                        "subject-output.json": json.dumps(subject, indent=2, sort_keys=True, ensure_ascii=False).encode() + b"\n",
                        "subject-trace.json": json.dumps(subject_trace, indent=2, sort_keys=True, ensure_ascii=False).encode() + b"\n",
                    }
                    grader_bundle.mkdir(parents=True)
                    for name, data in grader_files.items():
                        (grader_bundle / name).write_bytes(data)
                    if set(tree_snapshot(grader_bundle)) != set(grader_files):
                        raise EvalFailure("grader", "grader bundle allowlist mismatch")
                    grader_prompt, grader_context = inline_payload(grader_files, "grader")
                    current_phase = "grader"
                    calls["grader"] += 1
                    grader, grader_trace, grader_raw = invoke(
                        repo, case_raw, grader_bundle, "grader", current_case, runner, model, effort,
                        int(suite["timeout_seconds"]), grader_prompt, list(grader_files),
                    )
                    if grader_trace["runtime_thread_id"] in runtime_ids:
                        raise EvalFailure("grader", "fresh runtime context id was reused")
                    runtime_ids.add(grader_trace["runtime_thread_id"])
                    bindings = {
                        "model": model, "reasoning_effort": effort,
                        "context_files": context_bindings, "case_sha256": sha(case_bytes),
                        "rubric_sha256": sha(rubric_bytes),
                        "subject_output_sha256": sha(packed(subject)), "subject_trace": subject_raw,
                        "grader_context_files": grader_context, "grader_output_sha256": sha(packed(grader)),
                        "grader_trace": grader_raw,
                    }
                    receipt = {
                        "schema_version": 1, "run_id": run_id, "case_id": current_case,
                        "status": "passed", "binding": bindings,
                        "suite_sha256": suite_digest, "base_manifest_sha256": base_digest,
                        "current_evaluation_status_sha256": sha(input_bytes_by_logical_path[status_logical]),
                        "input_manifest_sha256": input_digest, "runner_provenance": runner_provenance,
                        "runner_mode": runner_provenance["mode"], "runner_sha256": runner_provenance["sha256"],
                        "harness_sha256": harness_sha256, "process": {"subject": subject_trace, "grader": grader_trace},
                        "promotion_state": "not_promoted", "evaluation_state": "fresh_eval_required",
                    }
                    receipt["run_hash"] = sha(packed(receipt))
                    receipts.append(receipt)
        run_raw_root.close()
        run_raw_root = None
        current_case = current_phase = "output"
        revalidate_input_snapshots(repo, input_bytes_by_logical_path)
        runner.revalidate()
        if sha(HARNESS_PATH.read_bytes()) != harness_sha256:
            raise EvalFailure("output", "eval harness changed during run")
        expected_outputs: dict[str, bytes] = {}
        for receipt in receipts:
            name = f"{receipt['case_id']}.receipt.json"
            expected_outputs[name] = pretty_json(receipt)
            results_dir.write_bytes(name, expected_outputs[name])
            published_names.append(name)
        summary = {
            "schema_version": 1, "suite_id": suite["suite_id"], "run_id": run_id,
            "status": "passed", "model": model, "reasoning_effort": effort,
            "call_count": calls, "case_results": {r["case_id"]: r["status"] for r in receipts},
            "receipt_hashes": {r["case_id"]: r["run_hash"] for r in receipts},
            "suite_sha256": suite_digest, "base_manifest_sha256": base_digest,
            "current_evaluation_status_sha256": sha(input_bytes_by_logical_path[status_logical]),
            "input_manifest_sha256": input_digest, "runner_provenance": runner_provenance,
            "runner_mode": runner_provenance["mode"], "runner_sha256": runner_provenance["sha256"],
            "harness_sha256": harness_sha256,
            "promotion_state": "not_promoted", "evaluation_state": "fresh_eval_required",
            "remaining_gap": "Full UberAccept, UberGoal, and UberPlan behavioral suites still require fresh evaluation.",
        }
        expected_outputs["targeted-run.json"] = pretty_json(summary)
        results_dir.write_bytes("targeted-run.json", expected_outputs["targeted-run.json"])
        published_names.append("targeted-run.json")
        revalidate_input_snapshots(repo, input_bytes_by_logical_path)
        runner.revalidate()
        if sha(HARNESS_PATH.read_bytes()) != harness_sha256:
            raise EvalFailure("output", "eval harness changed during run")
        relevant_names = {
            name for name in results_dir.names()
            if name in {"targeted-run.json", "last-failure.json"} or name.endswith(".receipt.json")
        }
        if relevant_names != set(expected_outputs):
            raise EvalFailure("output", "canonical result set changed during publication")
        for name, expected in expected_outputs.items():
            if results_dir.read_bytes(name) != expected:
                raise EvalFailure("output", f"canonical output changed during publication: {name}")
        return summary
    except (EvalFailure, KeyError, ValueError, OSError) as exc:
        if not outputs_validated or results_dir is None:
            raise
        failure = {
            "schema_version": 1, "suite_id": suite.get("suite_id"), "run_id": run_id,
            "case_id": current_case, "phase": getattr(exc, "phase", current_phase),
            "model": model, "reasoning_effort": effort, "reason": str(exc),
            "call_count": calls, "status": "failed_closed",
        }
        try:
            for stale in results_dir.anchored_names():
                if stale in set(published_names) | {"targeted-run.json"} or stale.endswith(".receipt.json"):
                    results_dir.anchored_unlink(stale)
            results_dir.revalidate()
            results_dir.write_json("last-failure.json", failure)
        except (EvalFailure, OSError):
            pass
        raise
    finally:
        if run_raw_root is not None:
            run_raw_root.close()
        if raw_dir is not None:
            raw_dir.close()
        if results_dir is not None:
            results_dir.close()
        if runner is not None:
            runner.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=ROOT)
    parser.add_argument("--suite", type=Path, default=SUITE_PATH)
    parser.add_argument("--codex-bin", required=True, help="explicit absolute native Codex path; test fakes also require --allow-test-runner")
    parser.add_argument("--model", default="gpt-5.6-sol")
    parser.add_argument("--effort", default="ultra")
    parser.add_argument("--allow-test-runner", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    try:
        summary = run_suite(args.repo.resolve(), args.suite.resolve(), args.codex_bin, args.model, args.effort, args.allow_test_runner)
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
