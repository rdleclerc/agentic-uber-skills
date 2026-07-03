#!/usr/bin/env python3
"""Lint repo-level agent contract and Uber skill routing policy."""
from __future__ import annotations

from pathlib import Path
import argparse
import re
import sys

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
PACK_SKILLS = [
    "uberrca",
    "uber-skill-creator",
    "ubergoal",
    "uberplan",
    "uberaccept",
    "uberskillevolver",
    "ubersimplify",
    "uberassess",
    "uberarchitect",
    "ubershow",
]
UBER_PHASE_SKILLS = ["uberplan", "uberaccept", "uberskillevolver", "ubersimplify", "uberassess", "uberarchitect"]
UTILITY_IMPLICIT_SKILLS = ["uberrca", "uber-skill-creator", "ubershow"]
ROOT_REQUIRED_FILES = ["AGENTS.md", "CLAUDE.md", "README.md", "ROADMAP.md"]
FORBIDDEN_FRONTMATTER_KEYS = {"model", "effort"}
MODEL_ID_RE = re.compile(
    r"\b(?:claude-[A-Za-z0-9][A-Za-z0-9_.-]*-\d+(?:[.-]\d+)*|gpt-\d+(?:[.-]\d+)*(?:-[A-Za-z0-9_.-]+)?)\b",
    re.I,
)
ABSOLUTE_PATH_RE = re.compile(
    r"(?<![A-Za-z0-9_:$~.-])"
    r"(/(?:Users|tmp|private|var|opt|usr|etc|home|Library|Applications|Volumes)/[^\s`'\"<>),]+)"
)
MACHINE_USER_PATH_RE = re.compile(r"/Users/[^/\s`'\"<>),]+/[^\s`'\"<>),]*")
PORTABILITY_EXEMPT_MARKERS = ("fixture-path: intentional", "portable-path: intentional")
DOCTRINE_TEXT_SUFFIXES = {".md", ".txt", ".toml", ".yaml", ".yml", ".json", ".html"}
AGENTS_REQUIRED_PHRASES = [
    "$ubergoal` is the only default/implicit Uber lifecycle router",
    "All skills in this pack must be installed and exposed to Codex sessions",
    "Review and acceptance lanes use the highest-capability available Claude lane; record `lane_used` in the receipt; never silently downgrade. In gaia contexts the spine's lane policy governs (`knowledge/coding-agent-operating-spine.md` in the gaia workspace repo).",
    "Phase skills are explicit or wrapper-invoked",
    "uberassess` = source-to-recommendation due diligence",
    "ubershow` = visual communication utility",
    "uberarchitect` = architecture stepback gate",
    "uberrca` = general incident/root-cause authority",
    "Agent Advocate = agent-behavior-specific RCA lens",
    "New standalone CLIs only where fixtures prove separate need; default = module in the pack-contract aggregator",
    "Source repo: this repository's checkout location",
    "Local Codex install target: `~/.codex/skills/<skill>`",
    "Local Claude install target: `~/.claude/skills/<skill>`",
    "Codex adapter metadata should expose every pack skill",
    "Do not commit, tag, push, or publish without explicit user authorization",
    "child/sub-`uberplan` appendix",
]
README_REQUIRED_PHRASES = [
    "Agent-facing source authority lives in [AGENTS.md](AGENTS.md)",
    "Review and acceptance lanes use the highest-capability available Claude lane; record `lane_used` in the receipt; never silently downgrade.",
    "invoke `$ubergoal` as the implicit lifecycle router",
    "`$uberrca` is the general incident/debugging/root-cause utility",
    "`$ubershow`",
    "skills invoked",
]
ROADMAP_REQUIRED_PHRASES = [
    "`ubergoal` is the only implicit/default Uber lifecycle router",
    "Phase skills are explicit or wrapper-invoked",
    "Codex adapter metadata still exposes every skill in the pack",
    "uberassess` = source-to-recommendation due diligence",
    "Build a small pack-level harness before creating a standalone `ubereval` skill",
    "Uberassess dogfooding",
    "Ubershow dogfooding",
    "RCA-driven testing adaptation",
]


