#!/usr/bin/env python3
"""Lint the ubersimplify skill package."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Iterable

REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "templates/simplify-plan.md",
    "templates/complexity-inventory.md",
    "templates/modularity-audit.md",
    "templates/dead-code-audit.md",
    "templates/test-confidence.md",
    "templates/simplification-candidates.md",
    "templates/patch-log.md",
    "templates/final-simplification-report.md",
    "references/dead-code-safeguards.md",
    "references/modularity-principles.md",
    "references/test-confidence.md",
    "references/agentic-simplification.md",
    "scripts/new_simplify_run.py",
    "scripts/validate_simplify_report.py",
    "evals/golden_skill_invocations.json",
]
REQUIRED_PHRASES = [
    "Complexity must justify itself",
    "deletion must earn proof",
    "Modularity gate",
    "Fail-fast gate",
    "Test-confidence policy",
    "Agent Advocate / human-counterfactual gate",
    "uberskillevolver",
]
FORBIDDEN_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache"}
FORBIDDEN_SUFFIXES = {".pyc", ".pyo"}


def tracked_files(root: Path) -> set[Path]:
    """Return git-tracked files under root, or empty set outside git.

    We intentionally check tracked/packageable artifacts rather than transient
    local caches so `python -m unittest` does not make lint self-fail.
    """
    try:
        top = subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "--show-toplevel"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except subprocess.CalledProcessError:
        return set()
    top_path = Path(top)
    rel_root = root.resolve().relative_to(top_path.resolve())
    out = subprocess.check_output(
        ["git", "-C", str(top_path), "ls-files", "-z", "--", str(rel_root)], text=False
    )
    files = set()
    for raw in out.split(b"\0"):
        if raw:
            files.add((top_path / raw.decode()).resolve())
    return files


def load_json(path: Path, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text())
    except Exception as exc:  # noqa: BLE001 - lint should report parse failure
        errors.append(f"invalid JSON: {path.relative_to(path.parents[1])}: {exc}")
        return None


def validate_openai_yaml(path: Path, errors: list[str]) -> None:
    if not path.exists():
        return
    text = path.read_text()
    try:
        import yaml  # type: ignore
    except Exception:
        # Minimal syntax guard for environments without PyYAML.
        for i, line in enumerate(text.splitlines(), 1):
            if line.strip() and not line.startswith(" ") and not re.match(r"^[A-Za-z_][\w-]*:\s*$", line):
                errors.append(f"agents/openai.yaml line {i} is not a simple top-level mapping key")
        return
    try:
        parsed = yaml.safe_load(text)
    except Exception as exc:  # noqa: BLE001
        errors.append(f"invalid YAML: agents/openai.yaml: {exc}")
        return
    if not isinstance(parsed, dict) or "interface" not in parsed or "policy" not in parsed:
        errors.append("agents/openai.yaml must contain interface and policy mappings")


def validate_eval_schema(root: Path, errors: list[str]) -> None:
    path = root / "evals" / "golden_skill_invocations.json"
    data = load_json(path, errors)
    if data is None:
        return
    if not isinstance(data, list) or not data:
        errors.append("golden_skill_invocations.json must be a non-empty list")
        return
    ids: set[str] = set()
    for idx, case in enumerate(data):
        if not isinstance(case, dict):
            errors.append(f"eval case {idx} must be an object")
            continue
        cid = case.get("id")
        if not isinstance(cid, str) or not cid:
            errors.append(f"eval case {idx} missing id")
        elif cid in ids:
            errors.append(f"duplicate eval id: {cid}")
        else:
            ids.add(cid)
        if not isinstance(case.get("user_prompt"), str) or not case.get("user_prompt"):
            errors.append(f"eval case {cid or idx} missing user_prompt")
        expected = case.get("expected_behavior")
        if not isinstance(expected, list) or not all(isinstance(item, str) and item for item in expected):
            errors.append(f"eval case {cid or idx} missing non-empty expected_behavior list")
        if "required_behavior" in case:
            errors.append(f"eval case {cid or idx} uses legacy required_behavior field")


def validate_skill_resource_refs(root: Path, skill: str, errors: list[str]) -> None:
    for ref in re.findall(r"`([^`]+)`", skill):
        if not (ref.startswith("templates/") or ref.startswith("references/") or ref.startswith("scripts/")):
            continue
        if not (root / ref).exists():
            errors.append(f"SKILL.md references missing resource: {ref}")


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
    if "name: ubersimplify" not in skill:
        errors.append("SKILL.md missing name: ubersimplify")
    for phrase in REQUIRED_PHRASES:
        if phrase not in skill:
            errors.append(f"SKILL.md missing phrase: {phrase}")
    if len(skill.splitlines()) > 190:
        errors.append("SKILL.md should stay concise (<190 lines)")
    validate_skill_resource_refs(root, skill, errors)

    meta_path = root / "agents" / "openai.yaml"
    validate_openai_yaml(meta_path, errors)
    meta = meta_path.read_text() if meta_path.exists() else ""
    if "$ubersimplify" not in meta or "Audit mode" not in meta:
        errors.append("agents/openai.yaml default prompt must mention $ubersimplify and Audit mode")
    if "allow_implicit_invocation: false" not in meta:
        errors.append("agents/openai.yaml should keep ubersimplify opt-in")

    validate_eval_schema(root, errors)

    for rel in ["scripts/new_simplify_run.py", "scripts/validate_simplify_report.py", "scripts/lint_skill_package.py"]:
        path = root / rel
        if path.exists() and not os.access(path, os.X_OK):
            errors.append(f"script should be executable: {rel}")

    tracked = tracked_files(root)
    for path in tracked:
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
