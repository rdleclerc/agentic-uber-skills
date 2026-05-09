#!/usr/bin/env python3
"""Validate a completed ubergoal plan contract.

By default this validates completed artifacts, not blank templates. Use
--allow-template only when checking that bundled templates contain the right
sections without requiring filled-in evidence.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CORE_SECTIONS = ["objective", "scope", "tier decision"]
TIER_REQUIREMENTS = {
    "0": CORE_SECTIONS,
    "1": CORE_SECTIONS + ["cost/complexity check", "risk-to-evidence map", "acceptance rubric", "pre-launch confidence gate"],
    "2": CORE_SECTIONS
    + [
        "cost/complexity check",
        "first-principles simplifier / complexity auditor",
        "planning review board",
        "agent advocate / agent failure rca",
        "architecture steward lane",
        "risk-to-evidence map",
        "acceptance rubric",
        "pre-launch confidence gate",
    ],
    "3": CORE_SECTIONS
    + [
        "cost/complexity check",
        "first-principles simplifier / complexity auditor",
        "planning review board",
        "agent advocate / agent failure rca",
        "architecture steward lane",
        "multi-agent plan",
        "risk-to-evidence map",
        "acceptance rubric",
        "pre-launch confidence gate",
    ],
}

PLACEHOLDER_PATTERNS = [
    r"\byes/no\b",
    r"\blow/medium/high\b",
    r"state the concrete",
    r"classify relevant",
    r"paste the final",
    r"activate only the lanes",
    r"only fill this if",
    r"blocker/non-blocker",
    r"plan section/file/test/eval",
    r"\|\s*\|\s*\|",
    r"^\s*-\s*$",
]

RUBRIC_DIMENSIONS = [
    "scope clarity",
    "planning review",
    "cost/complexity",
    "first-principles simplification",
    "codebase exploration",
    "agent rca",
    "architecture",
    "ownership",
    "code quality",
    "dead code",
    "unit/regression tests",
    "integration tests",
    "ui/browser tests",
    "evals",
    "safety",
    "observability",
    "rollback",
    "acceptance evidence",
]


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def sections(markdown: str) -> dict[str, str]:
    result: dict[str, list[str]] = {}
    current: str | None = None
    for line in markdown.splitlines():
        match = re.match(r"^(#{2})\s+(.+?)\s*$", line)
        if match:
            current = normalize(match.group(2).strip("# "))
            result.setdefault(current, [])
        elif current:
            result[current].append(line)
    return {key: "\n".join(value).strip() for key, value in result.items()}


def section_has_substance(content: str) -> bool:
    stripped_lines = [line.strip() for line in content.splitlines() if line.strip()]
    if not stripped_lines:
        return False
    non_boilerplate: list[str] = []
    for line in stripped_lines:
        low = line.lower()
        if re.match(r"^\|\s*-+", low):
            continue
        if re.match(r"^\|?\s*(dimension|surface|agent role|risk/failure mode|deterministic harness owns|score|---)", low):
            continue
        if any(re.search(pattern, low) for pattern in PLACEHOLDER_PATTERNS):
            continue
        # bare field labels are placeholders, e.g. '- Scope accepted:'
        if re.match(r"^-\s*[^:]{1,80}:\s*$", line):
            continue
        if line in {"-", "|  |  |  |", "|  |  |  |  |"}:
            continue
        non_boilerplate.append(line)
    return bool(non_boilerplate)


def require_field(text: str, label: str, errors: list[str]) -> str:
    escaped = re.escape(label)
    separator = r"[ \t]*(?::)?[ \t]*" if label.endswith("?") else r"[ \t]*:[ \t]*"
    pattern = re.compile(rf"^[ \t]*-[ \t]*{escaped}{separator}(.+?)[ \t]*$", re.I | re.M)
    match = pattern.search(text)
    if not match:
        errors.append(f"missing field: {label}")
        return ""
    value = match.group(1).strip()
    if not value or value.lower() in {"yes/no", "n/a", "tbd", "todo", "none?"}:
        errors.append(f"empty or placeholder field: {label}")
    return value


def table_meaningful_rows(section: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in section.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells or all(not cell or set(cell) <= {"-", ":"} for cell in cells):
            continue
        headerish = {"surface", "dimension", "risk/failure mode", "agent role", "deterministic harness owns"}
        if cells[0].strip().lower() in headerish:
            continue
        if any(cell for cell in cells) and not all(cell in {"", " ", "-"} for cell in cells):
            rows.append(cells)
    return rows


def blockers_clear(text: str, errors: list[str], label: str = "Material blockers") -> None:
    value = require_field(text, label, errors)
    if not value:
        return
    low = value.lower()
    if low not in {"none", "no", "none.", "resolved", "no material blockers"}:
        errors.append(f"{label} is not clear: {value}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Markdown plan contract path")
    parser.add_argument("--tier", choices=["0", "1", "2", "3"], help="Expected tier")
    parser.add_argument("--agent-behavior", action="store_true", help="Require Agent Advocate / Agent RCA evidence")
    parser.add_argument("--openclaw", action="store_true", help="Require OpenClaw / Platform Steward evidence")
    parser.add_argument("--allow-template", action="store_true", help="Validate template structure without filled-in evidence")
    args = parser.parse_args()

    text = args.path.read_text()
    lower = normalize(text)
    found = sections(text)
    errors: list[str] = []
    warnings: list[str] = []

    required = TIER_REQUIREMENTS.get(args.tier or "1", TIER_REQUIREMENTS["1"])
    for section in required:
        if section not in found:
            errors.append(f"missing required section: {section}")

    if args.allow_template:
        if errors:
            print("FAIL: plan template structure validation failed", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 1
        print("PASS: plan template structure checks passed")
        return 0

    # Completed-artifact checks.
    for section in required:
        if section in found and not section_has_substance(found[section]):
            errors.append(f"required section lacks completed substance: {section}")

    # Tier 0 is intentionally light but still needs a concrete test/evidence note.
    if args.tier == "0":
        if "test" not in lower and "evidence" not in lower:
            errors.append("tier 0 plan needs at least a lightweight test/evidence note")
    else:
        if "100% confident within scope" not in lower:
            errors.append("missing explicit scoped 100% confidence language")
        blockers_clear(text, errors)
        verdict = require_field(text, "100% confident within scope?", errors)
        if verdict and not verdict.lower().startswith("yes"):
            errors.append(f"confidence verdict is not yes: {verdict}")

    if args.tier in {"2", "3"}:
        if "steward" not in lower:
            errors.append(f"tier {args.tier} requires explicit Architecture Steward involvement")
        board = found.get("planning review board", "")
        if "allow confidence gate? yes" not in normalize(board):
            errors.append("planning review board must explicitly allow confidence gate: yes")
        if "lanes activated" not in normalize(board) or not section_has_substance(board):
            errors.append("planning review board must name activated/skipped lanes and reconciled findings")

    if args.tier == "3":
        if "multi-agent plan" in found and not table_meaningful_rows(found["multi-agent plan"]):
            errors.append("tier 3 multi-agent plan needs meaningful role rows")

    behavior_terms = [
        "multi-agent",
        "subagent",
        "agent behavior",
        "agent error",
        "prompt",
        "tool",
        "context",
        "memory",
        "handoff",
        "agent loop",
    ]
    behavior_scan_text = normalize("\n".join([
        found.get("objective", ""),
        found.get("scope", ""),
        found.get("affected surfaces", ""),
        found.get("architecture classification", ""),
    ]))
    behavior_scope = args.agent_behavior or any(term in behavior_scan_text for term in behavior_terms)
    enforce_agent_advocate = args.agent_behavior or args.tier in {"2", "3"}
    if enforce_agent_advocate:
        if "agent advocate / agent failure rca" not in found:
            errors.append("tier 2/3 or agent-behavior scope requires Agent Advocate / Agent Failure RCA section, even when explicitly not applicable")
        else:
            advocate = found["agent advocate / agent failure rca"]
            advocate_lower = normalize(advocate)
            explicitly_na = "not applicable because" in advocate_lower
            if behavior_scope and explicitly_na:
                errors.append("Agent Advocate cannot be marked not applicable when plan text indicates agent/prompt/tool/context/memory/handoff behavior scope")
            if not explicitly_na:
                for phrase in ["human counterfactual", "human-parity", "root failed invariant", "symptom-patch risk"]:
                    if phrase not in advocate_lower:
                        errors.append(f"Agent Advocate section missing: {phrase}")
                if "proceed? yes" not in advocate_lower:
                    errors.append("Agent Advocate verdict must explicitly say proceed? yes")

    if args.openclaw:
        board = found.get("planning review board", "") + "\n" + found.get("multi-agent plan", "")
        if "openclaw" not in normalize(board) and "platform steward" not in normalize(board):
            errors.append("--openclaw requires OpenClaw / Platform Steward lane or explicit policy rationale")

    risk_rows = table_meaningful_rows(found.get("risk-to-evidence map", ""))
    if args.tier != "0" and not risk_rows:
        errors.append("risk-to-evidence map needs at least one meaningful row")

    rubric = found.get("acceptance rubric", "")
    present_dimensions = [dimension for dimension in RUBRIC_DIMENSIONS if dimension in normalize(rubric)]
    if args.tier != "0" and len(present_dimensions) < 5:
        errors.append("rubric has fewer than five recognized risk-mapped dimensions")

    if args.tier != "0":
        cost = found.get("cost/complexity check", "")
        cost_lower = normalize(cost)
        if "failure class" not in cost_lower or "smaller alternative" not in cost_lower:
            errors.append("cost/complexity check must name the failure class and smaller alternative considered")
        if "benefit >> cost" not in cost_lower:
            errors.append("cost/complexity check must include a benefit >> cost argument")

    if args.tier in {"2", "3"}:
        simp = found.get("first-principles simplifier / complexity auditor", "")
        simp_lower = normalize(simp)
        if not simp:
            errors.append("tier 2/3 requires First-Principles Simplifier / Complexity Auditor section")
        else:
            for phrase in ["requirements challenged", "parts/processes/agents/schemas/files removed", "benefit >> cost verdict", "proceed? yes"]:
                if phrase not in simp_lower:
                    errors.append(f"First-Principles Simplifier section missing: {phrase}")

    if errors:
        print("FAIL: plan contract validation failed", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        for warning in warnings:
            print(f"warning: {warning}", file=sys.stderr)
        return 1

    print("PASS: plan contract sanity checks passed")
    for warning in warnings:
        print(f"warning: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
