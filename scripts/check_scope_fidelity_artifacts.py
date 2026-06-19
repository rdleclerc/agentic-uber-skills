#!/usr/bin/env python3
"""Presence/order checks for Uber scope-fidelity artifacts.

This is intentionally non-semantic: it does not compare original scope to
implemented scope. It only verifies that the durable scope artifact exists,
that plans/acceptance reports expose required fields, and that ship language
cannot appear before the scope-fidelity verdict.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PLACEHOLDERS = {
    "",
    "todo",
    "tbd",
    "n/a",
    "na",
    "none",
    "no",
    "yes/no",
    "quote/link required",
    "required if narrowed",
}


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def non_empty_citation(value: str) -> bool:
    cleaned = normalize(value).strip("[]()<>` ")
    return cleaned not in PLACEHOLDERS


def read(path: Path, errors: list[str], label: str) -> str:
    try:
        return path.read_text()
    except FileNotFoundError:
        errors.append(f"{label} missing: {path}")
    except OSError as exc:
        errors.append(f"{label} unreadable: {path}: {exc}")
    return ""


def check_ship_order(text: str, errors: list[str], path: Path) -> None:
    match = re.search(r"^##\s+Scope fidelity verdict\s*$", text, flags=re.I | re.M)
    if not match:
        errors.append(f"acceptance/final report lacks ## Scope fidelity verdict: {path}")
        return
    before = text[: match.start()]
    if re.search(r"\bship\b", before, flags=re.I):
        errors.append(f"SHIP/ship language appears before scope-fidelity verdict: {path}")


def approval_after_narrowing(lines: list[str], index: int) -> bool:
    window = lines[index : min(len(lines), index + 10)]
    for line in window:
        match = re.match(
            r"^\s*-\s*(?:Operator approved narrowing in|Approval evidence[^:]*)\s*:\s*(.+?)\s*$",
            line,
            flags=re.I,
        )
        if match and non_empty_citation(match.group(1)):
            return True
    return False


def check_narrowing_approval(text: str, errors: list[str], path: Path) -> None:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if re.match(r"^\s*-\s*Narrowing\?\s*(?::\s*)?yes\b", line, flags=re.I):
            if not approval_after_narrowing(lines, idx):
                errors.append(f"Narrowing? yes lacks non-empty approval citation: {path}:{idx + 1}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", type=Path, required=True, help="coordination/<task-slug>/scope.md")
    parser.add_argument("--plan", type=Path, action="append", default=[], help="durable plan file to inspect")
    parser.add_argument("--acceptance", type=Path, action="append", default=[], help="final acceptance/report file to inspect")
    args = parser.parse_args()

    errors: list[str] = []
    if not args.scope.exists():
        errors.append(f"scope.md missing: {args.scope}")
    elif not args.scope.is_file():
        errors.append(f"scope path is not a file: {args.scope}")

    for plan in args.plan:
        text = read(plan, errors, "plan")
        if text:
            if not re.search(r"^##\s+Scope fidelity\s*$", text, flags=re.I | re.M):
                errors.append(f"plan lacks ## Scope fidelity block: {plan}")
            check_narrowing_approval(text, errors, plan)

    for acceptance in args.acceptance:
        text = read(acceptance, errors, "acceptance")
        if text:
            check_ship_order(text, errors, acceptance)
            check_narrowing_approval(text, errors, acceptance)

    if errors:
        print("FAIL: scope fidelity artifact checks failed", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("PASS: scope fidelity artifact checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
