#!/usr/bin/env python3
"""Run four isolated reviewer-selection subject/grader evals."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SUITE_PATH = Path(__file__).with_name("suite.json")
EXPECTED_SUITE_SHA256 = "sha256:9f5bef7e1f96f4a4fa282ffe65c0f7d92f2fabcede7384efff36e3c402705142"
EXPECTED_BASE_SHA256 = "sha256:29ef5d6aea15c18143187c79df4d57e104df1a5b848cdfa427b0275be2e0a914"
EXPECTED_INPUT_MANIFEST_SHA256 = "sha256:14da4a1d3e0d7aeb43d50faf4079b4bfd05e5eb325c42f3952243d654be26884"
EXPECTED_CASE_IDS = {"generic-cross-model", "required-sol-ultra-unavailable", "explicit-claude-by-name", "gaia-adversarial-review"}
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


def sha(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def input_manifest_digest(paths: list[Path], root: Path) -> str:
    root = root.resolve()
    entries = [{"path": str(path.resolve().relative_to(root)), "sha256": sha(path.read_bytes())} for path in sorted(set(paths))]
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


def confined_path(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f"path escapes repository: {relative}")
    return path


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
    path.write_bytes(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False).encode() + b"\n")


def copy_subject_bundle(repo: Path, case_path: Path, bundle: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    case = load_json(case_path)
    bundle.mkdir(parents=True)
    copied: list[dict[str, Any]] = []
    for relative in case.get("context_files", []):
        target = bundle / str(relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(safe_path(repo, str(relative)), target)
        copied.append({"path": str(relative), "sha256": sha(target.read_bytes())})
    target_case = bundle / "case.json"
    shutil.copyfile(case_path, target_case)
    copied.append({"path": "case.json", "sha256": sha(target_case.read_bytes())})
    expected = {str(item) for item in case.get("context_files", [])} | {"case.json"}
    if set(tree_snapshot(bundle)) != expected:
        raise ValueError("subject bundle allowlist mismatch")
    return case, copied


def inline_payload(bundle: Path, phase: str) -> tuple[str, list[dict[str, Any]]]:
    files = []
    bindings = []
    for relative, digest in tree_snapshot(bundle).items():
        data = (bundle / relative).read_bytes()
        files.append({"path": relative, "content": data.decode("utf-8")})
        bindings.append({"path": relative, "sha256": digest})
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
    repo: Path, raw_dir: Path, bundle: Path, phase: str, case_id: str,
    codex_bin: str, model: str, effort: str, timeout: int, prompt: str,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, str]]:
    invocation_id = str(uuid.uuid4())
    cmd = command(codex_bin, model, effort, bundle)
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
            proc = subprocess.run(cmd, cwd=bundle, input=prompt, text=True, capture_output=True, timeout=timeout, env=env, check=False)
            stdout, stderr, returncode = proc.stdout.encode(), proc.stderr.encode(), proc.returncode
        except subprocess.TimeoutExpired as exc:
            stdout = (exc.stdout or b"") if isinstance(exc.stdout, bytes) else (exc.stdout or "").encode()
            stderr = (exc.stderr or b"") if isinstance(exc.stderr, bytes) else (exc.stderr or "").encode()
            returncode, timed_out = -1, True
    (raw_dir / f"{phase}.stdout.jsonl").write_bytes(stdout)
    (raw_dir / f"{phase}.stderr.log").write_bytes(stderr)
    (raw_dir / f"{phase}.prompt.sha256").write_text(sha(prompt.encode()) + "\n")
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
        "delivered_context_files": sorted(tree_snapshot(bundle)), "files_read": [],
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
    suite: dict[str, Any] = {}
    run_id = str(uuid.uuid4())
    results = repo / "evals/reviewer-selection/results"
    cleaned = False
    calls = {"subject": 0, "grader": 0}
    receipts: list[dict[str, Any]] = []
    runtime_ids: set[str] = set()
    current_case = current_phase = "preflight"
    published_paths: list[Path] = []
    try:
        suite = load_json(suite_path)
        suite_digest = sha(suite_path.read_bytes())
        results = confined_path(repo, str(suite["result_dir"]))
        raw_root = confined_path(repo, str(suite["raw_artifact_root"]))
        if not raw_root.is_relative_to((repo / ".uberlearn-local").resolve()):
            raise ValueError("raw artifact root must stay under .uberlearn-local")
        results.mkdir(parents=True, exist_ok=True)
        for stale in [results / "targeted-run.json", results / "last-failure.json", *results.glob("*.receipt.json")]:
            stale.unlink(missing_ok=True)
        cleaned = True
        if (model, effort) != (suite.get("model"), suite.get("reasoning_effort")):
            raise EvalFailure("preflight", f"model binding mismatch: requested {model}/{effort}")
        if not test_runner and (codex_bin != "codex" or results != (repo / "evals/reviewer-selection/results").resolve()):
            raise EvalFailure("preflight", "canonical runner, suite, and result paths are required")
        base_path = safe_path(suite_path.parent, str(suite["base_manifest"]))
        base_digest = sha(base_path.read_bytes())
        if not test_runner and (suite_digest, base_digest) != (EXPECTED_SUITE_SHA256, EXPECTED_BASE_SHA256):
            raise EvalFailure("preflight", "suite or base manifest digest mismatch")
        case_paths = [safe_path(suite_path.parent, str(item)) for item in suite.get("cases", [])]
        if not case_paths or len(case_paths) > 4:
            raise EvalFailure("preflight", "suite must contain one to four cases")
        case_ids = [str(load_json(path)["case_id"]) for path in case_paths]
        if len(set(case_ids)) != len(case_ids) or any(Path(case_id).name != case_id for case_id in case_ids):
            raise EvalFailure("preflight", "case ids must be unique safe filenames")
        if not test_runner and set(case_ids) != EXPECTED_CASE_IDS:
            raise EvalFailure("preflight", "canonical suite case set mismatch")
        manifest_paths = [base_path, suite_path, *case_paths]
        rubric_paths = [safe_path(suite_path.parent, str(suite["rubrics"][case_id])) for case_id in case_ids]
        manifest_paths.extend(rubric_paths)
        for case_path in case_paths:
            case = load_json(case_path)
            manifest_paths.extend(safe_path(repo, str(relative)) for relative in case.get("context_files", []))
        input_digest = input_manifest_digest(manifest_paths, repo)
        if not test_runner and input_digest != EXPECTED_INPUT_MANIFEST_SHA256:
            raise EvalFailure("preflight", "case, rubric, or context manifest digest mismatch")
        run_raw_root = raw_root / run_id
        run_raw_root.mkdir(parents=True)
        for case_path in case_paths:
            case = load_json(case_path)
            current_case = str(case["case_id"])
            rubric_path = safe_path(suite_path.parent, str(suite["rubrics"][current_case]))
            rubric = load_json(rubric_path)
            marker = str(rubric["secrecy_marker"])
            case_raw = run_raw_root / current_case
            case_raw.mkdir()
            with tempfile.TemporaryDirectory(prefix=f"uber-eval-{current_case}-") as temp_bundle:
                subject_bundle = Path(temp_bundle) / "subject"
                grader_bundle = Path(temp_bundle) / "grader"
                _, context_bindings = copy_subject_bundle(repo, case_path, subject_bundle)
                subject_prompt, _ = inline_payload(subject_bundle, "subject")
                if marker in subject_prompt or rubric_path.read_text(encoding="utf-8") in subject_prompt:
                    raise EvalFailure("subject", "hidden rubric leaked into subject context")
                current_phase = "subject"
                calls["subject"] += 1
                subject, subject_trace, subject_raw = invoke(
                    repo, case_raw, subject_bundle, "subject", current_case, codex_bin, model, effort, int(suite["timeout_seconds"]), subject_prompt)
                if subject_trace["runtime_thread_id"] in runtime_ids:
                    raise EvalFailure("subject", "fresh runtime context id was reused")
                runtime_ids.add(subject_trace["runtime_thread_id"])
                if marker in (case_raw / "subject.stdout.jsonl").read_text(errors="replace"):
                    raise EvalFailure("subject", "hidden rubric marker leaked into subject trace")
                validate_subject_against_rubric(subject, rubric)
                grader_bundle.mkdir(parents=True)
                write_json(grader_bundle / "rubric.json", rubric)
                write_json(grader_bundle / "subject-output.json", subject)
                write_json(grader_bundle / "subject-trace.json", subject_trace)
                if set(tree_snapshot(grader_bundle)) != {"rubric.json", "subject-output.json", "subject-trace.json"}:
                    raise EvalFailure("grader", "grader bundle allowlist mismatch")
                grader_prompt, grader_context = inline_payload(grader_bundle, "grader")
                current_phase = "grader"
                calls["grader"] += 1
                grader, grader_trace, grader_raw = invoke(
                    repo, case_raw, grader_bundle, "grader", current_case, codex_bin, model, effort, int(suite["timeout_seconds"]), grader_prompt)
                if grader_trace["runtime_thread_id"] in runtime_ids:
                    raise EvalFailure("grader", "fresh runtime context id was reused")
                runtime_ids.add(grader_trace["runtime_thread_id"])
                bindings = {
                    "model": model, "reasoning_effort": effort,
                    "context_files": context_bindings, "case_sha256": sha(case_path.read_bytes()),
                    "rubric_sha256": sha(rubric_path.read_bytes()),
                    "subject_output_sha256": sha(packed(subject)), "subject_trace": subject_raw,
                    "grader_context_files": grader_context, "grader_output_sha256": sha(packed(grader)),
                    "grader_trace": grader_raw,
                }
                receipt = {
                    "schema_version": 1, "run_id": run_id, "case_id": current_case,
                    "status": "passed", "binding": bindings,
                    "suite_sha256": suite_digest, "base_manifest_sha256": base_digest, "input_manifest_sha256": input_digest,
                    "runner_mode": "test_runner" if test_runner else "codex",
                    "runner_sha256": sha(Path(codex_bin).resolve().read_bytes()) if test_runner else sha(Path(shutil.which("codex")).resolve().read_bytes()),
                    "process": {"subject": subject_trace, "grader": grader_trace},
                    "promotion_state": "not_promoted", "evaluation_state": "fresh_eval_required",
                }
                receipt["run_hash"] = sha(packed(receipt))
                receipts.append(receipt)
        for receipt in receipts:
            write_json(results / f"{receipt['case_id']}.receipt.json", receipt)
            published_paths.append(results / f"{receipt['case_id']}.receipt.json")
        summary = {
            "schema_version": 1, "suite_id": suite["suite_id"], "run_id": run_id,
            "status": "passed", "model": model, "reasoning_effort": effort,
            "call_count": calls, "case_results": {r["case_id"]: r["status"] for r in receipts},
            "receipt_hashes": {r["case_id"]: r["run_hash"] for r in receipts},
            "suite_sha256": suite_digest, "base_manifest_sha256": base_digest,
            "input_manifest_sha256": input_digest,
            "runner_mode": "test_runner" if test_runner else "codex",
            "runner_sha256": sha(Path(codex_bin).resolve().read_bytes()) if test_runner else sha(Path(shutil.which("codex")).resolve().read_bytes()),
            "promotion_state": "not_promoted", "evaluation_state": "fresh_eval_required",
            "remaining_gap": "Full UberAccept, UberGoal, and UberPlan behavioral suites still require fresh evaluation.",
        }
        write_json(results / "targeted-run.json", summary)
        published_paths.append(results / "targeted-run.json")
        return summary
    except (EvalFailure, KeyError, ValueError, OSError) as exc:
        results.mkdir(parents=True, exist_ok=True)
        for stale in [*published_paths, results / "targeted-run.json", *results.glob("*.receipt.json")]:
            stale.unlink(missing_ok=True)
        failure = {
            "schema_version": 1, "suite_id": suite.get("suite_id"), "run_id": run_id,
            "case_id": current_case, "phase": getattr(exc, "phase", current_phase),
            "model": model, "reasoning_effort": effort, "reason": str(exc),
            "call_count": calls, "status": "failed_closed",
        }
        write_json(results / "last-failure.json", failure)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=ROOT)
    parser.add_argument("--suite", type=Path, default=SUITE_PATH)
    parser.add_argument("--codex-bin", default="codex")
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
