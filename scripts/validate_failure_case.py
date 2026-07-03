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
PLACEHOLDERS = {"", "todo", "tbd", "n/a", "yes/no"}
CASE_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
USER_PATH_RE = re.compile(r"/Users/[^/\s`'\"<>),]+/[^\s`'\"<>),]*")
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)(.*)\Z", re.S)


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


def has_parameterized_user_path(text: str, match: re.Match[str]) -> bool:
    line_start = text.rfind("\n", 0, match.start()) + 1
    line_end = text.find("\n", match.end())
    if line_end == -1:
        line_end = len(text)
    line = text[line_start:line_end]
    return "${" in line or "~/" in line or "<name>" in line or "<user>" in line


def expected_canonical_repo(layer: str) -> str:
    if layer == "runtime":
        return "agfunder-gaia/evals/failures/"
    return "agentic-uber-skills/evals/failures/"


def validate_file(path: Path) -> list[str]:
    try:
        text = path.read_text()
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

    what_happened = normalize(data.get("what_happened", ""))
    for match in USER_PATH_RE.finditer(what_happened):
        if not has_parameterized_user_path(what_happened, match):
            errors.append(f"what_happened contains unsanitized user path: {match.group(0)}")

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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="case file or directory of case files")
    args = parser.parse_args()
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
