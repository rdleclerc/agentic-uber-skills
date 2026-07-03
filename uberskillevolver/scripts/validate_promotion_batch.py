#!/usr/bin/env python3
"""Validate a Uberskillevolver skill-evolution promotion batch."""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

REQUIRED_SECTIONS = [
    "Batch metadata",
    "Candidates included",
    "Proposed skill changes",
    "Non-goals and deferred ideas",
    "Human review checklist",
    "Validation evidence",
    "Rollback / retirement plan",
    "Final decision",
]

FORBIDDEN = [
    "silent self-modification is allowed",
    "auto-apply without review",
    "mutate itself without review",
    "skip human review",
]

WORD_DELTA_RE = re.compile(r"\bwords_(?:added|removed)\s*=\s*\d+\b", re.IGNORECASE)


def section_body(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\s*$", text, flags=re.MULTILINE)
    if not match:
        return ""
    start = match.end()
    next_match = re.search(r"^## ", text[start:], flags=re.MULTILINE)
    end = start + next_match.start() if next_match else len(text)
    return text[start:end].strip()


def candidate_rows(text: str) -> list[str]:
    body = section_body(text, "Candidates included")
    rows: list[str] = []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or re.fullmatch(r"\|(?:[-: ]+\|)+", stripped):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if cells and cells[0].lower() == "id":
            continue
        rows.append(stripped)
    return rows


def has_word_delta_pair(row: str) -> bool:
    lowered = row.lower()
    return "words_added" in lowered and "words_removed" in lowered and len(WORD_DELTA_RE.findall(row)) >= 2


def validate(path: Path) -> list[str]:
    text = path.read_text()
    lower = text.lower()
    errors: list[str] = []
    for section in REQUIRED_SECTIONS:
        if f"## {section}" not in text:
            errors.append(f"missing required section: {section}")
    for phrase in FORBIDDEN:
        if phrase in lower:
            errors.append(f"forbidden drift policy phrase: {phrase}")
    checklist = section_body(text, "Human review checklist").lower()
    for required in ["no silent self-modification", "concrete run evidence", "benefit"]:
        if required not in checklist:
            errors.append(f"human review checklist must mention: {required}")
    validation = section_body(text, "Validation evidence").lower()
    if not any(word in validation for word in ["test", "eval", "validator", "lint", "quick validation"]):
        errors.append("validation evidence must mention tests/evals/validators/lint/quick validation")
    final = section_body(text, "Final decision").lower()
    if not any(decision in final for decision in ["approved", "revise", "rejected"]):
        errors.append("final decision must be approved, revise, or rejected")
    for row in candidate_rows(text):
        if re.search(r"\bpromote[- ]now\b", row, flags=re.IGNORECASE) and not has_word_delta_pair(row):
            errors.append("promote-now candidates must include words_added=<n> and words_removed=<n>")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch", type=Path)
    args = parser.parse_args()
    errors = validate(args.batch)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {args.batch}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
