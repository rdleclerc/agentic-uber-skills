#!/usr/bin/env python3
"""Validate a durable UberRCA artifact."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

INTAKE_FIELDS = ["failure_case_id", "case_updated", "not_applicable_with_reason"]
PLACEHOLDERS = {"", "todo", "tbd", "n/a", "none", "<id>", "<text>"}


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def sections(markdown: str) -> dict[str, str]:
    out: dict[str, list[str]] = {}
    current: str | None = None
    for line in markdown.splitlines():
        match = re.match(r"^##\s+(.+?)\s*$", line)
        if match:
            current = normalize(match.group(1))
            out.setdefault(current, [])
        elif current:
            out[current].append(line)
    return {key: "\n".join(value).strip() for key, value in out.items()}


def field_value(text: str, label: str) -> str:
    pattern = re.compile(rf"^[ \t]*(?:-[ \t]*)?{re.escape(label)}[ \t]*:[ \t]*(.+?)[ \t]*$", re.I | re.M)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def sentence_count(text: str) -> int:
    return len([part for part in re.split(r"[.!?]+", text.strip()) if part.strip()])


def validate_intake(text: str, errors: list[str]) -> None:
    present: list[str] = []
    for field in INTAKE_FIELDS:
        value = field_value(text, field)
        if value and normalize(value) not in PLACEHOLDERS:
            present.append(field)
    if len(present) != 1:
        errors.append(
            "failure intake requires exactly one non-empty field: "
            "failure_case_id | case_updated | not_applicable_with_reason"
        )


def validate(path: Path, *, allow_template: bool = False) -> list[str]:
    text = path.read_text()
    found = sections(text)
    errors: list[str] = []
    invariant = field_value(text, "class_invariant")
    if not invariant:
        errors.append("missing field: class_invariant")
    elif not allow_template:
        if normalize(invariant) in PLACEHOLDERS:
            errors.append("placeholder field: class_invariant")
        elif sentence_count(invariant) != 1:
            errors.append("class_invariant must be one sentence")

    surface = found.get("surface enumeration", "")
    if not surface:
        errors.append("missing required section: surface enumeration")
    elif not allow_template:
        bullets = [line for line in surface.splitlines() if line.strip().startswith("- ")]
        if not bullets:
            errors.append("surface_enumeration must be a non-empty list")
        elif all(normalize(line.strip()[2:]) in PLACEHOLDERS for line in bullets):
            errors.append("surface_enumeration must not contain only placeholder bullets")
    if allow_template:
        return errors
    validate_intake(text, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--allow-template", action="store_true")
    args = parser.parse_args()
    errors = validate(args.path, allow_template=args.allow_template)
    if errors:
        print("FAIL: RCA artifact validation failed", file=sys.stderr)
        for error in sorted(set(errors)):
            print(f"- {error}", file=sys.stderr)
        return 1
    print("PASS: RCA artifact checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
