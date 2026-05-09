#!/usr/bin/env python3
"""Validate a completed Architecture Steward report for ubergoal."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "pass type",
    "guide-loading scope",
    "component classification",
    "harness vs policy review",
    "required architecture dimensions",
    "complexity and tier challenge",
    "architecture findings",
    "gate recommendation",
]
REQUIRED_DIMENSIONS = [
    "source authority",
    "context assembly",
    "memory behavior",
    "tool boundaries",
    "durable execution",
    "eval/observability",
    "adoption/rollback",
    "subagent ownership",
    "human approvals",
    "budget/backpressure/fallback",
]


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def sections(markdown: str) -> dict[str, str]:
    result: dict[str, list[str]] = {}
    current: str | None = None
    for line in markdown.splitlines():
        match = re.match(r"^(#{2})\s+(.+?)\s*$", line)
        if match:
            current = normalize(match.group(2).strip("# "))
            result.setdefault(current, [])
        elif current:
            result[current].append(line)
    return {key: "\n".join(value).strip() for key, value in result.items()}


def rows(section: str) -> list[list[str]]:
    parsed: list[list[str]] = []
    for line in section.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells or cells[0].lower() in {"dimension", "guide/source", "deterministic harness responsibility", "severity"}:
            continue
        if all(set(cell) <= {"-", ":"} for cell in cells):
            continue
        parsed.append(cells)
    return parsed


def field_value(text: str, label: str) -> str:
    escaped = re.escape(label)
    separator = r"[ \t]*(?::)?[ \t]*" if label.endswith("?") else r"[ \t]*:[ \t]*"
    pattern = re.compile(rf"^[ \t]*-[ \t]*{escaped}{separator}(.+?)[ \t]*$", re.I | re.M)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--allow-template", action="store_true")
    args = parser.parse_args()

    text = args.path.read_text()
    lower = normalize(text)
    found = sections(text)
    errors: list[str] = []

    for section in REQUIRED_SECTIONS:
        if section not in found:
            errors.append(f"missing required section: {section}")

    for dimension in REQUIRED_DIMENSIONS:
        if dimension not in lower:
            errors.append(f"missing architecture dimension: {dimension}")

    if args.allow_template:
        if errors:
            print("FAIL: architecture steward template validation failed", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 1
        print("PASS: architecture steward template structure checks passed")
        return 0

    dimension_rows = rows(found.get("required architecture dimensions", ""))
    for dimension in REQUIRED_DIMENSIONS:
        matching = [row for row in dimension_rows if row and normalize(row[0]) == dimension]
        if not matching:
            errors.append(f"missing completed row for dimension: {dimension}")
            continue
        row = matching[0]
        # Dimension | Question | Finding | Evidence | Blocker?
        if len(row) < 5:
            errors.append(f"dimension row has too few cells: {dimension}")
            continue
        for idx, name in [(2, "finding"), (3, "evidence"), (4, "blocker")]:
            value = row[idx].strip().lower()
            if not value or value in {"", "n/a", "todo", "tbd"}:
                errors.append(f"dimension {dimension} missing {name}")

    guide_rows = rows(found.get("guide-loading scope", ""))
    if not guide_rows:
        errors.append("guide-loading scope needs at least one completed row")

    harness_rows = rows(found.get("harness vs policy review", ""))
    if not harness_rows:
        errors.append("harness vs policy review needs at least one completed row")

    allow = field_value(text, "Allow launch/acceptance?")
    if not allow:
        errors.append("missing Architecture Steward verdict allow field")
    elif not allow.lower().startswith("yes"):
        errors.append(f"Architecture Steward verdict does not allow launch/acceptance: {allow}")

    blockers = field_value(text, "Material blockers")
    if not blockers:
        errors.append("missing material blockers field")
    elif blockers.lower() not in {"none", "no", "none.", "resolved", "no material blockers"}:
        errors.append(f"material blockers not clear: {blockers}")

    if errors:
        print("FAIL: architecture steward report validation failed", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("PASS: architecture steward report sanity checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
