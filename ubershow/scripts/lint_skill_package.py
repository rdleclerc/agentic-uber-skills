#!/usr/bin/env python3
"""Lint the ubershow skill package."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "schemas/decision-board.schema.json",
    "snippets/copy-button.js",
    "snippets/theme.css",
    "templates/architecture-map.html",
    "templates/code-review-map.html",
    "templates/decision-board.html",
    "templates/implementation-plan.html",
    "templates/questionnaire.html",
    "templates/status-timeline.html",
    "templates/visual-brief.html",
    "evals/golden_skill_invocations.json",
]
TEMPLATES = [rel for rel in REQUIRED_FILES if rel.startswith("templates/")]
REQUIRED_SKILL_PHRASES = [
    "browser-first",
    "copyable decision receipt",
    "HTML artifacts are generated **views**, not canonical truth",
    "Obsidian/Soho House is optional archive context only",
    "Do **not** turn every answer into HTML",
]
FORBIDDEN_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache"}
FORBIDDEN_SUFFIXES = {".pyc", ".pyo"}


def tracked_files(root: Path) -> set[Path]:
    try:
        top = subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "--show-toplevel"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except subprocess.CalledProcessError:
        return set()
    top_path = Path(top)
    rel_root = root.resolve().relative_to(top_path.resolve())
    out = subprocess.check_output(["git", "-C", str(top_path), "ls-files", "-z", "--", str(rel_root)], text=False)
    files: set[Path] = set()
    for raw in out.split(b"\0"):
        if raw:
            files.add((top_path / raw.decode()).resolve())
    return files


def load_json(path: Path, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text())
    except Exception as exc:  # noqa: BLE001 - package lint reports parse errors
        errors.append(f"invalid JSON: {path.relative_to(path.parents[1])}: {exc}")
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dir", type=Path)
    args = parser.parse_args()
    root = args.skill_dir.resolve()
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        if not (root / rel).exists():
            errors.append(f"missing required file: {rel}")

    skill = (root / "SKILL.md").read_text() if (root / "SKILL.md").exists() else ""
    if "name: ubershow" not in skill:
        errors.append("SKILL.md missing name: ubershow")
    if len(skill.splitlines()) > 170:
        errors.append("SKILL.md should stay concise (<170 lines)")
    for phrase in REQUIRED_SKILL_PHRASES:
        if phrase not in skill:
            errors.append(f"SKILL.md missing phrase: {phrase}")
    for ref in re.findall(r"`([^`]+)`", skill):
        if not (ref.startswith("templates/") or ref.startswith("snippets/") or ref.startswith("schemas/")):
            continue
        if not (root / ref).exists():
            errors.append(f"SKILL.md references missing resource: {ref}")

    meta = (root / "agents" / "openai.yaml").read_text() if (root / "agents" / "openai.yaml").exists() else ""
    for phrase in ["Ubershow", "browser-first visual artifact", "copyable decision receipts", "allow_implicit_invocation: true"]:
        if phrase not in meta:
            errors.append(f"agents/openai.yaml missing phrase: {phrase}")

    schema = load_json(root / "schemas" / "decision-board.schema.json", errors)
    if isinstance(schema, dict):
        required = set(schema.get("required", []))
        expected = {"artifact_id", "title", "recommendation", "options", "sources", "open_questions"}
        if not expected <= required:
            errors.append(f"decision-board schema missing required fields: {sorted(expected - required)}")

    evals = load_json(root / "evals" / "golden_skill_invocations.json", errors)
    if isinstance(evals, list):
        if not evals:
            errors.append("golden_skill_invocations.json must contain at least one case")
        for idx, case in enumerate(evals):
            if not isinstance(case, dict):
                errors.append(f"eval case {idx} must be an object")
                continue
            if not case.get("id") or not case.get("user_prompt"):
                errors.append(f"eval case {idx} needs id and user_prompt")
            expected_behavior = case.get("expected_behavior")
            if not isinstance(expected_behavior, list) or not all(isinstance(item, str) and item for item in expected_behavior):
                errors.append(f"eval case {case.get('id', idx)} needs non-empty expected_behavior list")

    for rel in TEMPLATES:
        path = root / rel
        if not path.exists():
            continue
        text = path.read_text()
        lower = text.lower()
        for phrase in ["<!doctype html>", "data-artifact-kind=", "data-ubershow-template=", "decision-receipt", "copyDecisionReceipt", "navigator.clipboard.writeText"]:
            if phrase.lower() not in lower:
                errors.append(f"{rel} missing required self-contained artifact phrase: {phrase}")
        if "<script src=" in lower or "<link " in lower or "http://" in lower or "https://" in lower:
            errors.append(f"{rel} must be self-contained with no external network dependencies")

    for path in tracked_files(root):
        rel = path.relative_to(root)
        if any(part in FORBIDDEN_DIRS for part in rel.parts):
            errors.append(f"tracked forbidden cache path present: {rel}")
        if path.suffix in FORBIDDEN_SUFFIXES:
            errors.append(f"tracked forbidden bytecode file present: {rel}")

    if errors:
        for error in sorted(set(errors)):
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
