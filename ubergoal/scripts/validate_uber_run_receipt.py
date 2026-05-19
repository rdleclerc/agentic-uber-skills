#!/usr/bin/env python3
"""Validate a completed lightweight Uber run receipt.

This is a shape/evidence-presence validator, not a semantic judge. It keeps
`uberskillevolver` from promoting lessons based only on vague prose by requiring
skill-use, artifact, gate, replay, verdict, and learning-handoff receipts.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "run metadata",
    "skills used",
    "artifacts",
    "gates",
    "fresh-agent replay",
    "behavior verdict",
    "uberskillevolver handoff",
]
REQUIRED_SKILLS = [
    "ubergoal",
    "uberassess",
    "uberplan",
    "uberaccept",
    "ubersimplify",
    "uberskillevolver",
    "ubershow",
    "deep-rca",
    "skill-creator",
]
REQUIRED_GATES = [
    "goal created/bound or explicitly skipped",
    "uberplan or work-contract planning",
    "plan acceptance / thin-harness check",
    "uberaccept final proof",
    "policy-adherence / openclaw architecture check",
    "skills used summary",
    "uberskillevolver learning decision",
]
PLACEHOLDERS = {"", " ", "todo", "tbd", "yes/no", "yes/no/n/a", "pass/fail/n/a"}


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


def table_rows(section: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in section.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells or all(not cell or set(cell) <= {"-", ":"} for cell in cells):
            continue
        first = cells[0].strip().lower()
        if first in {"skill", "artifact", "gate"}:
            continue
        rows.append(cells)
    return rows


def require_field(section: str, label: str, errors: list[str]) -> str:
    separator = r"[ \t]*(?::)?[ \t]*" if label.endswith("?") else r"[ \t]*:[ \t]*"
    pattern = re.compile(rf"^[ \t]*-[ \t]*{re.escape(label)}{separator}(.+?)[ \t]*$", re.I | re.M)
    match = pattern.search(section)
    if not match:
        errors.append(f"missing field: {label}")
        return ""
    value = match.group(1).strip()
    if normalize(value) in PLACEHOLDERS:
        errors.append(f"placeholder field: {label}")
    return value


def validate(path: Path, allow_template: bool = False) -> list[str]:
    text = path.read_text()
    found = sections(text)
    errors: list[str] = []
    for section in REQUIRED_SECTIONS:
        if section not in found:
            errors.append(f"missing required section: {section}")
    if allow_template:
        return errors
    if errors:
        return errors

    metadata = found["run metadata"]
    for label in ["Run slug", "Date/time", "Project/repo", "Tier", "Owner/session", "Outcome"]:
        require_field(metadata, label, errors)

    skill_rows = table_rows(found["skills used"])
    skill_names = {normalize(row[0]) for row in skill_rows if row}
    for skill in REQUIRED_SKILLS:
        if skill not in skill_names:
            errors.append(f"skills used table missing skill: {skill}")
    for row in skill_rows:
        if len(row) < 5:
            errors.append(f"skills used row has too few cells: {' | '.join(row)}")
            continue
        used = normalize(row[1])
        evidence = normalize(row[2])
        reason = normalize(row[3])
        if used not in {"yes", "no", "n/a", "na", "not applicable"}:
            errors.append(f"skill {row[0]} has invalid Used? value: {row[1]}")
        if evidence in PLACEHOLDERS:
            errors.append(f"skill {row[0]} missing evidence/artifact entry")
        if reason in PLACEHOLDERS:
            errors.append(f"skill {row[0]} missing reason used/skipped")

    artifact_rows = table_rows(found["artifacts"])
    if len(artifact_rows) < 3:
        errors.append("artifacts table needs at least three meaningful rows")
    for row in artifact_rows:
        if len(row) >= 4 and normalize(row[2]).startswith("yes") and not normalize(row[3]).startswith("yes"):
            errors.append(f"required artifact not present: {row[0]}")

    gate_rows = table_rows(found["gates"])
    gate_names = {normalize(row[0]) for row in gate_rows if row}
    for gate in REQUIRED_GATES:
        if gate not in gate_names:
            errors.append(f"gates table missing gate: {gate}")
    for row in gate_rows:
        if len(row) >= 4:
            expected = normalize(row[1])
            result = normalize(row[3])
            if expected.startswith("yes") and result != "pass":
                errors.append(f"expected gate did not pass: {row[0]}={row[3]}")

    replay = found["fresh-agent replay"]
    for label in ["Replay mode", "Replay prompt / fixture", "Result", "Missing affordances", "Follow-up"]:
        require_field(replay, label, errors)

    verdict = found["behavior verdict"]
    for label in [
        "Did the run use the intended Uber skills?",
        "Did the skills change behavior versus generic planning?",
        "Did the run avoid fat-harness / deterministic-monolith drift?",
        "Did the run produce enough evidence for `uberskillevolver`?",
        "Verdict rationale",
    ]:
        require_field(verdict, label, errors)
    enough = require_field(verdict, "Did the run produce enough evidence for `uberskillevolver`?", errors)
    if enough and not normalize(enough).startswith("yes"):
        errors.append("receipt says it does not produce enough evidence for uberskillevolver")

    handoff = found["uberskillevolver handoff"]
    for label in ["Learning record path", "Candidate lessons", "Promote now", "Defer", "No-change rationale", "Safe to commit?"]:
        require_field(handoff, label, errors)
    safe = require_field(handoff, "Safe to commit?", errors)
    if safe and not normalize(safe).startswith("yes"):
        errors.append("uberskillevolver handoff is not safe to commit")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--allow-template", action="store_true")
    args = parser.parse_args()
    errors = validate(args.path, args.allow_template)
    if errors:
        print("FAIL: Uber run receipt validation failed", file=sys.stderr)
        for error in sorted(set(errors)):
            print(f"- {error}", file=sys.stderr)
        return 1
    print("PASS: Uber run receipt checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
