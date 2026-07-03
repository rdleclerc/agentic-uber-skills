#!/usr/bin/env python3
"""Validate failure-eval case files.

This standalone CLI is intentionally separate from the pack-contract aggregator
because Gaia's test suite invokes it cross-repo via
`${UBER_SKILLS_ROOT:-~/repos/agentic-uber-skills}/scripts/validate_failure_case.py`.
That cross-repo call path is the fixture-backed need that justifies a new CLI
under amendment J.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_FIELDS = [
    "id",
    "date_observed",
    "layer",
    "canonical_layer",
    "title",
    "what_happened",
    "failure_class",
    "cost",
    "gate_that_missed_it",
    "eval_check",
    "eval_type",
    "plan_items",
    "status",
]
OPTIONAL_FIELDS = {"canonical_repo", "canonical_pointer", "notes"}
LAYERS = {"process", "runtime", "both"}
CANONICAL_LAYERS = {"process", "runtime"}
EVAL_TYPES = {"executable", "fixture", "checklist", "live"}
STATUSES = {"seed", "eval_built", "enforced"}
PLACEHOLDERS = {"", "todo", "tbd", "n/a", "none", "yes/no"}
CASE_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
USER_PATH_RE = re.compile(r"/Users/[^/\s`'\"<>),]+/[^\s`'\"<>),]*")
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)(.*)\Z", re.S)
INDEX_LINE_RE = re.compile(
    r"^\s*-\s+(?P<id>[a-z0-9]+(?:-[a-z0-9]+)*)\s+·\s+"
    r"(?P<layer>[a-z]+)\((?P<canonical_layer>[a-z]+)\)\s+·\s+"
    r"(?P<status>[a-z_]+)\s+·\s+"
    r"(?:date:\s+(?P<date>\d{4}-\d{2}-\d{2})\s+·\s+)?"
    r"canonical:\s+(?P<canonical>.+?)\s*$"
)
REPO_CANONICAL_DIRS = {
    "agfunder-gaia/evals/failures/",
    "agentic-uber-skills/evals/failures/",
}


def normalize(value: object) -> str:
    if isinstance(value, list):
        return ", ".join(str(item).strip() for item in value)
    return str(value).strip()


def parse_scalar(raw: str) -> str:
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, object], str, list[str]]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text, ["missing YAML frontmatter"]
    raw, body = match.group(1), match.group(2)
    data: dict[str, object] = {}
    errors: list[str] = []
    current_key: str | None = None
    for line_no, line in enumerate(raw.splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - ") or line.startswith("- "):
            if current_key is None:
                errors.append(f"frontmatter line {line_no}: list item without key")
                continue
            existing = data.setdefault(current_key, [])
            if not isinstance(existing, list):
                errors.append(f"frontmatter line {line_no}: mixed scalar/list for {current_key}")
                continue
            existing.append(parse_scalar(line.split("- ", 1)[1]))
            continue
        match_key = re.match(r"^([A-Za-z0-9_]+):(?:\s*(.*))?$", line)
        if not match_key:
            errors.append(f"frontmatter line {line_no}: unsupported YAML syntax")
            current_key = None
            continue
        key, value = match_key.group(1), match_key.group(2) or ""
        current_key = key
        if value == "":
            data[key] = []
        else:
            data[key] = parse_scalar(value)
    return data, body, errors


def nonempty(data: dict[str, object], field: str) -> bool:
    value = data.get(field)
    if isinstance(value, list):
        return bool(value) and all(normalize(item).lower() not in PLACEHOLDERS for item in value)
    return normalize(value or "").lower() not in PLACEHOLDERS


def parameterized_default_spans(line: str) -> list[tuple[int, int]]:
    return [(span.start(), span.end()) for span in re.finditer(r"\$\{[^}\n]*:-[^}\n]*\}", line)]


def range_inside_spans(match_start: int, match_end: int, spans: list[tuple[int, int]]) -> bool:
    return any(start <= match_start and match_end <= end for start, end in spans)


def has_parameterized_user_path(text: str, match: re.Match[str]) -> bool:
    line_start = text.rfind("\n", 0, match.start()) + 1
    line_end = text.find("\n", match.end())
    if line_end == -1:
        line_end = len(text)
    line = text[line_start:line_end]
    local_start = match.start() - line_start
    local_end = match.end() - line_start
    return match.group(0).startswith("~/") or range_inside_spans(local_start, local_end, parameterized_default_spans(line))


def expected_canonical_repo(layer: str) -> str:
    if layer == "runtime":
        return "agfunder-gaia/evals/failures/"
    return "agentic-uber-skills/evals/failures/"


def validate_file(path: Path) -> list[str]:
    try:
        text = path.read_text()
    except OSError as exc:
        return [f"{path}: cannot read case file: {exc}"]
    except UnicodeDecodeError as exc:
        return [f"{path}: not UTF-8 text: {exc}"]
    data, body, errors = parse_frontmatter(text)
    prefix = str(path)
    unknown = sorted(set(data) - set(REQUIRED_FIELDS) - OPTIONAL_FIELDS)
    for field in unknown:
        errors.append(f"unknown field: {field}")
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"missing required field: {field}")
        elif not nonempty(data, field):
            errors.append(f"empty or placeholder field: {field}")

    case_id = normalize(data.get("id", ""))
    if case_id and not CASE_ID_RE.fullmatch(case_id):
        errors.append(f"invalid id: {case_id}")
    if path.name != f"{case_id}.md" and case_id:
        errors.append(f"filename must match id: expected {case_id}.md")
    date = normalize(data.get("date_observed", ""))
    if date and not DATE_RE.fullmatch(date):
        errors.append(f"date_observed must be YYYY-MM-DD: {date}")
    layer = normalize(data.get("layer", ""))
    canonical_layer = normalize(data.get("canonical_layer", ""))
    if layer and layer not in LAYERS:
        errors.append(f"invalid layer: {layer}")
    if canonical_layer and canonical_layer not in CANONICAL_LAYERS:
        errors.append(f"invalid canonical_layer: {canonical_layer}")
    if layer in {"process", "runtime"} and canonical_layer and canonical_layer != layer:
        errors.append(f"canonical_layer must equal layer for non-both cases: layer={layer} canonical_layer={canonical_layer}")
    if normalize(data.get("eval_type", "")) not in EVAL_TYPES and "eval_type" in data:
        errors.append(f"invalid eval_type: {normalize(data.get('eval_type', ''))}")
    if normalize(data.get("status", "")) not in STATUSES and "status" in data:
        errors.append(f"invalid status: {normalize(data.get('status', ''))}")
    if not isinstance(data.get("plan_items"), list) or not data.get("plan_items"):
        errors.append("plan_items must be a non-empty YAML list")

    for field in ["title", "what_happened", "cost"]:
        value = normalize(data.get(field, ""))
        for match in USER_PATH_RE.finditer(value):
            if not has_parameterized_user_path(value, match):
                errors.append(f"{field} contains unsanitized user path: {match.group(0)}")
    for match in USER_PATH_RE.finditer(body):
        if not has_parameterized_user_path(body, match):
            errors.append(f"body contains unsanitized user path: {match.group(0)}")

    is_pointer = (
        normalize(data.get("canonical_pointer", "")).lower() in {"true", "yes"}
        or "pointer" in body.lower()
        or "canonical:" in body.lower()
    )
    if is_pointer and canonical_layer:
        expected = expected_canonical_repo(canonical_layer)
        combined = f"{normalize(data.get('canonical_repo', ''))}\n{body}"
        if expected not in combined:
            errors.append(f"pointer file must name canonical repo path: {expected}")

    return [f"{prefix}: {error}" for error in errors]


def iter_case_files(target: Path) -> list[Path]:
    if target.is_dir():
        return sorted(path for path in target.glob("*.md") if path.name != "README.md")
    return [target]


def parse_case_metadata(path: Path) -> tuple[dict[str, object], list[str]]:
    try:
        text = path.read_text()
    except OSError as exc:
        return {}, [f"{path}: cannot read case file: {exc}"]
    except UnicodeDecodeError as exc:
        return {}, [f"{path}: not UTF-8 text: {exc}"]
    data, _body, parse_errors = parse_frontmatter(text)
    return data, [f"{path}: {error}" for error in parse_errors]


def is_local_canonical(canonical: str) -> bool:
    return canonical.startswith("evals/failures/cases/")


def canonical_repo_dir_for_cases(cases_dir: Path) -> str | None:
    parts = cases_dir.expanduser().resolve(strict=False).parts
    for repo in ("agfunder-gaia", "agentic-uber-skills"):
        for index, part in enumerate(parts):
            if part != repo:
                continue
            if tuple(parts[index + 1 : index + 4]) == ("evals", "failures", "cases"):
                return f"{repo}/evals/failures/"
    return None


def is_local_index_entry(canonical: str, cases_dir: Path, case_id: str = "", file_ids: set[str] | None = None) -> bool:
    repo_dir = canonical_repo_dir_for_cases(cases_dir)
    if is_local_canonical(canonical):
        return True
    if canonical not in REPO_CANONICAL_DIRS:
        return False
    if repo_dir:
        return canonical == repo_dir
    return bool(file_ids is not None and case_id in file_ids)


def parse_index(index_path: Path) -> tuple[dict[str, dict[str, str]], list[str]]:
    try:
        lines = index_path.read_text().splitlines()
    except OSError as exc:
        return {}, [f"{index_path}: cannot read index: {exc}"]
    entries: dict[str, dict[str, str]] = {}
    errors: list[str] = []
    for line_no, line in enumerate(lines, start=1):
        if not line.lstrip().startswith("- "):
            continue
        match = INDEX_LINE_RE.match(line)
        if not match:
            errors.append(f"{index_path}:{line_no}: malformed index line")
            continue
        case_id = match.group("id")
        if case_id in entries:
            errors.append(f"{index_path}:{line_no}: duplicate case id: {case_id}")
            continue
        entries[case_id] = match.groupdict()
        observed = entries[case_id].get("date")
        if observed and not DATE_RE.fullmatch(observed):
            errors.append(f"{index_path}:{line_no}: invalid date segment: {observed}")
    return entries, errors


def validate_index(index_path: Path, cases_dir: Path) -> list[str]:
    entries, errors = parse_index(index_path)
    if not entries:
        errors.append(f"{index_path}: no index entries found")
    files = iter_case_files(cases_dir)
    case_by_id: dict[str, tuple[Path, dict[str, object]]] = {}
    for path in files:
        data, parse_errors = parse_case_metadata(path)
        errors.extend(parse_errors)
        case_id = normalize(data.get("id", ""))
        if not case_id:
            errors.append(f"{path}: missing id for index consistency")
            continue
        if case_id in case_by_id:
            errors.append(f"{path}: duplicate case id also found at {case_by_id[case_id][0]}")
            continue
        case_by_id[case_id] = (path, data)

    file_ids = set(case_by_id)
    local_index_ids = {
        case_id
        for case_id, entry in entries.items()
        if is_local_index_entry(entry["canonical"], cases_dir, case_id, file_ids)
    }
    missing_from_index = sorted(file_ids - local_index_ids)
    missing_files = sorted(local_index_ids - file_ids)
    for case_id in missing_from_index:
        errors.append(f"{index_path}: case file missing from local index: {case_id}")
    for case_id in missing_files:
        errors.append(f"{index_path}: local index id has no case file: {case_id}")

    for case_id, entry in entries.items():
        if not CASE_ID_RE.fullmatch(case_id):
            errors.append(f"{index_path}: invalid index id: {case_id}")
        canonical = entry["canonical"]
        if is_local_index_entry(canonical, cases_dir, case_id, file_ids):
            if is_local_canonical(canonical) and canonical != f"evals/failures/cases/{case_id}.md":
                errors.append(f"{index_path}: local canonical path mismatch for {case_id}: {entry['canonical']}")
            if case_id not in case_by_id:
                continue
            path, data = case_by_id[case_id]
            status = normalize(data.get("status", ""))
            if entry["status"] != status:
                errors.append(f"{index_path}: status mismatch for {case_id}: index={entry['status']} case={status} ({path})")
        elif canonical not in REPO_CANONICAL_DIRS:
            errors.append(f"{index_path}: unsupported canonical path for {case_id}: {canonical}")
    return errors


def validate_cross_index(index_path: Path, other_index_path: Path) -> list[str]:
    left, errors = parse_index(index_path)
    right, right_errors = parse_index(other_index_path)
    errors.extend(right_errors)
    if not left:
        errors.append(f"{index_path}: no index entries found")
    if not right:
        errors.append(f"{other_index_path}: no index entries found")
    shared = sorted(set(left) & set(right))
    if not shared:
        errors.append(f"{index_path}: no shared ids with {other_index_path}")
        return errors
    for case_id in shared:
        left_status = left[case_id]["status"]
        right_status = right[case_id]["status"]
        if left_status != right_status:
            errors.append(
                f"shared-id status mismatch for {case_id}: "
                f"{index_path}={left_status} {other_index_path}={right_status}"
            )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", type=Path, help="case file or directory of case files")
    parser.add_argument("--index", type=Path, default=None, help="INDEX.md to check against a local cases directory")
    parser.add_argument("--cases", type=Path, default=None, help="case directory for --index mode")
    parser.add_argument("--cross-index", type=Path, default=None, help="other INDEX.md to compare shared-id statuses against")
    args = parser.parse_args()
    if args.cross_index:
        if not args.index:
            parser.error("--cross-index requires --index")
        errors = validate_cross_index(args.index, args.cross_index)
        if errors:
            print("FAIL: failure case cross-index validation failed", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 1
        print(f"PASS: shared-id statuses match between {args.index} and {args.cross_index}")
        return 0
    if args.index or args.cases:
        if not args.index or not args.cases:
            parser.error("--index and --cases must be provided together")
        errors = validate_index(args.index, args.cases)
        if errors:
            print("FAIL: failure case index validation failed", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 1
        print(f"PASS: index {args.index} matches cases in {args.cases}")
        return 0
    if args.target is None:
        parser.error("target is required unless --index --cases is used")
    files = iter_case_files(args.target)
    errors: list[str] = []
    if not files:
        errors.append(f"{args.target}: no case files found")
    for path in files:
        errors.extend(validate_file(path))
    if errors:
        print("FAIL: failure case validation failed", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"PASS: validated {len(files)} failure case file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
