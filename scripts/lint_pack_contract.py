#!/usr/bin/env python3
"""Lint repo-level agent contract and Uber skill routing policy."""
from __future__ import annotations

from pathlib import Path
import argparse
import re
import sys

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
PACK_SKILLS = ["deep-rca", "ubergoal", "uberplan", "uberaccept", "uberskillevolver", "ubersimplify", "uberassess"]
UBER_PHASE_SKILLS = ["uberplan", "uberaccept", "uberskillevolver", "ubersimplify", "uberassess"]
ROOT_REQUIRED_FILES = ["AGENTS.md", "CLAUDE.md", "README.md", "ROADMAP.md"]
AGENTS_REQUIRED_PHRASES = [
    "$ubergoal` is the only default/implicit Uber lifecycle router",
    "Phase skills are explicit or wrapper-invoked",
    "uberassess` = source-to-recommendation due diligence",
    "deep-rca` = general incident/root-cause authority",
    "Agent Advocate = agent-behavior-specific RCA lens",
    "Source repo: `/Users/claw1/agentic-uber-skills`",
    "Local Codex install target: `/Users/claw1/.codex/skills/<skill>`",
    "Do not commit, tag, push, or publish without explicit user authorization",
]
README_REQUIRED_PHRASES = [
    "Agent-facing source authority lives in [AGENTS.md](AGENTS.md)",
    "invoke `$ubergoal` as the implicit lifecycle router",
    "`$deep-rca` is the general incident/debugging/root-cause utility",
]
ROADMAP_REQUIRED_PHRASES = [
    "`ubergoal` is the only implicit/default Uber lifecycle router",
    "Phase skills are explicit or wrapper-invoked",
    "uberassess` = source-to-recommendation due diligence",
    "Build a small pack-level harness before creating a standalone `ubereval` skill",
    "Uberassess dogfooding",
]


def read(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def policy_value(root: Path, skill: str) -> str | None:
    path = root / skill / "agents" / "openai.yaml"
    if not path.exists():
        return None
    match = re.search(r"^\s*allow_implicit_invocation:\s*(true|false)\s*$", path.read_text(), flags=re.M)
    return match.group(1) if match else None


def install_loop_skills(readme: str, heading: str) -> set[str]:
    pattern = rf"### {re.escape(heading)}.*?for s in ([^;]+); do"
    match = re.search(pattern, readme, flags=re.S)
    if not match:
        return set()
    return set(match.group(1).split())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    args = parser.parse_args()
    root = args.root.resolve()

    errors: list[str] = []

    for rel in ROOT_REQUIRED_FILES:
        if not (root / rel).exists():
            errors.append(f"missing root contract file: {rel}")

    for skill in PACK_SKILLS:
        if not (root / skill / "SKILL.md").exists():
            errors.append(f"missing skill package: {skill}/SKILL.md")

    implicit = {skill: policy_value(root, skill) for skill in ["ubergoal", *UBER_PHASE_SKILLS]}
    if implicit.get("ubergoal") != "true":
        errors.append("ubergoal must be the only implicit/default Uber router")
    for skill in UBER_PHASE_SKILLS:
        if implicit.get(skill) != "false":
            errors.append(f"{skill} must be explicit/wrapper-invoked with allow_implicit_invocation: false")

    for skill in UBER_PHASE_SKILLS:
        skill_text = read(root / skill / "SKILL.md")
        meta = read(root / skill / "agents" / "openai.yaml")
        if skill == "uberassess":
            if "Direct-use only when explicitly named" not in skill_text or "routed by `ubergoal`" not in skill_text:
                errors.append("uberassess SKILL.md must state direct-use/routed-only policy")
            if "only when explicitly invoked" not in meta or "routed by $ubergoal" not in meta:
                errors.append("uberassess metadata must state explicit-or-routed invocation")
        else:
            if "Direct-use only when explicitly named or routed by ubergoal" not in skill_text:
                errors.append(f"{skill} SKILL.md must state direct-use/routed-only policy")
            if "only when explicitly invoked or routed by $ubergoal" not in meta:
                errors.append(f"{skill} metadata must state explicit-or-routed invocation")

    agents = read(root / "AGENTS.md")
    for phrase in AGENTS_REQUIRED_PHRASES:
        if phrase not in agents:
            errors.append(f"AGENTS.md missing phrase: {phrase}")

    claude = read(root / "CLAUDE.md")
    if "AGENTS.md" not in claude or "$ubergoal` is the default router" not in claude:
        errors.append("CLAUDE.md must defer to AGENTS.md and name ubergoal as default router")

    readme = read(root / "README.md")
    for phrase in README_REQUIRED_PHRASES:
        if phrase not in readme:
            errors.append(f"README.md missing phrase: {phrase}")
    for heading in ["Generic install", "Codex-compatible install", "Claude Code-compatible install"]:
        skills = install_loop_skills(readme, heading)
        if skills != set(PACK_SKILLS):
            errors.append(f"{heading} loop should include exactly {', '.join(PACK_SKILLS)}; found {sorted(skills)}")

    roadmap = read(root / "ROADMAP.md")
    for phrase in ROADMAP_REQUIRED_PHRASES:
        if phrase not in roadmap:
            errors.append(f"ROADMAP.md missing phrase: {phrase}")

    if errors:
        for error in sorted(set(errors)):
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"PASS: pack contract lint passed for {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
