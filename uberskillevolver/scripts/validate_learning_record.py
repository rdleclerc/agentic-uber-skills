#!/usr/bin/env python3
"""Validate a Uberskillevolver post-run learning record."""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

REQUIRED_SECTIONS = [
    "Run metadata",
    "Evidence links",
    "What worked",
    "What failed or surprised us",
    "Agent Advocate / human counterfactual",
    "Complexity and speed economics",
    "Runtime topology lesson",
    "Lesson candidates",
    "Completion-claim regression check",
    "Promotion decision",
    "Privacy and redaction",
    "Validation / follow-up",
]

DECISIONS = ("promote", "defer", "delete", "no-change", "no change")
PLACEHOLDER_PATTERNS = (r"TODO", r"TBD", r"\[\s*\]")


def section_body(text: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\s*$"
    match = re.search(pattern, text, flags=re.MULTILINE)
    if not match:
        return ""
    start = match.end()
    next_match = re.search(r"^## ", text[start:], flags=re.MULTILINE)
    end = start + next_match.start() if next_match else len(text)
    return text[start:end].strip()


def non_placeholder_lines(body: str) -> list[str]:
    lines = []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped or stripped in {"-", "|---|---|---|---|---|"}:
            continue
        if any(re.search(p, stripped, flags=re.IGNORECASE) for p in PLACEHOLDER_PATTERNS):
            continue
        # Ignore pure table scaffolding with empty cells.
        if stripped.startswith("|") and re.fullmatch(r"[|\sLIDessonvcEidPromtfrNangeohw-]+", stripped):
            continue
        lines.append(stripped)
    return lines


def validate(path: Path) -> list[str]:
    text = path.read_text()
    errors: list[str] = []
    for section in REQUIRED_SECTIONS:
        if f"## {section}" not in text:
            errors.append(f"missing required section: {section}")

    evidence = section_body(text, "Evidence links")
    if len(non_placeholder_lines(evidence)) < 1:
        errors.append("Evidence links must contain at least one concrete non-placeholder item")

    promotion = section_body(text, "Promotion decision").lower()
    if not any(decision in promotion for decision in DECISIONS):
        errors.append("Promotion decision must name promote/defer/delete/no-change")

    privacy = section_body(text, "Privacy and redaction").lower()
    if "safe to commit" not in privacy:
        errors.append("Privacy and redaction must state whether the record is safe to commit")

    regression = section_body(text, "Completion-claim regression check")
    if len(non_placeholder_lines(regression)) < 3:
        errors.append("Completion-claim regression check must contain concrete evidence or no-change rationale")
    regression_lower = regression.lower()
    for phrase in ["shared safe proof spine", "operational outcome contract", "eval/template/validator", "anti-bloat"]:
        if phrase not in regression_lower:
            errors.append(f"Completion-claim regression check missing: {phrase}")

    topology = section_body(text, "Runtime topology lesson")
    if len(non_placeholder_lines(topology)) < 3:
        errors.append("Runtime topology lesson must contain concrete topology evidence or no-change rationale")
    topology_lower = topology.lower()
    for phrase in ["plan depth", "spawned-agent depth", "depth/thread", "restore"]:
        if phrase not in topology_lower:
            errors.append(f"Runtime topology lesson missing: {phrase}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    errors = validate(args.record)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {args.record}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
