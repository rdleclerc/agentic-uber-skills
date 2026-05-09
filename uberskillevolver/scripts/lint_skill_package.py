#!/usr/bin/env python3
"""Lint the uberskillevolver skill package."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "templates/post-run-learning.md",
    "templates/lesson-candidate.md",
    "templates/promotion-batch.md",
    "templates/skill-evolution-change-plan.md",
    "scripts/new_learning_record.py",
    "scripts/validate_learning_record.py",
    "scripts/validate_promotion_batch.py",
    "evals/golden_skill_invocations.json",
    "references/cross-machine-learning.md",
]

REQUIRED_SKILL_PHRASES = [
    "never through silent self-modification",
    "human-reviewed",
    "benefit is **clearly much greater than**",
    "Agent Advocate",
    "Relationship to Ubergoal",
    "Cross-machine learning",
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dir", type=Path)
    args = parser.parse_args()
    root = args.skill_dir
    errors: list[str] = []
    for rel in REQUIRED_FILES:
        if not (root / rel).exists():
            errors.append(f"missing required file: {rel}")
    skill = root / "SKILL.md"
    if skill.exists():
        text = skill.read_text()
        if "name: uberskillevolver" not in text:
            errors.append("SKILL.md frontmatter must name uberskillevolver")
        for phrase in REQUIRED_SKILL_PHRASES:
            if phrase not in text:
                errors.append(f"SKILL.md missing phrase: {phrase}")
        if len(text.splitlines()) > 260:
            errors.append("SKILL.md should stay concise (<260 lines)")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
