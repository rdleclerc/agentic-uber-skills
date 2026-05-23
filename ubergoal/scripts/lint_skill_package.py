#!/usr/bin/env python3
"""Lint the thin ubergoal wrapper package."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SKILL_NAME = "ubergoal"
REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "templates/goal-ledger.md",
    "templates/uber-run-receipt.md",
    "references/goal-objective.md",
    "references/refactor-campaign-profile.md",
    "scripts/validate_goal_objective.py",
    "scripts/validate_uber_run_receipt.py",
    "evals/golden_skill_invocations.json",
]
FORBIDDEN_MONOLITH_FILES = [
    "templates/plan-contract.md",
    "templates/final-acceptance.md",
    "scripts/validate_plan_contract.py",
    "scripts/validate_acceptance_report.py",
]
FORBIDDEN_SUFFIXES = {".pyc", ".pyo"}
FORBIDDEN_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache"}
REQUIRED_PHRASES = [
    "thin lifecycle wrapper",
    "goal owner",
    "bounded review-board coordinator",
    "create or bind",
    "specialist review-board agents",
    "Uber run receipt",
    "refactor campaign",
    "$uberplan",
    "$uberaccept",
    "$uberskillevolver",
    "$ubersimplify",
    "$uberassess",
    "benefit is **clearly much greater than**",
    "five consecutive failures",
    "material unexpected test failures",
    "user expectation / surprise assessment",
    "Skills invoked summary",
]
FORBIDDEN_PHRASES = [
    "Do not create a platform goal merely because this skill is active",
    "do not call create_goal unless",
    "do not create a platform goal without explicit launch instruction",
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
    for rel in FORBIDDEN_MONOLITH_FILES:
        if (root / rel).exists():
            errors.append(f"monolith resource should live in subskills, not ubergoal: {rel}")
    skill = (root / "SKILL.md").read_text() if (root / "SKILL.md").exists() else ""
    if f"name: {SKILL_NAME}" not in skill:
        errors.append(f"SKILL.md missing expected name: {SKILL_NAME}")
    for phrase in REQUIRED_PHRASES:
        if phrase not in skill:
            errors.append(f"SKILL.md missing phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in skill:
            errors.append(f"SKILL.md still contains obsolete goal-launch rule: {phrase}")
    if len(skill.splitlines()) > 160:
        errors.append("SKILL.md should stay thin (<160 lines)")
    meta = (root / "agents" / "openai.yaml").read_text() if (root / "agents" / "openai.yaml").exists() else ""
    for phrase in ["$ubergoal", "$uberplan", "$deep-rca", "$uberaccept", "$uberskillevolver", "$ubersimplify", "$uberassess", "create or bind", "specialist review-board agents", "refactor-campaign profile", "five consecutive failures", "user expectation/surprise"]:
        if phrase not in meta:
            errors.append(f"agents/openai.yaml missing phrase: {phrase}")
    for phrase in FORBIDDEN_PHRASES:
        if phrase in meta:
            errors.append(f"agents/openai.yaml still contains obsolete goal-launch rule: {phrase}")
    evals = root / "evals" / "golden_skill_invocations.json"
    if evals.exists():
        try:
            json.loads(evals.read_text())
        except Exception as exc:
            errors.append(f"invalid eval json: {exc}")
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