def read(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def frontmatter(root: Path, skill: str) -> str:
    text = read(root / skill / "SKILL.md")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", text, flags=re.S)
    if not match:
        return ""
    return match.group(1)


def doctrine_text_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for rel in ["AGENTS.md", "README.md", "ROADMAP.md"]:
        path = root / rel
        if path.exists():
            files.append(path)
    for skill in PACK_SKILLS:
        skill_root = root / skill
        skill_md = skill_root / "SKILL.md"
        if skill_md.exists():
            files.append(skill_md)
        for dirname in ["references", "templates"]:
            base = skill_root / dirname
            if base.exists():
                files.extend(path for path in base.rglob("*") if path.is_file() and path.suffix in DOCTRINE_TEXT_SUFFIXES)
    for dirname in ["references", "templates"]:
        base = root / dirname
        if base.exists():
            files.extend(path for path in base.rglob("*") if path.is_file() and path.suffix in DOCTRINE_TEXT_SUFFIXES)
    return sorted(set(files))


def has_portability_exemption(lines: list[str], index: int) -> bool:
    for offset in (-1, 0):
        candidate = index + offset
        if 0 <= candidate < len(lines):
            if any(marker in lines[candidate] for marker in PORTABILITY_EXEMPT_MARKERS):
                return True
    return False


def is_parameterized_path_line(line: str) -> bool:
    return "${" in line and ":-" in line and "}" in line


def clean_path_candidate(raw: str) -> str:
    return raw.rstrip(".,:;")


def validate_frontmatter_policy(root: Path, errors: list[str]) -> None:
    for skill in PACK_SKILLS:
        path = root / skill / "SKILL.md"
        if not path.exists():
            errors.append(f"missing skill package: {skill}/SKILL.md")
            continue
        meta = frontmatter(root, skill)
        if not meta:
            errors.append(f"{skill} must have SKILL.md frontmatter")
            continue
        for match in re.finditer(r"^\s*([A-Za-z0-9_-]+)\s*:", meta, flags=re.M):
            key = match.group(1).lower()
            if key in FORBIDDEN_FRONTMATTER_KEYS:
                errors.append(f"{skill} SKILL.md frontmatter must not contain `{key}:`")
        model_match = MODEL_ID_RE.search(meta)
        if model_match:
            errors.append(f"{skill} SKILL.md frontmatter must not hardcode model id `{model_match.group(0)}`")


def validate_portability_oracle(root: Path, errors: list[str]) -> None:
    for path in doctrine_text_files(root):
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        rel = path.relative_to(root)
        lines = text.splitlines()
        for index, line in enumerate(lines):
            if has_portability_exemption(lines, index) or is_parameterized_path_line(line):
                continue
            for match in MACHINE_USER_PATH_RE.finditer(line):
                candidate = clean_path_candidate(match.group(0))
                errors.append(f"{rel}:{index + 1} machine-specific path must be parameterized or marker-exempted: {candidate}")
            for match in ABSOLUTE_PATH_RE.finditer(line):
                candidate = clean_path_candidate(match.group(1))
                if MACHINE_USER_PATH_RE.search(candidate):
                    continue
                if not Path(candidate).exists():
                    errors.append(f"{rel}:{index + 1} absolute path does not exist or need parameterization: {candidate}")


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

    validate_frontmatter_policy(root, errors)

    implicit = {skill: policy_value(root, skill) for skill in ["ubergoal", *UBER_PHASE_SKILLS]}
    if implicit.get("ubergoal") != "true":
        errors.append("ubergoal must be the only implicit/default Uber router")
    for skill in UBER_PHASE_SKILLS:
        if implicit.get(skill) != "true":
            errors.append(f"{skill} must be exposed to Codex sessions with allow_implicit_invocation: true")
    for skill in UTILITY_IMPLICIT_SKILLS:
        if policy_value(root, skill) != "true":
            errors.append(f"{skill} utility metadata must allow task-specific implicit invocation")

    for skill in UBER_PHASE_SKILLS:
        skill_text = read(root / skill / "SKILL.md")
        meta = read(root / skill / "agents" / "openai.yaml")
        if skill == "uberassess":
            if "Do not auto-trigger from task similarity" not in skill_text or "routed by `ubergoal`" not in skill_text:
                errors.append("uberassess SKILL.md must state direct-use/routed-only policy")
            if "only when explicitly invoked" not in meta or "routed by $ubergoal" not in meta:
                errors.append("uberassess metadata must state explicit-or-routed invocation")
        else:
            if "Do not auto-trigger from task similarity" not in skill_text or "Use only when explicitly named" not in skill_text:
                errors.append(f"{skill} SKILL.md must state direct-use/routed-only policy")
            if "only when explicitly invoked or routed by $ubergoal" not in meta:
                errors.append(f"{skill} metadata must state explicit-or-routed invocation")

    deep = read(root / "uberrca" / "SKILL.md")
    deep_meta = read(root / "uberrca" / "agents" / "openai.yaml")
    deep_evals = root / "uberrca" / "evals" / "golden_skill_invocations.json"
    deep_lint = root / "uberrca" / "scripts" / "lint_skill_package.py"
    if "self-challenge loop" not in deep or "lowest enforceable layer" not in deep:
        errors.append("uberrca must keep RCA depth and durable-fix doctrine")
    if "$uberarchitect" not in deep or "Architecture stepback route" not in deep:
        errors.append("uberrca must route system-shape RCA to uberarchitect")
    if "$uberrca" not in deep_meta or "proximate cause" not in deep_meta:
        errors.append("uberrca metadata must describe proximate-cause RCA trigger")
    if not deep_evals.exists() or not deep_lint.exists():
        errors.append("uberrca must keep golden evals and package lint")
    if (root / "uberrca" / "README.md").exists():
        errors.append("uberrca must not carry package-local README.md")

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

    validate_portability_oracle(root, errors)

    if errors:
        for error in sorted(set(errors)):
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"PASS: pack contract lint passed for {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
