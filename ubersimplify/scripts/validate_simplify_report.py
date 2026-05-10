#!/usr/bin/env python3
"""Validate a completed ubersimplify final report.

This validator is intentionally conservative for Patch mode. It cannot prove
semantic safety, but it should block reports that merely look complete while
missing authorization, tests, dynamic-reference proof, or rollback detail.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

REQUIRED_SECTIONS = [
    "Run metadata",
    "Summary",
    "Complexity reduced or candidates found",
    "Modularity / fail-fast findings",
    "Dead-code findings",
    "Test confidence and evidence",
    "Safety gates",
    "Patch evidence",
    "Uberskillevolver handoff",
    "Final verdict",
]

REQUIRED_GATE_PHRASES = [
    "Chesterton gate passed?",
    "Evidence gate passed?",
    "Rollback gate passed?",
    "Dynamic-reference safeguards checked?",
    "Benefit >> cost demonstrated?",
]

VALID_MODES = {"audit", "plan", "patch"}
EMPTY_VALUES = {
    "",
    "-",
    "none",
    "none.",
    "n/a",
    "na",
    "not applicable",
    "todo",
    "tbd",
    "missing",
    "unknown",
}
BAD_PATCH_EVIDENCE_PATTERNS = [
    r"\bvibes?\b",
    r"\bgrep[- ]only\b",
    r"\bnone run\b",
    r"\bnot tested\b",
    r"\bno tests?\b",
    r"\buntested\b",
    r"\brevert somehow\b",
    r"\bhope it works\b",
]
DYNAMIC_DETAIL_TERMS = [
    "import",
    "entrypoint",
    "route",
    "config",
    "prompt",
    "tool",
    "external",
    "registry",
    "migration",
    "ci",
    "cron",
    "launchd",
    "docs",
    "installed",
    "consumer",
]
COMMAND_HINTS = [
    "python",
    "pytest",
    "unittest",
    "npm",
    "pnpm",
    "yarn",
    "uv",
    "ruff",
    "mypy",
    "lint",
    "test",
    "validate",
    "playwright",
    "browser",
    "eval",
    "rg ",
    "grep",
]
RESULT_HINTS = ["pass", "passed", "ok", "success", "green", "0 failures", "no failures"]


def section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\s*$", text, flags=re.MULTILINE)
    if not match:
        return ""
    start = match.end()
    next_match = re.search(r"^## ", text[start:], flags=re.MULTILINE)
    end = start + next_match.start() if next_match else len(text)
    return text[start:end].strip()


def has_substance(body: str) -> bool:
    for line in body.splitlines():
        s = line.strip()
        if not s or s in {"-", "|---|---|---|", "|---|---|---|---|"}:
            continue
        if re.fullmatch(r"\|[\s|:-]+\|", s):
            continue
        if re.search(r"\b(TODO|TBD)\b", s, flags=re.I):
            continue
        return True
    return False


def field(text: str, label: str) -> str:
    m = re.search(rf"^[ \t]*-[ \t]*{re.escape(label)}\s*(.*?)\s*$", text, flags=re.M | re.I)
    return m.group(1).strip() if m else ""


def gate_line(gates: str, label: str) -> str:
    m = re.search(rf"^[ \t]*-[ \t]*{re.escape(label)}\s*(.*?)\s*$", gates, flags=re.M | re.I)
    return m.group(1).strip() if m else ""


def normalized_mode(run_metadata: str) -> str:
    mode = field(run_metadata, "Mode:").strip().lower()
    return re.split(r"\s+|\|", mode)[0] if mode else ""


def is_emptyish(value: str) -> bool:
    value = value.strip().strip(".").lower()
    return value in EMPTY_VALUES


def has_bad_patch_phrase(value: str) -> bool:
    return any(re.search(pattern, value, flags=re.I) for pattern in BAD_PATCH_EVIDENCE_PATTERNS)


def evidence_has_concrete_command(value: str) -> bool:
    lower = value.lower()
    return any(hint in lower for hint in COMMAND_HINTS) and any(hint in lower for hint in RESULT_HINTS)


def confidence_rows(evidence: str) -> list[tuple[str, str, str, str]]:
    rows: list[tuple[str, str, str, str]] = []
    for line in evidence.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip().lower() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 4 or cells[0] in {"---", "layer"}:
            continue
        rows.append(tuple(cells[:4]))
    return rows


def validate_ready_verdict(verdict: str, errors: list[str]) -> str:
    ready = field(verdict, "Ready to accept?").strip().lower()
    blockers = field(verdict, "Material blockers:").strip().lower()
    if ready not in {"yes", "no"}:
        errors.append("final verdict Ready to accept? must be exactly yes or no")
    if ready == "yes" and blockers not in {"none", "no", "none."}:
        errors.append("ready=yes requires Material blockers: none")
    return ready


def validate_patch_mode(text: str, errors: list[str]) -> None:
    patch = section(text, "Patch evidence")
    gates = section(text, "Safety gates")
    evidence = section(text, "Test confidence and evidence")

    authorization = field(patch, "Patch authorization:")
    changed = field(patch, "Files changed:")
    checks = field(patch, "Tests/evals/static checks after patch:")
    rollback = field(patch, "Rollback plan:")

    if is_emptyish(authorization) or re.search(r"not authorized|no authorization|without authorization", authorization, flags=re.I):
        errors.append("patch mode requires explicit Patch authorization")
    if is_emptyish(changed):
        errors.append("patch mode requires non-empty Files changed")
    if is_emptyish(checks) or has_bad_patch_phrase(checks) or not evidence_has_concrete_command(checks):
        errors.append("patch mode requires concrete post-patch test/eval/static command with passing result")
    if is_emptyish(rollback) or has_bad_patch_phrase(rollback) or len(rollback) < 20:
        errors.append("patch mode requires concrete rollback/backout plan")

    dynamic = gate_line(gates, "Dynamic-reference safeguards checked?")
    dynamic_lower = dynamic.lower()
    if not dynamic_lower.startswith("yes"):
        errors.append("patch mode requires Dynamic-reference safeguards checked? yes with details")
    if len(dynamic) < 25 or not any(term in dynamic_lower for term in DYNAMIC_DETAIL_TERMS):
        errors.append("patch mode requires dynamic-reference safeguard details, not a bare yes")

    rows = confidence_rows(evidence)
    if not rows:
        errors.append("patch mode requires parseable test-confidence rows")
    weak_rows = [row for row in rows if row[3] in {"weak", "unknown"}]
    if weak_rows:
        errors.append("patch mode cannot accept weak/unknown confidence rows for touched behavior")

    patch_text = patch.lower()
    for label, value in [
        ("Patch authorization", authorization),
        ("Files changed", changed),
        ("Tests/evals/static checks after patch", checks),
        ("Rollback plan", rollback),
    ]:
        if has_bad_patch_phrase(value):
            errors.append(f"patch mode has vague/unsafe {label} evidence")
    if "grep only" in text.lower() and "dynamic" not in text.lower():
        errors.append("grep-only deletion evidence requires dynamic-reference proof")


def validate(path: Path, allow_template: bool = False) -> list[str]:
    text = path.read_text()
    errors: list[str] = []
    for heading in REQUIRED_SECTIONS:
        if f"## {heading}" not in text:
            errors.append(f"missing required section: {heading}")
    for phrase in REQUIRED_GATE_PHRASES:
        if phrase not in text:
            errors.append(f"missing safety gate phrase: {phrase}")
    if allow_template:
        return errors

    for heading in REQUIRED_SECTIONS:
        body = section(text, heading)
        if not has_substance(body):
            errors.append(f"section lacks completed substance: {heading}")

    run_metadata = section(text, "Run metadata")
    mode = normalized_mode(run_metadata)
    if mode not in VALID_MODES:
        errors.append("Run metadata Mode must be one of audit, plan, or patch")

    gates = section(text, "Safety gates").lower()
    for gate in ["chesterton", "evidence", "rollback", "dynamic-reference", "benefit >> cost"]:
        if gate not in gates:
            errors.append(f"safety gate missing in completed report: {gate}")

    verdict = section(text, "Final verdict")
    ready = validate_ready_verdict(verdict, errors)

    if "uberskillevolver" not in section(text, "Uberskillevolver handoff").lower():
        errors.append("handoff must mention uberskillevolver")

    evidence = section(text, "Test confidence and evidence").lower()
    if not any(term in evidence for term in ["pass", "passed", "not applicable", "audit only", "n/a"]):
        errors.append("test confidence/evidence must include pass, not applicable, or audit-only rationale")

    if mode == "patch":
        validate_patch_mode(text, errors)
        residual = field(verdict, "Residual risks:").lower()
        if ready == "yes" and re.search(r"missing|not run|no behavior eval|no eval|untested", residual):
            errors.append("ready patch verdict cannot leave missing behavior/eval proof as residual risk")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("--allow-template", action="store_true")
    args = parser.parse_args()
    errors = validate(args.report, args.allow_template)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
