#!/usr/bin/env python3
"""Lint the uberplan skill package."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SKILL_NAME = "uberplan"
REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "templates/plan-contract.md",
    "templates/confidence-gate.md",
    "templates/planning-review-board.md",
    "templates/exploration-trail.md",
    "templates/agent-failure-rca.md",
    "templates/architecture-steward-report.md",
    "templates/first-principles-simplifier-report.md",
    "templates/agent-brief.md",
    "references/tiering-and-rubric.md",
    "references/agentic-architecture-checklist.md",
    "scripts/validate_plan_contract.py",
    "evals/golden_skill_invocations.json",
]
FORBIDDEN_SUFFIXES = {".pyc", ".pyo"}
FORBIDDEN_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache"}
REQUIRED_PHRASES = [
    "benefit >> cost",
    "Agent Advocate",
    "human counterfactual",
    "First-Principles",
    "confidence gate",
    "long-running goal",
    "Agent execution proof ladder",
    "User expectation / surprise assessment",
    "over-orchestration",
    "five consecutive clear failures",
    "RCA-driven scope expansion",
    "child/sub-`uberplan` appendix",
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
    skill = (root / "SKILL.md").read_text() if (root / "SKILL.md").exists() else ""
    if f"name: {SKILL_NAME}" not in skill:
        errors.append(f"SKILL.md missing expected name: {SKILL_NAME}")
    for phrase in REQUIRED_PHRASES:
        if phrase not in skill:
            errors.append(f"SKILL.md missing phrase: {phrase}")
    if len(skill.splitlines()) > 220:
        errors.append("SKILL.md should stay concise (<220 lines)")
    for match in re.findall(r"`((?:templates|references|scripts)/[^`]+)`", skill):
        if not (root / match).exists():
            errors.append(f"SKILL.md references missing resource: {match}")
    meta = (root / "agents" / "openai.yaml").read_text() if (root / "agents" / "openai.yaml").exists() else ""
    if "$uberplan" not in meta or "benefit >> cost" not in meta:
        errors.append("agents/openai.yaml default prompt must mention $uberplan and benefit >> cost")
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
