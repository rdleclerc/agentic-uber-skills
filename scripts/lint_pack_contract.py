#!/usr/bin/env python3
"""Lint repo-level agent contract and Uber skill routing policy."""
from __future__ import annotations

from pathlib import Path
import argparse
from dataclasses import dataclass
import hashlib
import math
import os
import re
import subprocess
import sys
import tempfile
import time
import tomllib

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
PACK_SKILLS = [
    "uberrca",
    "uber-skill-creator",
    "ubergoal",
    "uberplan",
    "uberaccept",
    "uberskillevolver",
    "ubersimplify",
    "uberassess",
    "uberarchitect",
    "ubershow",
    "testing-strategy",
]
UBER_PHASE_SKILLS = ["uberplan", "uberaccept", "uberskillevolver", "ubersimplify", "uberassess", "uberarchitect"]
UTILITY_IMPLICIT_SKILLS = ["uberrca", "uber-skill-creator", "ubershow", "testing-strategy"]
ROOT_REQUIRED_FILES = ["AGENTS.md", "CLAUDE.md", "README.md", "ROADMAP.md"]
SKILL_WORD_BUDGETS = {
    "ubergoal/SKILL.md": 800,
    "uberplan/SKILL.md": 3400,
    "uberaccept/SKILL.md": 2150,
    "uberassess/SKILL.md": 1900,
    "uberarchitect/SKILL.md": 900,
    "uberrca/SKILL.md": 1500,
    "ubershow/SKILL.md": 1400,
    "uber-skill-creator/SKILL.md": 1350,
    "uberskillevolver/SKILL.md": 1550,
    "ubersimplify/SKILL.md": 700,
    "testing-strategy/SKILL.md": 900,
}
FORBIDDEN_FRONTMATTER_KEYS = {"model", "effort"}
MODEL_ID_RE = re.compile(
    r"\b(?:claude-[A-Za-z0-9][A-Za-z0-9_.-]*-\d+(?:[.-]\d+)*|gpt-\d+(?:[.-]\d+)*(?:-[A-Za-z0-9_.-]+)?)\b",
    re.I,
)
ABSOLUTE_PATH_RE = re.compile(
    r"(?<![A-Za-z0-9_:$~.-])"
    r"(/(?:Users|tmp|private|var|opt|usr|etc|home|Library|Applications|Volumes)/[^\s`'\"<>),]+)"
)
MACHINE_USER_PATH_RE = re.compile(r"/Users/[^/\s`'\"<>),]+/[^\s`'\"<>),]*")
PORTABILITY_EXEMPT_MARKERS = ("fixture-path: intentional", "portable-path: intentional")
DOCTRINE_TEXT_SUFFIXES = {".md", ".txt", ".toml", ".yaml", ".yml", ".json", ".html"}
AGENTS_REQUIRED_PHRASES = [
    "$ubergoal` is the only default/implicit Uber lifecycle router",
    "All skills in this pack must be installed and exposed to Codex sessions",
    "Review and acceptance lanes use a fresh, independent context on the strongest model and reasoning effort allowed by the active project policy; record `lane_used` in the receipt; never silently downgrade. Claude may be selected only when the operator explicitly requests Claude by name. In gaia contexts the spine's lane policy governs (`knowledge/coding-agent-operating-spine.md` in the gaia workspace repo).",
    "Phase skills are explicit or wrapper-invoked",
    "uberassess` = source-to-recommendation due diligence",
    "ubershow` = visual communication utility",
    "testing-strategy` = automatic portable test-selection utility",
    "uberarchitect` = architecture stepback gate",
    "uberrca` = general incident/root-cause authority",
    "Agent Advocate = agent-behavior-specific RCA lens",
    "New standalone CLIs only where fixtures prove separate need; default = module in the pack-contract aggregator",
    "Source repo: this repository's checkout location",
    "Local Codex install target: `~/.codex/skills/<skill>`",
    "Local Claude install target: `~/.claude/skills/<skill>`",
    "Codex adapter metadata should expose every pack skill",
    "Do not commit, tag, push, or publish without explicit user authorization",
    "child/sub-`uberplan` appendix",
    "Reword a fingerprinted rule",
]
README_REQUIRED_PHRASES = [
    "Agent-facing source authority lives in [AGENTS.md](AGENTS.md)",
    "Review and acceptance lanes use a fresh, independent context on the strongest model and reasoning effort allowed by the active project policy; record `lane_used` in the receipt; never silently downgrade. Claude may be selected only when the operator explicitly requests Claude by name.",
    "invoke `$ubergoal` as the implicit lifecycle router",
    "`$uberrca` is the general incident/debugging/root-cause utility",
    "`$ubershow`",
    "`$testing-strategy`",
    "skills invoked",
]
FORBIDDEN_AUTOMATIC_CLAUDE_PATTERNS = [
    r"review and acceptance lanes use the highest-capability available claude lane",
    r"claude\s+--model\s+opus\s+--effort\s+max",
    r"on the highest-capability claude lane \+ review-board lanes",
    r"high-tier claude lane",
    r"explicit claude review or cross-model review",
    r"\bcross-model (?:review )?request\b(?![^.\n]{0,80}\b(?:does not|do not|not authorized)\b)[^.\n]{0,80}\bclaude\b",
]
ROUTING_ANSWER_KEY_REQUIRED_PHRASES = [
    "Production launchd service edit.",
    "full 4-phase ladder, active-project reviewer lane, safe-predecessor approval, live/runtime proof",
]
ROADMAP_REQUIRED_PHRASES = [
    "`ubergoal` is the only implicit/default Uber lifecycle router",
    "Phase skills are explicit or wrapper-invoked",
    "Codex adapter metadata still exposes every skill in the pack",
    "uberassess` = source-to-recommendation due diligence",
    "Build a small pack-level harness before creating a standalone `ubereval` skill",
    "Uberassess dogfooding",
    "Ubershow dogfooding",
    "Testing strategy dogfooding",
    "RCA-driven testing adaptation",
]
DRIFT_REGISTRY = "references/drift-fingerprints.toml"
DRIFT_REQUIRED_FIELDS = {
    "id",
    "owner",
    "adoption_state",
    "canonical_source",
    "target_paths",
    "match",
    "pattern",
    "normalization",
    "allowed_absences",
    "severity",
    "blocking_wave",
}
DRIFT_OPTIONAL_FIELDS = {"pending", "git_ref"}
DRIFT_ADOPTION_STATES = {"report_only", "blocking", "planned"}
DRIFT_MATCH_TYPES = {"literal", "regex", "sha256"}
DRIFT_NORMALIZATIONS = {"none", "whitespace"}
DRIFT_SEVERITIES = {"error", "warn"}
INSTALL_SYNC_IGNORED_EXTRAS = {
    "chronicle",
    "harmonic",
    "codex-primary-runtime",
    "gaia-session-lane",
    "build-agent-eval",
    "design-agent-memory",
    "design-context-engine",
    "design-source-lane",
    "openclaw-agentic-skill-creator",
    "openclaw-agentic-tool-designer",
    "review-agentic-architecture",
}
SECRET_SCAN_DIRS = ["coordination", "evals"]
SECRET_SCAN_SUFFIXES = DOCTRINE_TEXT_SUFFIXES
SECRET_TOKEN_PATTERNS = [
    ("openai_sk", re.compile(r"\bsk-[A-Za-z0-9_-]{8,}\b")),
    ("slack_xoxb", re.compile(r"\bxoxb-[A-Za-z0-9-]{8,}\b")),
    ("slack_xoxp", re.compile(r"\bxoxp-[A-Za-z0-9-]{8,}\b")),
    ("slack_xoxc", re.compile(r"\bxoxc-[A-Za-z0-9-]{8,}\b")),
    ("slack_xoxs", re.compile(r"\bxoxs-[A-Za-z0-9-]{8,}\b")),
    ("slack_xapp", re.compile(r"\bxapp-[A-Za-z0-9-]{8,}\b")),
    ("github_ghp", re.compile(r"\bghp_[A-Za-z0-9_]{16,}\b")),
    ("github_gho", re.compile(r"\bgho_[A-Za-z0-9_]{16,}\b")),
    ("github_pat", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{16,}\b")),
    ("aws_akia", re.compile(r"\bAKIA[0-9A-Z]{12,}\b")),
    (
        "aws_secret_key",
        re.compile(
            r"(?i)\b(?:aws[_-]?)?(?:secret|access)[_-]?(?:access[_-]?)?key\b"
            r"[^\n]{0,40}[:=]\s*['\"]?[A-Za-z0-9/+=]{40}['\"]?"
        ),
    ),
    ("google_aiza", re.compile(r"\bAIza[0-9A-Za-z_-]{20,}\b")),
    ("bearer_long", re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{40,}\b")),
    ("pem_private_key", re.compile(r"-----BEGIN (?:RSA |DSA |EC |OPENSSH |)?PRIVATE KEY-----")),
    ("jwt_base64url", re.compile(r"\b[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{16,}\b")),
    ("hex_32", re.compile(r"\b[0-9A-Fa-f]{32,}\b")),
    ("base64_32", re.compile(r"\b(?=[A-Za-z0-9+/=]{32,}\b)(?=.*[+=])(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])[A-Za-z0-9+/]{32,}={0,2}\b")),
]


@dataclass(frozen=True)
class CheckReport:
    lines: list[str]
    blocking_failures: list[str]
    errors: list[str]

    def exit_code(self, strict: bool) -> int:
        if self.errors:
            return 1
        if strict and self.blocking_failures:
            return 1
        return 0

    def print(self) -> None:
        for line in self.lines:
            print(line)
        for error in self.errors:
            print(f"ERROR: {error}", file=sys.stderr)


def read(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def frontmatter(root: Path, skill: str) -> str:
    text = read(root / skill / "SKILL.md")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", text, flags=re.S)
    if not match:
        return ""
    return match.group(1)


def doctrine_text_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for rel in ["AGENTS.md", "README.md", "ROADMAP.md"]:
        path = root / rel
        if path.exists():
            files.append(path)
    for skill in PACK_SKILLS:
        skill_root = root / skill
        skill_md = skill_root / "SKILL.md"
        if skill_md.exists():
            files.append(skill_md)
        for dirname in ["references", "templates"]:
            base = skill_root / dirname
            if base.exists():
                files.extend(path for path in base.rglob("*") if path.is_file() and path.suffix in DOCTRINE_TEXT_SUFFIXES)
    for dirname in ["references", "templates"]:
        base = root / dirname
        if base.exists():
            files.extend(path for path in base.rglob("*") if path.is_file() and path.suffix in DOCTRINE_TEXT_SUFFIXES)
    return sorted(set(files))


def has_portability_exemption(lines: list[str], index: int) -> bool:
    for offset in (-1, 0):
        candidate = index + offset
        if 0 <= candidate < len(lines):
            if any(marker in lines[candidate] for marker in PORTABILITY_EXEMPT_MARKERS):
                return True
    return False


def parameterized_default_spans(line: str) -> list[tuple[int, int]]:
    return [(match.start(), match.end()) for match in re.finditer(r"\$\{[^}\n]*:-[^}\n]*\}", line)]


def match_inside_spans(match: re.Match[str], spans: list[tuple[int, int]]) -> bool:
    return any(start <= match.start() and match.end() <= end for start, end in spans)


def is_parameterized_path_match(line: str, match: re.Match[str]) -> bool:
    candidate = match.group(0)
    return candidate.startswith("~/") or match_inside_spans(match, parameterized_default_spans(line))


def clean_path_candidate(raw: str) -> str:
    return raw.rstrip(".,:;")


def validate_frontmatter_policy(root: Path, errors: list[str]) -> None:
    for skill in PACK_SKILLS:
        path = root / skill / "SKILL.md"
        if not path.exists():
            errors.append(f"missing skill package: {skill}/SKILL.md")
            continue
        meta = frontmatter(root, skill)
        if not meta:
            errors.append(f"{skill} must have SKILL.md frontmatter")
            continue
        for match in re.finditer(r"^\s*([A-Za-z0-9_-]+)\s*:", meta, flags=re.M):
            key = match.group(1).lower()
            if key in FORBIDDEN_FRONTMATTER_KEYS:
                errors.append(f"{skill} SKILL.md frontmatter must not contain `{key}:`")
        model_match = MODEL_ID_RE.search(meta)
        if model_match:
            errors.append(f"{skill} SKILL.md frontmatter must not hardcode model id `{model_match.group(0)}`")


def validate_skill_word_budgets(root: Path, errors: list[str]) -> None:
    for rel, budget in SKILL_WORD_BUDGETS.items():
        path = root / rel
        if not path.exists():
            errors.append(f"word budget target missing: {rel}")
            continue
        count = len(path.read_text().split())
        if count > budget:
            errors.append(f"{rel} word budget exceeded: {count} > {budget}")


def validate_portability_oracle(root: Path, errors: list[str]) -> None:
    for path in doctrine_text_files(root):
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        rel = path.relative_to(root)
        lines = text.splitlines()
        for index, line in enumerate(lines):
            if has_portability_exemption(lines, index):
                continue
            for match in MACHINE_USER_PATH_RE.finditer(line):
                if is_parameterized_path_match(line, match):
                    continue
                candidate = clean_path_candidate(match.group(0))
                errors.append(f"{rel}:{index + 1} machine-specific path must be parameterized or marker-exempted: {candidate}")
            for match in ABSOLUTE_PATH_RE.finditer(line):
                if is_parameterized_path_match(line, match):
                    continue
                candidate = clean_path_candidate(match.group(1))
                if MACHINE_USER_PATH_RE.search(candidate):
                    continue
                if not Path(candidate).exists():
                    errors.append(f"{rel}:{index + 1} absolute path does not exist or need parameterization: {candidate}")


def resolve_git_dir(root: Path) -> tuple[Path | None, str | None]:
    dot_git = root / ".git"
    if dot_git.is_dir():
        return dot_git, None
    if dot_git.is_file():
        try:
            text = dot_git.read_text().strip()
        except OSError as exc:
            return None, f"cannot read .git file at {dot_git}: {exc}"
        if not text.startswith("gitdir:"):
            return None, f"{dot_git} is not a gitdir pointer"
        raw = text.split(":", 1)[1].strip()
        git_dir = Path(raw).expanduser()
        if not git_dir.is_absolute():
            git_dir = (root / git_dir).resolve()
        return git_dir, None
    return None, f"{root} has no .git directory or gitdir pointer"


def probe_directory_write(path: Path, label: str) -> str | None:
    if not path.exists():
        return f"{label} does not exist: {path}"
    if not path.is_dir():
        return f"{label} is not a directory: {path}"
    try:
        with tempfile.NamedTemporaryFile(prefix="codex-preflight-", dir=path, delete=True) as handle:
            handle.write(b"ok")
            handle.flush()
    except OSError as exc:
        return f"{label} is not writable: {path} ({exc})"
    return None


def check_dispatch_preflight(root: Path) -> CheckReport:
    """Preflight dispatch writeability for the active implementation root."""
    lines = [f"DISPATCH PREFLIGHT root={root}"]
    errors: list[str] = []
    root = root.resolve()
    if not root.exists():
        errors.append(f"root does not exist: {root}")
        return CheckReport(lines, [], errors)
    if not root.is_dir():
        errors.append(f"root is not a directory: {root}")
        return CheckReport(lines, [], errors)

    git_dir, git_error = resolve_git_dir(root)
    if git_error:
        errors.append(git_error)
    elif git_dir:
        git_write_error = probe_directory_write(git_dir, ".git directory")
        if git_write_error:
            errors.append(git_write_error)
        else:
            lines.append(f"PASS git-dir-writable path={git_dir}")

    try:
        proc = subprocess.run(
            ["git", "-C", str(root), "status", "--porcelain"],
            text=True,
            capture_output=True,
            check=False,
            timeout=20,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        errors.append(f"git status probe failed to run: {exc}")
    else:
        if proc.returncode != 0:
            detail = (proc.stderr or proc.stdout or "").strip()
            suffix = f": {detail}" if detail else ""
            errors.append(f"git status probe failed with exit {proc.returncode}{suffix}")
        else:
            lines.append("PASS git-status")

    tmp_root = Path(os.environ.get("TMPDIR") or tempfile.gettempdir()).expanduser()
    tmp_error = probe_directory_write(tmp_root, "TMPDIR")
    if tmp_error:
        errors.append(tmp_error)
    else:
        lines.append(f"PASS tmpdir-writable path={tmp_root}")

    if not errors:
        lines.append("PASS dispatch preflight")
    return CheckReport(lines, [], errors)


def expand_shell_token(value: str, *, use_env: bool = True) -> str:
    def replace(match: re.Match[str]) -> str:
        name = match.group("name")
        default = match.group("default")
        if default is not None:
            if use_env and os.environ.get(name):
                return os.environ[name]
            return str(Path(default).expanduser())
        return os.environ.get(name, "") if use_env else ""

    expanded = re.sub(
        r"(?<!\\)\$\{(?P<name>[A-Za-z_][A-Za-z0-9_]*)(?::-((?P<default>[^}]*)))?\}",
        replace,
        value,
    )
    expanded = expanded.replace(r"\${", "${")
    return str(Path(expanded).expanduser()) if expanded.startswith("~") else expanded


def resolve_registry_path(root: Path, raw_path: str) -> Path:
    expanded = expand_shell_token(raw_path, use_env=True)
    path = Path(expanded).expanduser()
    if not path.is_absolute():
        path = root / path
    return path


def normalize_match_text(value: str, normalization: str) -> str:
    if normalization == "whitespace":
        return " ".join(value.split())
    return value


def sha256_pattern_digest(pattern: str) -> str | None:
    match = re.fullmatch(r"(?:sha256:)?([0-9a-f]{64})", pattern.strip())
    return match.group(1) if match else None


def load_drift_registry(path: Path) -> tuple[list[dict[str, object]], list[str]]:
    if not path.exists():
        return [], [f"drift registry missing: {path}"]
    try:
        data = tomllib.loads(path.read_text())
    except tomllib.TOMLDecodeError as exc:
        return [], [f"drift registry TOML error in {path}: {exc}"]
    raw_entries = data.get("fingerprint")
    if not isinstance(raw_entries, list):
        return [], [f"drift registry {path} must contain [[fingerprint]] entries"]

    entries: list[dict[str, object]] = []
    errors: list[str] = []
    for index, entry in enumerate(raw_entries, start=1):
        if not isinstance(entry, dict):
            errors.append(f"drift registry entry {index} must be a table")
            continue
        entry_id = str(entry.get("id") or f"entry-{index}")
        missing = sorted(DRIFT_REQUIRED_FIELDS - set(entry))
        if missing:
            errors.append(f"drift registry entry {entry_id} missing required field(s): {', '.join(missing)}")
            continue
        unknown = sorted(set(entry) - DRIFT_REQUIRED_FIELDS - DRIFT_OPTIONAL_FIELDS)
        if unknown:
            errors.append(f"drift registry entry {entry_id} has unknown field(s): {', '.join(unknown)}")
        for field in ["id", "owner", "adoption_state", "canonical_source", "match", "pattern", "normalization", "severity"]:
            if not isinstance(entry[field], str):
                errors.append(f"drift registry entry {entry_id} field {field} must be a string")
        if entry["adoption_state"] not in DRIFT_ADOPTION_STATES:
            errors.append(f"drift registry entry {entry_id} has invalid adoption_state: {entry['adoption_state']}")
        if entry["match"] not in DRIFT_MATCH_TYPES:
            errors.append(f"drift registry entry {entry_id} has invalid match: {entry['match']}")
        if entry["normalization"] not in DRIFT_NORMALIZATIONS:
            errors.append(f"drift registry entry {entry_id} has invalid normalization: {entry['normalization']}")
        if entry["match"] == "sha256" and entry["normalization"] != "none":
            errors.append(f"drift registry entry {entry_id} sha256 match requires normalization=none")
        if entry["match"] == "sha256" and (
            not isinstance(entry["pattern"], str) or sha256_pattern_digest(entry["pattern"]) is None
        ):
            errors.append(
                f"drift registry entry {entry_id} sha256 pattern must be 64 lowercase hex characters, "
                "optionally prefixed by sha256:"
            )
        if entry["severity"] not in DRIFT_SEVERITIES:
            errors.append(f"drift registry entry {entry_id} has invalid severity: {entry['severity']}")
        if not isinstance(entry["target_paths"], list) or not all(isinstance(item, str) for item in entry["target_paths"]):
            errors.append(f"drift registry entry {entry_id} target_paths must be a list of strings")
        if not isinstance(entry["allowed_absences"], list) or not all(
            isinstance(item, str) for item in entry["allowed_absences"]
        ):
            errors.append(f"drift registry entry {entry_id} allowed_absences must be a list of strings")
        if not isinstance(entry["blocking_wave"], int):
            errors.append(f"drift registry entry {entry_id} blocking_wave must be an int")
        if "pending" in entry and not isinstance(entry["pending"], str):
            errors.append(f"drift registry entry {entry_id} pending must be a string")
        if "git_ref" in entry and not isinstance(entry["git_ref"], str):
            errors.append(f"drift registry entry {entry_id} git_ref must be a string")
        entries.append(entry)
    return entries, errors


def pattern_matches(content: str | bytes, pattern: str, match_type: str, normalization: str) -> tuple[bool, str]:
    raw_content = content.encode("utf-8") if isinstance(content, str) else content
    if match_type == "sha256":
        if normalization != "none":
            return False, "sha256 match requires normalization=none"
        expected = sha256_pattern_digest(pattern)
        if expected is None:
            return False, "invalid sha256 pattern"
        actual = hashlib.sha256(raw_content).hexdigest()
        return actual == expected, f"sha256 mismatch expected={expected} actual={actual}"
    try:
        text = raw_content.decode("utf-8")
    except UnicodeDecodeError as exc:
        return False, f"unreadable text: {exc}"
    comparable_text = normalize_match_text(text, normalization)
    comparable_pattern = normalize_match_text(expand_shell_token(pattern, use_env=False), normalization)
    if comparable_pattern == "":
        return False, "empty pattern"
    if match_type == "literal":
        return comparable_pattern in comparable_text, "literal not found"
    try:
        found = re.search(comparable_pattern, comparable_text, flags=re.M | re.S) is not None
    except re.error as exc:
        return False, f"invalid regex: {exc}"
    return found, "regex not found"


def find_git_repo_root(path: Path) -> Path | None:
    """Find a containing repo without invoking git."""
    start = path if path.is_dir() else path.parent
    start = start.expanduser().resolve(strict=False)
    for candidate in [start, *start.parents]:
        if (candidate / ".git").exists():
            return candidate
    return None


def read_drift_target(
    target_path: Path,
    git_ref: str,
    *,
    require_git_ref: bool = False,
) -> tuple[bytes | None, bool, str, list[str], str | None]:
    """Read a drift target, optionally from a git ref.

    Returns exact bytes, exists, source, notes, error.
    """
    notes: list[str] = []
    if git_ref:
        repo_root = find_git_repo_root(target_path)
        if repo_root is None:
            if require_git_ref:
                return (
                    None,
                    True,
                    f"git_ref({git_ref})",
                    notes,
                    f"required git_ref source unavailable: no containing git repository for {target_path}",
                )
        else:
            try:
                rel = target_path.expanduser().resolve(strict=False).relative_to(repo_root.resolve(strict=False))
            except ValueError:
                rel = None
            if rel is None:
                if require_git_ref:
                    return (
                        None,
                        True,
                        f"git_ref({git_ref})",
                        notes,
                        f"required git_ref source unavailable: {target_path} is outside {repo_root}",
                    )
            else:
                try:
                    proc = subprocess.run(
                        ["git", "-C", str(repo_root), "show", f"{git_ref}:{rel.as_posix()}"],
                        capture_output=True,
                        check=False,
                        timeout=20,
                    )
                except (OSError, subprocess.TimeoutExpired) as exc:
                    if require_git_ref:
                        return (
                            None,
                            True,
                            f"git_ref({git_ref})",
                            notes,
                            f"required git_ref source unreadable: {exc}",
                        )
                    notes.append(f"git_ref fallback ref={git_ref} repo={repo_root} detail={exc}")
                else:
                    if proc.returncode == 0:
                        return proc.stdout, True, f"git_ref({git_ref})", notes, None
                    detail = (proc.stderr or proc.stdout or b"").strip().splitlines()
                    suffix = detail[0].decode("utf-8", errors="replace") if detail else f"exit {proc.returncode}"
                    if require_git_ref:
                        return (
                            None,
                            True,
                            f"git_ref({git_ref})",
                            notes,
                            f"required git_ref source unreadable: {suffix}",
                        )
                    notes.append(f"git_ref fallback ref={git_ref} repo={repo_root} detail={suffix}")

    if not target_path.exists():
        return None, False, "working_tree", notes, None
    try:
        return target_path.read_bytes(), True, "working_tree", notes, None
    except OSError as exc:
        return None, True, "working_tree", notes, f"unreadable bytes: {exc}"


def is_remote_tracking_ref(git_ref: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9._-]+/.+", git_ref))


def fetch_head_path(repo_root: Path) -> Path:
    git_path = repo_root / ".git"
    if git_path.is_dir():
        return git_path / "FETCH_HEAD"
    return git_path / "FETCH_HEAD"


def git_ref_freshness_note(repo_root: Path, git_ref: str) -> str | None:
    if is_remote_tracking_ref(git_ref):
        fetch_head = fetch_head_path(repo_root)
        try:
            age_hours = (time.time() - fetch_head.stat().st_mtime) / 3600
        except OSError:
            return None
        if age_hours <= 24:
            return None
        return f"NOTE git_ref freshness repo={repo_root} ref={git_ref} fetch_head_stale_hours={age_hours:.1f}"
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo_root), "rev-list", "--count", f"{git_ref}..{git_ref}@{{upstream}}"],
            text=True,
            capture_output=True,
            check=False,
            timeout=20,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0:
        return None
    try:
        behind_count = int(proc.stdout.strip())
    except ValueError:
        return None
    if behind_count <= 0:
        return None
    return f"NOTE git_ref freshness repo={repo_root} ref={git_ref} local_ref_behind_upstream_by={behind_count}"


def drift_freshness_notes(root: Path, entries: list[dict[str, object]]) -> list[str]:
    notes: list[str] = []
    seen: set[tuple[str, str]] = set()
    for entry in entries:
        git_ref = str(entry.get("git_ref") or "")
        if not git_ref:
            continue
        for raw_target in entry["target_paths"]:  # type: ignore[index]
            target_path = resolve_registry_path(root, str(raw_target))
            repo_root = find_git_repo_root(target_path)
            if repo_root is None:
                continue
            key = (str(repo_root), git_ref)
            if key in seen:
                continue
            seen.add(key)
            note = git_ref_freshness_note(repo_root, git_ref)
            if note:
                notes.append(note)
    return notes


def check_doctrine_drift(root: Path, *, registry_path: Path | None = None) -> CheckReport:
    """Report doctrine fingerprint drift; only adoption_state=blocking fails strict mode."""
    registry = registry_path or (root / DRIFT_REGISTRY)
    entries, errors = load_drift_registry(registry)
    lines = [f"DOCTRINE DRIFT REPORT registry={registry}"]
    blocking_failures: list[str] = []
    if errors:
        return CheckReport(lines, [], errors)
    lines.extend(drift_freshness_notes(root, entries))

    for entry in entries:
        entry_id = str(entry["id"])
        adoption_state = str(entry["adoption_state"])
        severity = str(entry["severity"])
        blocking_wave = entry["blocking_wave"]
        pending = str(entry.get("pending") or "")
        git_ref = str(entry.get("git_ref") or "")
        match_type = str(entry["match"])
        allowed_absences = set(entry["allowed_absences"])  # type: ignore[arg-type]
        target_paths = entry["target_paths"]  # type: ignore[assignment]
        for raw_target in target_paths:
            target_path = resolve_registry_path(root, raw_target)
            detail_prefix = (
                f"id={entry_id} target={raw_target} adoption_state={adoption_state} "
                f"severity={severity} blocking_wave={blocking_wave}"
            )
            content, target_exists, source, notes, read_error = read_drift_target(
                target_path,
                git_ref,
                require_git_ref=adoption_state == "blocking" and match_type == "sha256" and bool(git_ref),
            )
            for note in notes:
                lines.append(f"NOTE {detail_prefix} {note}")
            if not target_exists:
                allowed = raw_target in allowed_absences
                status = "ABSENT(allowed)" if allowed else "ABSENT(not)"
                detail = f"{status} {detail_prefix} resolved={target_path}"
                if pending:
                    detail += f" pending={pending}"
                lines.append(detail)
                if adoption_state == "blocking" and not allowed:
                    blocking_failures.append(detail)
                continue
            if read_error is not None or content is None:
                detail = f"DIVERGED {detail_prefix} source={source} detail={read_error or 'unreadable content'}"
                lines.append(detail)
                if adoption_state == "blocking":
                    blocking_failures.append(detail)
                continue

            matched, miss_detail = pattern_matches(
                content,
                str(entry["pattern"]),
                match_type,
                str(entry["normalization"]),
            )
            if matched:
                lines.append(f"MATCH {detail_prefix} source={source}")
            else:
                allowed = raw_target in allowed_absences and str(entry["pattern"]) == ""
                status = "ABSENT(allowed)" if allowed else "DIVERGED"
                detail = f"{status} {detail_prefix} source={source} detail={miss_detail}"
                if pending:
                    detail += f" pending={pending}"
                lines.append(detail)
                if adoption_state == "blocking" and not allowed:
                    blocking_failures.append(detail)
    return CheckReport(lines, blocking_failures, [])


def skills_root_from_env(kind: str) -> Path:
    specific = f"UBER_{kind.upper()}_SKILLS_ROOT"
    generic = f"{kind.upper()}_SKILLS_ROOT"
    value = os.environ.get(specific) or os.environ.get(generic)
    if value:
        return Path(value).expanduser()
    return Path.home() / f".{kind.lower()}" / "skills"


def allowed_install_extra(name: str) -> bool:
    return name in INSTALL_SYNC_IGNORED_EXTRAS or name.startswith(".") or name == "plugins" or name.startswith("plugins/")


def check_skill_install_sync(root: Path) -> CheckReport:
    """Report pack skill install sync. Strict failure starts at blocking_wave=2."""
    lines = ["SKILL INSTALL SYNC REPORT blocking_wave=2"]
    violations: list[str] = []
    errors: list[str] = []
    expected = set(PACK_SKILLS)

    for kind in ["claude", "codex"]:
        skills_root = skills_root_from_env(kind)
        if not skills_root.exists():
            detail = f"VIOLATION root={kind} path={skills_root} detail=skills root missing"
            lines.append(detail)
            violations.append(detail)
            continue
        for skill in PACK_SKILLS:
            install_path = skills_root / skill
            expected_target = (root / skill).resolve()
            prefix = f"root={kind} skill={skill} path={install_path}"
            if not install_path.exists() and not install_path.is_symlink():
                detail = f"VIOLATION {prefix} detail=missing symlink"
                lines.append(detail)
                violations.append(detail)
                continue
            if not install_path.is_symlink():
                detail = f"VIOLATION {prefix} detail=copy-or-directory install; symlink required"
                lines.append(detail)
                violations.append(detail)
                continue
            actual_target = install_path.resolve()
            if actual_target != expected_target:
                detail = f"VIOLATION {prefix} detail=wrong target actual={actual_target} expected={expected_target}"
                lines.append(detail)
                violations.append(detail)
                continue
            lines.append(f"MATCH {prefix} target={actual_target}")

        for child in sorted(skills_root.iterdir(), key=lambda item: item.name):
            if child.name in expected:
                continue
            if allowed_install_extra(child.name):
                lines.append(f"EXTRA_ALLOWED root={kind} name={child.name}")
            else:
                lines.append(f"WARN root={kind} name={child.name} detail=unknown extra skill entry")
    return CheckReport(lines, violations, errors)


def secret_scan_base_files(root: Path) -> list[Path]:
    files = set(doctrine_text_files(root))
    for dirname in SECRET_SCAN_DIRS:
        base = root / dirname
        if base.exists():
            files.update(path for path in base.rglob("*") if path.is_file() and path.suffix in SECRET_SCAN_SUFFIXES)
    return sorted(files)


def explicit_scan_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        expanded = path.expanduser()
        if expanded.is_dir():
            files.extend(item for item in expanded.rglob("*") if item.is_file())
        elif expanded.exists():
            files.append(expanded)
    return sorted(set(files))


def strip_safe_secret_refs(line: str) -> str:
    return re.sub(r"op://[^\s`'\"<>),]+", "op://", line)


def shannon_entropy(value: str) -> float:
    if not value:
        return 0.0
    total = len(value)
    counts = {char: value.count(char) for char in set(value)}
    return -sum((count / total) * math.log2(count / total) for count in counts.values())


def inside_backticks(line: str, start: int) -> bool:
    return line[:start].count("`") % 2 == 1


def preceded_by_commit(line: str, start: int) -> bool:
    prefix = line[max(0, start - 24) : start]
    return re.search(r"\bcommit\s+$", prefix, flags=re.I) is not None


def preceded_by_sha256(line: str, start: int) -> bool:
    prefix = line[max(0, start - 16) : start]
    return re.search(r"\bsha-?256:$", prefix, flags=re.I) is not None


def allowed_hex_reference(line: str, match: re.Match[str]) -> bool:
    value = match.group(0)
    if len(value) == 64:
        return inside_backticks(line, match.start()) or preceded_by_sha256(line, match.start())
    if len(value) != 40:
        return False
    return inside_backticks(line, match.start()) or preceded_by_commit(line, match.start())


def pattern_hits(name: str, pattern: re.Pattern[str], line: str) -> bool:
    for match in pattern.finditer(line):
        if name == "hex_32" and allowed_hex_reference(line, match):
            continue
        if name == "base64_32" and shannon_entropy(match.group(0)) < 4.2:
            continue
        return True
    return False


def check_secret_scan(root: Path, *, extra_paths: list[Path] | None = None) -> CheckReport:
    """Report likely credential literals in doctrine, coordination, and eval artifacts.

    This check is report-only by default; `--strict` makes violations blocking.
    Adoption state: blocking_wave=2. Test fixtures under `tests/fixtures` are
    outside the default scan path so fake tokens never exempt themselves by
    content.
    """
    lines = ["SECRET SCAN REPORT blocking_wave=2 default=report_only"]
    violations: list[str] = []
    errors: list[str] = []
    files = secret_scan_base_files(root)
    if extra_paths:
        files.extend(explicit_scan_files(extra_paths))
    for path in sorted(set(files)):
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        try:
            rel = path.relative_to(root)
        except ValueError:
            rel = path
        for line_no, line in enumerate(text.splitlines(), start=1):
            sanitized = strip_safe_secret_refs(line)
            for name, pattern in SECRET_TOKEN_PATTERNS:
                if pattern_hits(name, pattern, sanitized):
                    detail = f"SECRET_CANDIDATE path={rel}:{line_no} kind={name}"
                    lines.append(detail)
                    violations.append(detail)
                    break
    if not violations:
        lines.append("PASS no likely credential literals found")
    return CheckReport(lines, violations, errors)


def policy_value(root: Path, skill: str) -> str | None:
    path = root / skill / "agents" / "openai.yaml"
    if not path.exists():
        return None
    match = re.search(r"^\s*allow_implicit_invocation:\s*(true|false)\s*$", path.read_text(), flags=re.M)
    return match.group(1) if match else None


def install_loop_skills(readme: str, heading: str) -> set[str]:
    pattern = rf"### {re.escape(heading)}.*?for s in ([^;]+); do"
    match = re.search(pattern, readme, flags=re.S)
    if not match:
        return set()
    return set(match.group(1).split())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--drift", action="store_true", help="run only the doctrine drift report")
    parser.add_argument("--install-sync", action="store_true", help="run only the local skill install-sync report")
    parser.add_argument("--secret-scan", action="store_true", help="run only the report-only secret scan")
    parser.add_argument("--secret-scan-path", action="append", type=Path, default=[], help="extra file/dir to scan for secret-scan tests")
    parser.add_argument("--dispatch-preflight", type=Path, nargs="?", const=DEFAULT_ROOT, default=None, help="run only the dispatch writeability preflight for a repo root")
    parser.add_argument("--strict", action="store_true", help="fail focused reports on blocking violations")
    parser.add_argument("--drift-registry", type=Path, default=None, help="override doctrine drift registry path")
    args = parser.parse_args()
    root = args.root.resolve()

    if args.drift or args.install_sync or args.secret_scan or args.dispatch_preflight is not None:
        reports: list[CheckReport] = []
        if args.drift:
            reports.append(check_doctrine_drift(root, registry_path=args.drift_registry))
        if args.install_sync:
            reports.append(check_skill_install_sync(root))
        if args.secret_scan:
            reports.append(check_secret_scan(root, extra_paths=args.secret_scan_path))
        if args.dispatch_preflight is not None:
            reports.append(check_dispatch_preflight(args.dispatch_preflight))
        exit_code = 0
        for report in reports:
            report.print()
            exit_code = max(exit_code, report.exit_code(args.strict))
        return exit_code

    errors: list[str] = []

    for rel in ROOT_REQUIRED_FILES:
        if not (root / rel).exists():
            errors.append(f"missing root contract file: {rel}")

    validate_frontmatter_policy(root, errors)
    validate_skill_word_budgets(root, errors)

    implicit = {skill: policy_value(root, skill) for skill in ["ubergoal", *UBER_PHASE_SKILLS]}
    if implicit.get("ubergoal") != "true":
        errors.append("ubergoal must be the only implicit/default Uber router")
    for skill in UBER_PHASE_SKILLS:
        if implicit.get(skill) != "true":
            errors.append(f"{skill} must be exposed to Codex sessions with allow_implicit_invocation: true")
    for skill in UTILITY_IMPLICIT_SKILLS:
        if policy_value(root, skill) != "true":
            errors.append(f"{skill} utility metadata must allow task-specific implicit invocation")

    for skill in UBER_PHASE_SKILLS:
        skill_text = read(root / skill / "SKILL.md")
        meta = read(root / skill / "agents" / "openai.yaml")
        if skill == "uberassess":
            if "Do not auto-trigger from task similarity" not in skill_text or "routed by `ubergoal`" not in skill_text:
                errors.append("uberassess SKILL.md must state direct-use/routed-only policy")
            if "only when explicitly invoked" not in meta or "routed by $ubergoal" not in meta:
                errors.append("uberassess metadata must state explicit-or-routed invocation")
        else:
            if "Do not auto-trigger from task similarity" not in skill_text or "Use only when explicitly named" not in skill_text:
                errors.append(f"{skill} SKILL.md must state direct-use/routed-only policy")
            if "only when explicitly invoked or routed by $ubergoal" not in meta:
                errors.append(f"{skill} metadata must state explicit-or-routed invocation")

    deep = read(root / "uberrca" / "SKILL.md")
    deep_meta = read(root / "uberrca" / "agents" / "openai.yaml")
    deep_evals = root / "uberrca" / "evals" / "golden_skill_invocations.json"
    deep_lint = root / "uberrca" / "scripts" / "lint_skill_package.py"
    if "self-challenge loop" not in deep or "lowest enforceable layer" not in deep:
        errors.append("uberrca must keep RCA depth and durable-fix doctrine")
    if "$uberarchitect" not in deep or "Architecture stepback route" not in deep:
        errors.append("uberrca must route system-shape RCA to uberarchitect")
    if "$uberrca" not in deep_meta or "proximate cause" not in deep_meta:
        errors.append("uberrca metadata must describe proximate-cause RCA trigger")
    if not deep_evals.exists() or not deep_lint.exists():
        errors.append("uberrca must keep golden evals and package lint")
    if (root / "uberrca" / "README.md").exists():
        errors.append("uberrca must not carry package-local README.md")

    agents = read(root / "AGENTS.md")
    for phrase in AGENTS_REQUIRED_PHRASES:
        if phrase not in agents:
            errors.append(f"AGENTS.md missing phrase: {phrase}")

    claude = read(root / "CLAUDE.md")
    if "AGENTS.md" not in claude or "$ubergoal` is the default router" not in claude:
        errors.append("CLAUDE.md must defer to AGENTS.md and name ubergoal as default router")

    readme = read(root / "README.md")
    for phrase in README_REQUIRED_PHRASES:
        if phrase not in readme:
            errors.append(f"README.md missing phrase: {phrase}")
    for heading in ["Generic install", "Codex-compatible install", "Claude Code-compatible install"]:
        skills = install_loop_skills(readme, heading)
        if skills != set(PACK_SKILLS):
            errors.append(f"{heading} loop should include exactly {', '.join(PACK_SKILLS)}; found {sorted(skills)}")

    active_review_policy_paths = [
        root / "AGENTS.md",
        root / "README.md",
        root / "evals" / "routing" / "answer-key.md",
        root / "ubergoal" / "SKILL.md",
        root / "uberplan" / "SKILL.md",
        root / "uberassess" / "SKILL.md",
        root / "uberrca" / "SKILL.md",
        root / "uberaccept" / "SKILL.md",
        root / "uberplan" / "templates" / "plan-tier3.md",
        root / "references" / "claude-adversary.md",
    ]
    for policy_path in active_review_policy_paths:
        policy_text = read(policy_path)
        for pattern in FORBIDDEN_AUTOMATIC_CLAUDE_PATTERNS:
            if re.search(pattern, policy_text, flags=re.IGNORECASE):
                errors.append(
                    "active review policy restores forbidden automatic Claude default: "
                    f"{policy_path.relative_to(root)} matches /{pattern}/i"
                )

    routing_answer_key = read(root / "evals" / "routing" / "answer-key.md")
    for phrase in ROUTING_ANSWER_KEY_REQUIRED_PHRASES:
        if phrase not in routing_answer_key:
            errors.append(f"evals/routing/answer-key.md missing phrase: {phrase}")

    roadmap = read(root / "ROADMAP.md")
    for phrase in ROADMAP_REQUIRED_PHRASES:
        if phrase not in roadmap:
            errors.append(f"ROADMAP.md missing phrase: {phrase}")

    validate_portability_oracle(root, errors)
    drift_report = check_doctrine_drift(root, registry_path=args.drift_registry)
    install_sync_report = check_skill_install_sync(root)
    secret_report = check_secret_scan(root)
    drift_report.print()
    install_sync_report.print()
    secret_report.print()
    errors.extend(f"doctrine drift: {error}" for error in drift_report.errors)
    errors.extend(f"install sync: {error}" for error in install_sync_report.errors)
    errors.extend(f"secret scan: {error}" for error in secret_report.errors)
    if args.strict:
        errors.extend(f"doctrine drift: {failure}" for failure in drift_report.blocking_failures)
        errors.extend(f"install sync: {failure}" for failure in install_sync_report.blocking_failures)
        errors.extend(f"secret scan: {failure}" for failure in secret_report.blocking_failures)

    if errors:
        for error in sorted(set(errors)):
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"PASS: pack contract lint passed for {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
