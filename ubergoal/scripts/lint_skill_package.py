#!/usr/bin/env python3
"""Lint the ubergoal skill package."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SKILL_NAME = "ubergoal"
REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "templates/plan-contract.md",
    "templates/confidence-gate.md",
    "templates/goal-ledger.md",
    "templates/planning-review-board.md",
    "templates/agent-failure-rca.md",
    "templates/architecture-steward-report.md",
    "templates/agent-brief.md",
    "templates/final-acceptance.md",
    "references/codex-goal-objective.md",
    "references/tiering-and-rubric.md",
    "references/agentic-architecture-checklist.md",
    "scripts/validate_goal_objective.py",
    "scripts/validate_plan_contract.py",
    "scripts/validate_acceptance_report.py",
    "scripts/validate_architecture_steward_report.py",
]

FORBIDDEN_SUFFIXES = {".pyc", ".pyo"}
FORBIDDEN_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dir", type=Path)
    args = parser.parse_args()
    root = args.skill_dir
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        if not (root / rel).exists():
            errors.append(f"missing required file: {rel}")

    skill = (root / "SKILL.md").read_text() if (root / "SKILL.md").exists() else ""
    if not skill.startswith("---"):
        errors.append("SKILL.md missing YAML frontmatter")
    if f"name: {SKILL_NAME}" not in skill:
        errors.append(f"SKILL.md missing expected name: {SKILL_NAME}")
    if "description:" not in skill:
        errors.append("SKILL.md missing description")

    for match in re.findall(r"`((?:templates|references|scripts)/[^`]+)`", skill):
        if not (root / match).exists():
            errors.append(f"SKILL.md references missing resource: {match}")

    meta = (root / "agents" / "openai.yaml").read_text() if (root / "agents" / "openai.yaml").exists() else ""
    if f"${SKILL_NAME}" not in meta:
        errors.append(f"agents/openai.yaml default_prompt must mention ${SKILL_NAME}")
    for phrase in ["do not call `create_goal`", "Agent Advocate", "human counterfactual", "planning review board", "cost/complexity"]:
        if phrase not in meta:
            errors.append(f"agents/openai.yaml missing prompt phrase: {phrase}")

    for path in root.rglob("*"):
        if any(part in FORBIDDEN_DIRS for part in path.parts):
            errors.append(f"forbidden cache path present: {path.relative_to(root)}")
        if path.suffix in FORBIDDEN_SUFFIXES:
            errors.append(f"forbidden bytecode file present: {path.relative_to(root)}")

    if errors:
        print("FAIL: skill package lint failed", file=sys.stderr)
        for error in sorted(set(errors)):
            print(f"- {error}", file=sys.stderr)
        return 1
    print("PASS: skill package lint passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
