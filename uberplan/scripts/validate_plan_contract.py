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
    "1": CORE_SECTIONS
    + [
        "cost/complexity check",
        "repository topology / package seam",
        "risk-to-evidence map",
        "acceptance rubric",
        "pre-launch confidence gate",
    ],
    "2": CORE_SECTIONS
    + [
        "product / prd checklist",
        "task map / implementation graph",
        "cost/complexity check",
        "first-principles simplifier / complexity auditor",
        "planning review board",
        "agent advocate / agent failure rca",
        "architecture steward lane",
        "repository topology / package seam",
        "risk-to-evidence map",
        "acceptance rubric",
        "pre-launch confidence gate",
    ],
    "3": CORE_SECTIONS
    + [
        "product / prd checklist",
        "task map / implementation graph",
        "cost/complexity check",
        "first-principles simplifier / complexity auditor",
        "planning review board",
        "agent advocate / agent failure rca",
        "architecture steward lane",
        "multi-agent plan",
        "repository topology / package seam",
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
    "agent boundary contract",
    "regex / keyword semantics",
    "prd checklist",
    "task map",
    "thin harness / fat agent",
    "source-convention check",
    "architecture",
    "repository topology",
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


CODE_OR_TOPOLOGY_PATTERNS = [
    r"\bnew/moved code\b",
    r"\bnew/moved code files?\b",
    r"\badd(?:s|ed|ing)? (?:a )?(?:new )?(?:module|package|file|script|validator)\b",
    r"\bnew (?:module|package|file|script|validator)\b",
    r"\broot[- ]level (?:module|file)\b",
    r"\bmove(?:s|d|ing)? (?:code|module|file|package)\b",
    r"\bpackage move\b",
    r"\brefactor\b",
    r"\bpackage seam (?:change|changes|changed)\b",
    r"\bpackage boundary (?:change|changes|changed)\b",
    r"\bimport boundary\b",
    r"\bdependency boundary\b",
]


def has_code_or_topology_scope(text: str) -> bool:
    return any(re.search(pattern, text, re.I) for pattern in CODE_OR_TOPOLOGY_PATTERNS)


def validate_repository_topology(found: dict[str, str], lower: str, tier: str, errors: list[str]) -> None:
    if tier == "0":
        return
    section_name = "repository topology / package seam"
    section = found.get(section_name, "")
    if not section:
        return
    if not section_has_substance(section):
        errors.append("required section lacks completed substance: repository topology / package seam")
        return

    code_scope = has_code_or_topology_scope(lower)
    section_lower = normalize(section)
    explicitly_na = "not applicable because" in section_lower
    if explicitly_na:
        if code_scope:
            errors.append(
                "repository topology cannot be marked not applicable when plan text indicates new/moved code, root-level modules, package moves, refactors, or package/dependency seams"
            )
        return

    for label in [
        "Intended package/module destination",
        "Why this does not belong at the root/convenience layer",
        "Public import/API seam",
        "Private/internal files",
        "Repo-local topology/dependency guard to run or add",
        "If no guard exists, why that is acceptable for this task",
    ]:
        value = require_field(section, label, errors)
        low = value.lower()
        if low in {"none", "no", "no guard", "not needed", "not applicable"}:
            errors.append(f"repository topology field is not sufficient: {label}={value}")

    guard = require_field(section, "Repo-local topology/dependency guard to run or add", errors).lower()
    if guard and not any(term in guard for term in ["test", "gate", "dependency", "topology", "lint", "validator", "validate", "command"]):
        errors.append("repository topology guard must name an executable gate/test/lint/validator command")


SENTINEL_TERMS = [
    "wrong-shaped",
    "identifier",
    "swallowed",
    "ask",
    "shared",
    "mutable",
    "untrusted",
    "bounded",
    "privileged",
    "parent",
    "trace",
]


SEMANTIC_PATTERN_SCOPE_TERMS = [
    "regex",
    "regexp",
    "regular expression",
    "keyword",
    "pattern list",
    "string matcher",
    "classifier",
    "router",
    "routing",
    "heuristic",
    "semantic judgment",
    "semantic judgement",
    "request-likeness",
    "intent",
]


AGENTIC_SYSTEM_TERMS = [
    "agentic-system",
    "agentic system",
    "agent loop",
    "multi-agent",
    "subagent",
    "skill",
    "tool registry",
    "memory subsystem",
    "context engine",
    "source authority",
    "cross-agent",
    "prompt",
    "model/adaptive",
]


def has_semantic_pattern_scope(text: str) -> bool:
    return any(term in text for term in SEMANTIC_PATTERN_SCOPE_TERMS)


def has_agentic_system_scope(text: str) -> bool:
    return any(term in text for term in AGENTIC_SYSTEM_TERMS)


def validate_prd_checklist(found: dict[str, str], tier: str, errors: list[str]) -> None:
    if tier == "0":
        return
    section_name = "product / prd checklist"
    section = found.get(section_name, "")
    if not section:
        return
    if not section_has_substance(section):
        errors.append("required section lacks completed substance: Product / PRD checklist")
        return
    checked_items = re.findall(r"^\s*-\s*\[[ xX]\]\s+\S+", section, re.M)
    if len(checked_items) < 3:
        errors.append("Product / PRD checklist must include at least three checkable - [ ] / - [x] items")
    section_lower = normalize(section)
    for term in ["user", "problem", "requirement", "non-goal", "acceptance"]:
        if term not in section_lower:
            errors.append(f"Product / PRD checklist missing concept: {term}")


def validate_task_map(found: dict[str, str], tier: str, errors: list[str]) -> None:
    if tier == "0":
        return
    section_name = "task map / implementation graph"
    section = found.get(section_name, "")
    if not section:
        return
    if not section_has_substance(section):
        errors.append("required section lacks completed substance: Task map / implementation graph")
        return
    section_lower = normalize(section)
    if "```mermaid" not in section_lower:
        errors.append("Task map / implementation graph must include a Mermaid diagram")
    if not re.search(r"\bT[0-9]+\b", section):
        errors.append("Task map / implementation graph must use stable task IDs such as T1, T2, T3")
    for term in ["depend", "owner", "write", "evidence", "done"]:
        if term not in section_lower:
            errors.append(f"Task map / implementation graph missing concept: {term}")


def validate_thin_harness_rubric(found: dict[str, str], required: bool, errors: list[str]) -> None:
    section_name = "thin harness / fat agent design rubric"
    section = found.get(section_name, "")
    if not required:
        return
    if not section:
        errors.append("agentic-system scope requires Thin harness / fat agent design rubric section")
        return
    if not section_has_substance(section):
        errors.append("required section lacks completed substance: Thin harness / fat agent design rubric")
        return
    section_lower = normalize(section)
    for term in [
        "harness owns",
        "agent owns",
        "monolith",
        "deterministic",
        "skill",
        "tool",
        "reusable",
        "modular",
        "depend",
    ]:
        if term not in section_lower:
            errors.append(f"Thin harness / fat agent design rubric missing concept: {term}")
    if "regex" not in section_lower and "keyword" not in section_lower:
        errors.append("Thin harness / fat agent design rubric must address regex/keyword semantic-authority risk")


def validate_source_convention_check(found: dict[str, str], required: bool, errors: list[str]) -> None:
    section_name = "source-convention check"
    section = found.get(section_name, "")
    if not required:
        return
    if not section:
        errors.append("agentic-system scope requires Source-convention check section")
        return
    if not section_has_substance(section):
        errors.append("required section lacks completed substance: Source-convention check")
        return
    section_lower = normalize(section)
    for term in ["source", "codex", "openclaude", "claude code", "convention", "copied"]:
        if term not in section_lower:
            errors.append(f"Source-convention check missing concept: {term}")
    if not any(term in section_lower for term in ["public", "approved", "local", "available", "unavailable"]):
        errors.append("Source-convention check must name whether source references are approved/public/local/available or unavailable")
    if not any(term in section_lower for term in ["no leaked", "proprietary", "do not copy", "not copied", "no code copied"]):
        errors.append("Source-convention check must state the no-leaked/proprietary/no-copy boundary")


def validate_agentic_evidence_map(found: dict[str, str], required: bool, errors: list[str]) -> None:
    if not required:
        return
    evidence = normalize(found.get("risk-to-evidence map", ""))
    rubric = normalize(found.get("acceptance rubric", ""))
    combined = evidence + " " + rubric
    evidence_groups = {
        "unit/regression": ["unit", "regression"],
        "integration": ["integration"],
        "acceptance": ["acceptance"],
        "e2e/simulation": ["e2e", "end-to-end", "simulation", "simulated"],
        "evals": ["eval", "fixture", "real-world", "real bug", "replay"],
    }
    for label, terms in evidence_groups.items():
        if not any(term in combined for term in terms):
            errors.append(f"agentic-system evidence map must cover or explicitly reject {label} evidence")


def validate_regex_keyword_semantic_gate(found: dict[str, str], required: bool, errors: list[str]) -> None:
    section_name = "regex / keyword semantic gate"
    section = found.get(section_name, "")
    if not required:
        return
    if not section:
        errors.append("agentic or regex/keyword scope requires Regex / keyword semantic gate section")
        return
    if not section_has_substance(section):
        errors.append("required section lacks completed substance: Regex / keyword semantic gate")
        return
    section_lower = normalize(section)
    substantive_lines = [line.strip().lower() for line in section.splitlines() if line.strip()]
    if substantive_lines and substantive_lines[0].startswith("not applicable because"):
        errors.append("Regex / keyword semantic gate cannot be marked not applicable when agentic or regex/keyword scope is active")
        return

    for label in [
        "Pattern uses introduced/touched",
        "Classification for each use",
        "Semantic authority over natural language present?",
        "Raw input preserved for model/review?",
        "Eval/replay/negative cases",
        "Observability and rollback",
        "Gate verdict",
    ]:
        require_field(section, label, errors)

    classification = require_field(section, "Classification for each use", errors).lower()
    if classification and not any(term in classification for term in ["mechanical", "candidate", "semantic authority"]):
        errors.append("Regex / keyword semantic gate classification must use mechanical syntax, candidate signal, or semantic authority")

    semantic_authority = require_field(section, "Semantic authority over natural language present?", errors).lower()
    if semantic_authority and not semantic_authority.startswith(("yes", "no")):
        errors.append("Semantic authority over natural language present? must be yes or no")
    if semantic_authority.startswith("yes"):
        exception = require_field(section, "If yes, explicit exception approval and why model policy is not sufficient", errors).lower()
        if not exception or "approval" not in exception:
            errors.append("semantic-authority regex/keyword exception must name explicit approval")
        if "eval" not in section_lower and "replay" not in section_lower:
            errors.append("semantic-authority regex/keyword exception requires eval/replay coverage")
        if "rollback" not in section_lower:
            errors.append("semantic-authority regex/keyword exception requires rollback")
    raw_preserved = require_field(section, "Raw input preserved for model/review?", errors).lower()
    if raw_preserved and not raw_preserved.startswith("yes"):
        errors.append("Regex / keyword semantic gate must preserve raw input for model/review")
    verdict = require_field(section, "Gate verdict", errors)
    if verdict and "proceed? yes" not in verdict.lower():
        errors.append("Regex / keyword semantic gate verdict must explicitly say proceed? yes")


def validate_agent_boundary_contract(found: dict[str, str], behavior_scope: bool, errors: list[str]) -> None:
    section_name = "agent boundary contract"
    section = found.get(section_name, "")
    if not behavior_scope:
        return
    if not section:
        errors.append("agent-behavior scope requires Agent Boundary Contract section")
        return
    if not section_has_substance(section):
        errors.append("required section lacks completed substance: Agent Boundary Contract")
        return
    section_lower = normalize(section)
    if "not applicable because" in section_lower:
        errors.append("Agent Boundary Contract cannot be marked not applicable when agent-behavior scope is active")
        return

    for label in [
        "Boundary surfaces",
        "Shape contract",
        "Authority contract",
        "Isolation contract",
        "Failure semantics",
        "Observability/replay evidence",
        "Sentinel probes checked",
        "Boundary verdict",
    ]:
        require_field(section, label, errors)

    for term in ["shape", "authority", "isolation", "failure", "observability", "replay", "sentinel"]:
        if term not in section_lower:
            errors.append(f"Agent Boundary Contract missing concept: {term}")
    sentinel_value = require_field(section, "Sentinel probes checked", errors).lower()
    if sentinel_value and not any(term in sentinel_value for term in SENTINEL_TERMS):
        errors.append("Agent Boundary Contract sentinel probes must name at least one relevant recurring failure probe")
    verdict = require_field(section, "Boundary verdict", errors)
    if verdict and "proceed? yes" not in verdict.lower():
        errors.append("Agent Boundary Contract verdict must explicitly say proceed? yes")


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

    validate_prd_checklist(found, args.tier or "1", errors)
    validate_task_map(found, args.tier or "1", errors)
    validate_repository_topology(found, lower, args.tier or "1", errors)

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
        found.get("deterministic harness vs adaptive policy", ""),
    ]))
    behavior_scope = args.agent_behavior or (args.tier != "0" and any(term in behavior_scan_text for term in behavior_terms))
    agentic_system_scope = args.tier != "0" and (behavior_scope or has_agentic_system_scope(behavior_scan_text))
    validate_thin_harness_rubric(found, agentic_system_scope, errors)
    validate_source_convention_check(found, agentic_system_scope, errors)
    validate_agent_boundary_contract(found, behavior_scope, errors)
    semantic_pattern_scope = behavior_scope or has_semantic_pattern_scope(behavior_scan_text)
    validate_regex_keyword_semantic_gate(found, semantic_pattern_scope, errors)
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
    validate_agentic_evidence_map(found, agentic_system_scope, errors)

    rubric = found.get("acceptance rubric", "")
    present_dimensions = [dimension for dimension in RUBRIC_DIMENSIONS if dimension in normalize(rubric)]
    if args.tier != "0" and len(present_dimensions) < 5:
        errors.append("rubric has fewer than five recognized risk-mapped dimensions")
    if args.tier != "0" and has_code_or_topology_scope(lower) and "repository topology" not in normalize(rubric):
        errors.append("acceptance rubric must include repository topology when plan indicates new/moved code or package seams")

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
