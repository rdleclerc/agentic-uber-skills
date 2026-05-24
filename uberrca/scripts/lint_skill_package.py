#!/usr/bin/env python3
"""Lint the uberrca skill package."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SKILL_NAME = "uberrca"
REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "evals/golden_skill_invocations.json",
    "scripts/lint_skill_package.py",
    "tests/test_validators.py",
]
REQUIRED_SKILL_PHRASES = [
    "self-challenge loop",
    "convergence test",
    "depth floor",
    "RCA ladder",
    "lowest enforceable layer",
    "five consecutive clear failures",
]
REQUIRED_META_PHRASES = [
    "allow_implicit_invocation: true",
    "$uberrca",
    "proximate cause",
]
FORBIDDEN_FILES = ["README.md"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dir", type=Path)
    args = parser.parse_args()
    root = args.skill_dir
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        if not (root / rel).exists():
            errors.append(f"missing required file: {rel}")
    for rel in FORBIDDEN_FILES:
        if (root / rel).exists():
            errors.append(f"forbidden auxiliary file in skill package: {rel}")

    skill = (root / "SKILL.md").read_text() if (root / "SKILL.md").exists() else ""
    if f"name: {SKILL_NAME}" not in skill:
        errors.append(f"SKILL.md missing expected name: {SKILL_NAME}")
    for phrase in REQUIRED_SKILL_PHRASES:
        if phrase not in skill:
            errors.append(f"SKILL.md missing phrase: {phrase}")

    meta = (root / "agents" / "openai.yaml").read_text() if (root / "agents" / "openai.yaml").exists() else ""
    for phrase in REQUIRED_META_PHRASES:
        if phrase not in meta:
            errors.append(f"agents/openai.yaml missing phrase: {phrase}")

    eval_path = root / "evals" / "golden_skill_invocations.json"
    if eval_path.exists():
        cases = json.loads(eval_path.read_text())
        if not isinstance(cases, list) or len(cases) < 4:
            errors.append("golden evals must contain at least four cases")
        ids = {case.get("id") for case in cases if isinstance(case, dict)}
        if "repeated_agent_patch_requires_class_rca" not in ids:
            errors.append("golden evals missing repeated-agent-patch case")
        if not any(case.get("should_trigger") is False for case in cases if isinstance(case, dict)):
            errors.append("golden evals need at least one non-trigger case")
        for case in cases:
            if not isinstance(case, dict):
                errors.append("each golden eval case must be an object")
                continue
            for field in ["id", "user_prompt", "should_trigger", "required_behavior"]:
                if field not in case:
                    errors.append(f"golden eval missing field {field}: {case.get('id', '<unknown>')}")
            if case.get("should_trigger") is True and not case.get("forbidden_behavior"):
                errors.append(f"trigger case needs forbidden behavior: {case.get('id', '<unknown>')}")

    for path in root.rglob("*"):
        if "__pycache__" in path.parts:
            errors.append(f"forbidden cache path present: {path.relative_to(root)}")
        if path.suffix in {".pyc", ".pyo"}:
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
