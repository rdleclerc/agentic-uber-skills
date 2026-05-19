#!/usr/bin/env python3
"""Lint the repo-local Uber skill creator package."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

SKILL_NAME = "uber-skill-creator"
REQUIRED_FILES = [
    "SKILL.md",
    "NOTICE.md",
    "LICENSE.txt",
    "agents/openai.yaml",
    "references/openai_yaml.md",
    "references/eval_driven_skill_creation.md",
    "scripts/init_skill.py",
    "scripts/quick_validate.py",
    "scripts/generate_openai_yaml.py",
    "scripts/generate_eval_report.py",
]
REQUIRED_PHRASES = [
    "portable",
    "eval-driven extension",
    "with-skill vs without-skill",
    "HTML review report",
    "trigger-description tuning",
]
FORBIDDEN_PLATFORM_PHRASES = [
    "claude-with-access-to-the-skill",
    "claude -p",
    "/skill-creator",
    "Claude Code command",
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
    for phrase in FORBIDDEN_PLATFORM_PHRASES:
        if phrase in skill:
            errors.append(f"SKILL.md contains platform-specific phrase: {phrase}")

    notice = (root / "NOTICE.md").read_text() if (root / "NOTICE.md").exists() else ""
    for phrase in ["OpenAI", "Anthropic", "No proprietary or leaked", "portable"]:
        if phrase not in notice:
            errors.append(f"NOTICE.md missing provenance phrase: {phrase}")

    meta = (root / "agents" / "openai.yaml").read_text() if (root / "agents" / "openai.yaml").exists() else ""
    if "allow_implicit_invocation: true" not in meta:
        errors.append("agents/openai.yaml must allow implicit invocation")
    if "eval-driven extension" not in meta:
        errors.append("agents/openai.yaml default prompt must mention eval-driven extension")

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
