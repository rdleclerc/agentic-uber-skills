#!/usr/bin/env python3
"""Lint the uberassess skill package."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SKILL_NAME = "uberassess"
REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "templates/assessment-packet.md",
    "templates/source-packet.md",
    "templates/project-context-card.md",
    "references/source-resolvers.md",
    "references/project-routing.md",
    "references/hermes-and-approval.md",
    "scripts/validate_assessment_packet.py",
    "evals/golden_skill_invocations.json",
]
REQUIRED_PHRASES = [
    "source-grounded recommendations",
    "Implementation before approval: no",
    "benefit >> cost",
    "Agent Advocate",
    "human counterfactual",
    "Hermes",
    "Do not create MCP servers",
    "Deep Research Assessment",
    "idea seed",
    "source map",
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
    if f"name: {SKILL_NAME}" not in skill:
        errors.append(f"SKILL.md missing expected name: {SKILL_NAME}")
    for phrase in REQUIRED_PHRASES:
        if phrase not in skill:
            errors.append(f"SKILL.md missing phrase: {phrase}")
    if len(skill.splitlines()) > 190:
        errors.append("SKILL.md should stay concise (<190 lines)")
    for match in re.findall(r"`((?:templates|references|scripts)/[^`]+)`", skill):
        if not (root / match).exists():
            errors.append(f"SKILL.md references missing resource: {match}")
    meta = (root / "agents" / "openai.yaml").read_text() if (root / "agents" / "openai.yaml").exists() else ""
    for phrase in ["$uberassess", "external source", "benefit >> cost", "allow_implicit_invocation: true", "do not auto-trigger from task similarity"]:
        if phrase not in meta:
            errors.append(f"agents/openai.yaml missing phrase: {phrase}")
    evals = root / "evals" / "golden_skill_invocations.json"
    if evals.exists():
        try:
            cases = json.loads(evals.read_text())
            for case in cases:
                if not case.get("id") or not case.get("user_prompt") or not case.get("expected_behavior"):
                    errors.append("each eval case needs id, user_prompt, expected_behavior")
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
