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
        "goal execution posture and delivery",
        "user expectation / surprise assessment",
        "definition of done / operational outcome contract",
        "testing adaptation gate",
        "cost/complexity check",
        "repository topology / package seam",
        "risk-to-evidence map",
        "acceptance rubric",
        "pre-launch confidence gate",
    ],
    "2": CORE_SECTIONS
    + [
        "goal execution posture and delivery",
        "user expectation / surprise assessment",
        "definition of done / operational outcome contract",
        "product / prd checklist",
        "task map / implementation graph",
        "verifiable subgoals and metrics",
        "parallelization plan",
        "runtime agent topology / codex depth-thread policy",
        "testing adaptation gate",
        "cost/complexity check",
        "first-principles simplifier / complexity auditor",
        "planning review board",
        "agent advocate / agent failure rca",
        "architecture steward lane",
        "target architecture / file tree",
        "repository topology / package seam",
        "code-health / dead-code tool plan",
        "decision / tradeoff / surprise register",
        "pre-presentation over-orchestration review",
        "plan acceptance gate",
        "risk-to-evidence map",
        "acceptance rubric",
        "pre-launch confidence gate",
    ],
    "3": CORE_SECTIONS
    + [
        "goal execution posture and delivery",
        "user expectation / surprise assessment",
        "definition of done / operational outcome contract",
        "product / prd checklist",
        "task map / implementation graph",
        "verifiable subgoals and metrics",
        "parallelization plan",
        "runtime agent topology / codex depth-thread policy",
        "testing adaptation gate",
        "cost/complexity check",
        "first-principles simplifier / complexity auditor",
        "planning review board",
        "agent advocate / agent failure rca",
        "architecture steward lane",
        "multi-agent plan",
        "target architecture / file tree",
        "repository topology / package seam",
        "code-health / dead-code tool plan",
        "decision / tradeoff / surprise register",
        "pre-presentation over-orchestration review",
        "plan acceptance gate",
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
    "verifiable subgoals",
    "parallelization",
    "runtime agent topology",
    "tier 3 expensive-proof preflight",
    "burn-in vs final proof",
    "phase-boundary contract fuzz",
    "testing adaptation",
    "goal execution posture",
    "user expectation",
    "surprise assessment",
    "operational outcome",
    "recursive pseudocode",
    "plan tree artifact layout",
    "agent execution proof ladder",
    "thin harness / fat agent",
    "source-convention check",
    "architecture",
    "target file tree",
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
    "decision/tradeoff register",
    "over-orchestration review",
    "plan acceptance",
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


EXPENSIVE_PROOF_STRONG_TERMS = [
    "expensive-proof",
    "expensive proof",
    "replacement proof",
    "production replacement",
    "runtime replacement",
    "burn-in",
    "burn in",
    "final proof",
    "giant run",
    "long-run proof",
    "long run proof",
    "true e2e",
    "true-e2e",
    "end-to-end replacement",
]

EXPENSIVE_PROOF_CONTEXT_TERMS = [
    "agentic runtime",
    "agentic-system runtime",
    "runtime",
    "production",
    "replacement",
    "e2e",
    "end-to-end",
]

EXPENSIVE_PROOF_ACTION_TERMS = [
    "proof",
    "burn",
    "burn-in",
    "final",
    "canary",
    "soak",
    "p10",
    "p20",
    "hours",
    "expensive",
]

PRODUCTION_IMPLEMENTATION_TERMS = [
    "production implementation",
    "production/runtime",
    "runtime implementation",
    "unattended production",
    "long-running production",
    "long-running implementation goal",
    "external/irreversible",
    "external or irreversible",
    "unsafe/irreversible",
    "unsafe or irreversible",
    "irreversible stop",
    "external stop",
    "safe predecessor",
    "runnable safe next action",
]


def has_semantic_pattern_scope(text: str) -> bool:
    return any(term in text for term in SEMANTIC_PATTERN_SCOPE_TERMS)


def has_agentic_system_scope(text: str) -> bool:
    return any(term in text for term in AGENTIC_SYSTEM_TERMS)


def has_tier3_expensive_proof_scope(found: dict[str, str], tier: str) -> bool:
    if tier != "3":
        return False
    scan_sections = [
        "objective",
        "scope",
        "goal execution posture and delivery",
        "definition of done / operational outcome contract",
        "product / prd checklist",
        "task map / implementation graph",
        "verifiable subgoals and metrics",
        "parallelization plan",
        "testing adaptation gate",
        "tier decision",
        "risk-to-evidence map",
        "pre-launch confidence gate",
    ]
    text = normalize("\n".join(found.get(section, "") for section in scan_sections))
    if any(term in text for term in EXPENSIVE_PROOF_STRONG_TERMS):
        return True
    sentenceish_units = re.split(r"[.\n;|]+", text)
    return any(
        any(context in unit for context in EXPENSIVE_PROOF_CONTEXT_TERMS)
        and any(action in unit for action in EXPENSIVE_PROOF_ACTION_TERMS)
        for unit in sentenceish_units
    )


def has_production_implementation_scope(found: dict[str, str]) -> bool:
    scan_sections = [
        "objective",
        "scope",
        "goal execution posture and delivery",
        "definition of done / operational outcome contract",
        "product / prd checklist",
        "task map / implementation graph",
        "verifiable subgoals and metrics",
        "parallelization plan",
        "user expectation / surprise assessment",
        "risk-to-evidence map",
        "pre-launch confidence gate",
    ]
    text = normalize("\n".join(found.get(section, "") for section in scan_sections))
    return any(term in text for term in PRODUCTION_IMPLEMENTATION_TERMS)


def validate_unattended_production_approval_plan(found: dict[str, str], required: bool, errors: list[str]) -> None:
    section_name = "unattended production/runtime approval and safe-predecessor plan"
    section = found.get(section_name, "")
    if not required:
        return
    if not section:
        errors.append("production/runtime implementation scope requires Unattended production/runtime approval and safe-predecessor plan section")
        return
    if not section_has_substance(section):
        errors.append("required section lacks completed substance: Unattended production/runtime approval and safe-predecessor plan")
        return
    labels = [
        "Production/runtime implementation goal?",
        "Expected unattended window / operator absence",
        "Upfront approval packet path/status",
        "External/irreversible action categories considered",
        "Safe autonomous predecessor work decomposition",
        "Exact stop-before-external-action rule",
        "Active blocker definition",
        "Hard blocker after exhaustion definition",
        "Parent completion rule",
        "If no upfront approval needed, why",
    ]
    values = {label: require_field(section, label, errors) for label in labels}
    applies = values["Production/runtime implementation goal?"].lower().startswith("yes")
    if not applies:
        return
    approval = normalize(values["Upfront approval packet path/status"])
    if approval in {"none", "n/a", "not needed", "not applicable"}:
        errors.append("production/runtime implementation plans need an upfront approval packet path/status or explicit already-approved evidence")
    categories = normalize(values["External/irreversible action categories considered"])
    if not any(term in categories for term in ["external", "irreversible", "unsafe", "approval", "credential", "spend", "destructive"]):
        errors.append("upfront approval packet must consider external/irreversible/unsafe action categories")
    decomposition = normalize(values["Safe autonomous predecessor work decomposition"])
    if "safe" not in decomposition or "predecessor" not in decomposition:
        errors.append("safe predecessor decomposition must explicitly name safe predecessor work")
    stop_rule = normalize(values["Exact stop-before-external-action rule"])
    if not any(term in stop_rule for term in ["stop", "pause", "block", "ask"]):
        errors.append("stop-before-external-action rule must include stop/pause/block/ask behavior")
    if not any(term in stop_rule for term in ["external", "irreversible", "unsafe"]):
        errors.append("stop-before-external-action rule must name the external/irreversible/unsafe boundary")
    active = normalize(values["Active blocker definition"])
    if "runnable safe next action" not in active:
        errors.append("active blocker definition must mention runnable safe next action")
    hard = normalize(values["Hard blocker after exhaustion definition"])
    if "exhaust" not in hard or not any(term in hard for term in ["external", "irreversible", "unsafe", "approval"]):
        errors.append("hard blocker definition must require safe-action exhaustion and exact external/unsafe blocker")
    completion = normalize(values["Parent completion rule"])
    if "runnable safe next action" not in completion or "0" not in completion:
        errors.append("parent completion rule must require runnable safe next action count = 0")


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



DEAD_CODE_TOOL_TERMS = [
    "vulture",
    "knip",
    "ruff",
    "pyright",
    "mypy",
    "ts-prune",
    "depcheck",
    "eslint",
    "tsc",
    "grep",
    "git grep",
    "lint",
    "test",
]


def validate_verifiable_subgoals(found: dict[str, str], tier: str, errors: list[str]) -> None:
    if tier == "0":
        return
    section_name = "verifiable subgoals and metrics"
    section = found.get(section_name, "")
    if not section:
        return
    if not section_has_substance(section):
        errors.append("required section lacks completed substance: Verifiable subgoals and metrics")
        return
    rows = table_meaningful_rows(section)
    if len(rows) < 2:
        errors.append("Verifiable subgoals and metrics needs at least two meaningful subgoal rows")
    section_lower = normalize(section)
    for term in ["evidence", "metric", "score", "rubric", "owner", "done"]:
        if term not in section_lower:
            errors.append(f"Verifiable subgoals and metrics missing concept: {term}")
    if not re.search(r"\bG[0-9]+\b", section):
        errors.append("Verifiable subgoals and metrics must use stable subgoal IDs such as G1, G2")


def validate_parallelization_plan(found: dict[str, str], tier: str, errors: list[str]) -> None:
    if tier == "0":
        return
    section_name = "parallelization plan"
    section = found.get(section_name, "")
    if not section:
        return
    if not section_has_substance(section):
        errors.append("required section lacks completed substance: Parallelization plan")
        return
    section_lower = normalize(section)
    for term in ["critical path", "parallel", "serial", "write", "concurrency", "integration"]:
        if term not in section_lower:
            errors.append(f"Parallelization plan missing concept: {term}")
    if "subagent" not in section_lower and "unavailable" not in section_lower and "not authorized" not in section_lower:
        errors.append("Parallelization plan must state what happens if subagents are not authorized or unavailable")


def validate_runtime_agent_topology(found: dict[str, str], required: bool, errors: list[str]) -> None:
    section_name = "runtime agent topology / codex depth-thread policy"
    section = found.get(section_name, "")
    if not required:
        return
    if not section:
        errors.append("agentic/campaign scope requires Runtime agent topology / Codex depth-thread policy section")
        return
    if not section_has_substance(section):
        errors.append("required section lacks completed substance: Runtime agent topology / Codex depth-thread policy")
        return
    section_lower = normalize(section)
    if "not applicable because" in section_lower:
        errors.append("Runtime agent topology cannot be marked not applicable for agentic/campaign scope")
        return
    for label in [
        "Config source / observed source",
        "Standard campaign preset",
        "Current or planned `max_threads`",
        "Current or planned `max_depth`",
        "Role shape",
        "Does this plan need depth 3?",
        "If depth 3 is needed, prompt text and approval record path",
        "Deep-campaign preset",
        "Wider-campaign preset and separate approval rule",
        "Restore-to-default rule",
        "Child-agent depth policy",
    ]:
        require_field(section, label, errors)
    for term in ["max_threads", "max_depth", "6", "2", "8", "3", "approval", "restore", "l0", "l1", "l2"]:
        if term not in section_lower:
            errors.append(f"Runtime agent topology / Codex depth-thread policy missing concept: {term}")


def _field_text(section: str, label: str, errors: list[str]) -> str:
    return normalize(require_field(section, label, errors))


def validate_tier3_expensive_proof_preflight(found: dict[str, str], required: bool, errors: list[str]) -> None:
    section_name = "tier 3 expensive-proof plan-tree preflight"
    section = found.get(section_name, "")
    if not required:
        return
    if not section:
        errors.append(
            "Tier 3 expensive-proof/replacement/runtime proof scope requires Tier 3 expensive-proof plan-tree preflight section"
        )
        return
    if not section_has_substance(section):
        errors.append("required section lacks completed substance: Tier 3 expensive-proof plan-tree preflight")
        return

    section_lower = normalize(section)
    labels = [
        "Scope trigger / expensive-proof classification",
        "Risk/failure-class inventory",
        "Observability / telemetry preflight",
        "Phase-boundary / contract-fuzz preflight",
        "Burn-in proof plan",
        "Final-proof separation",
        "Stop/replan rules",
        "Child-plan/status-ledger structure",
        "Flat-plan exception?",
        "If flat-plan exception, recorded approval and validator-bypass reason",
    ]
    values = {label: _field_text(section, label, errors) for label in labels}

    for term in ["tier 3", "expensive", "proof"]:
        if term not in values["Scope trigger / expensive-proof classification"]:
            errors.append(f"expensive-proof classification must explicitly mention: {term}")

    risk_rows = table_meaningful_rows(values["Risk/failure-class inventory"] + "\n" + section)
    risk_text = values["Risk/failure-class inventory"]
    if "failure" not in risk_text or "risk" not in risk_text:
        errors.append("Risk/failure-class inventory must name risks and failure classes")
    if len(risk_rows) < 3 and len(re.findall(r"(?:^|[,;])\s*[^,;]+failure", risk_text)) < 3:
        errors.append("Risk/failure-class inventory needs at least three concrete failure-class rows/items")

    obs = values["Observability / telemetry preflight"]
    if not any(term in obs for term in ["telemetry", "observability", "trace", "log", "metric", "receipt"]):
        errors.append("Observability / telemetry preflight must name trace/log/metric/receipt evidence")
    if not any(term in obs for term in ["preflight", "before", "dry-run", "smoke"]):
        errors.append("Observability / telemetry preflight must be checked before burn-in/final proof")

    fuzz = values["Phase-boundary / contract-fuzz preflight"]
    for term in ["phase", "contract"]:
        if term not in fuzz:
            errors.append(f"Phase-boundary / contract-fuzz preflight missing: {term}")
    if not any(term in fuzz for term in ["fuzz", "negative", "adversarial", "malformed", "truncation", "boundary"]):
        errors.append("Phase-boundary / contract-fuzz preflight must include fuzz/negative/adversarial boundary coverage")

    burn = values["Burn-in proof plan"]
    final = values["Final-proof separation"]
    if not any(term in burn for term in ["burn-in", "burn in", "canary", "soak", "pilot"]):
        errors.append("Burn-in proof plan must name burn-in/canary/soak/pilot evidence")
    if "final" not in final or "proof" not in final:
        errors.append("Final-proof separation must explicitly name final proof")
    if not any(term in final for term in ["separate", "after", "distinct", "not the same", "not reuse"]):
        errors.append("Final-proof separation must state burn-in and final proof are distinct gates")

    stop = values["Stop/replan rules"]
    if not any(term in stop for term in ["stop", "abort", "pause"]):
        errors.append("Stop/replan rules must include an explicit stop/abort/pause action")
    if not any(term in stop for term in ["replan", "revise", "child plan", "subplan", "rca"]):
        errors.append("Stop/replan rules must include replan/revise/child-plan/RCA action")

    child = values["Child-plan/status-ledger structure"]
    exception = values["Flat-plan exception?"]
    exception_reason = values["If flat-plan exception, recorded approval and validator-bypass reason"]
    exception_yes = exception.startswith("yes")
    if exception_yes:
        if not any(term in exception_reason for term in ["approval", "approved", "bypass"]):
            errors.append("Flat-plan exception requires recorded approval and validator-bypass reason")
        if "benefit >> cost" not in exception_reason:
            errors.append("Flat-plan exception must justify benefit >> cost")
    else:
        for term in ["child", "status", "ledger"]:
            if term not in child:
                errors.append(f"Child-plan/status-ledger structure missing: {term}")
        if any(term in child for term in ["not applicable", "none", "no child", "flat"]):
            errors.append("Tier 3 expensive-proof scope cannot omit child-plan/status-ledger structure without a flat-plan exception")

    if "type0" in section_lower and "general" not in section_lower and "example" not in section_lower:
        errors.append("Tier 3 expensive-proof preflight must be general, not hardcoded to Type0")


def validate_testing_adaptation_gate(found: dict[str, str], tier: str, errors: list[str]) -> None:
    if tier == "0":
        return
    section_name = "testing adaptation gate"
    section = found.get(section_name, "")
    if not section:
        return
    if not section_has_substance(section):
        errors.append("required section lacks completed substance: Testing adaptation gate")
        return
    section_lower = normalize(section)
    for label in [
        "Failure streak threshold",
        "Systematic failure signal",
        "Material unexpected failure trigger",
        "Stop action",
        "RCA artifact",
        "Plan revision path",
        "RCA-driven scope decision",
        "Child/sub-uberplan appendix",
        "Parent plan append/merge actions",
        "Resume rule",
    ]:
        require_field(section, label, errors)
    if "five" not in section_lower and "5" not in section_lower:
        errors.append("Testing adaptation gate must stop before or at five consecutive clear failures")
    for term in ["clear", "failure", "test", "rca", "uberrca", "uberplan", "ubergoal", "resume", "unexpected", "scope", "append"]:
        if term not in section_lower:
            errors.append(f"Testing adaptation gate missing concept: {term}")


def validate_goal_execution_posture(found: dict[str, str], tier: str, errors: list[str]) -> None:
    if tier == "0":
        return
    section_name = "goal execution posture and delivery"
    section = found.get(section_name, "")
    if not section:
        return
    if not section_has_substance(section):
        errors.append("required section lacks completed substance: Goal execution posture and delivery")
        return
    section_lower = normalize(section)
    for label in [
        "Markdown plan file path",
        "Thread highlights to return",
        "Execution horizon",
        "Checkpoint cadence",
        "Work package granularity",
        "Uberslice exception?",
    ]:
        require_field(section, label, errors)
    path = require_field(section, "Markdown plan file path", errors)
    if path and ".md" not in path.lower():
        errors.append("Goal execution posture must name a durable .md plan file path")
    for term in ["thread", "highlight", "checkpoint"]:
        if term not in section_lower:
            errors.append(f"Goal execution posture missing concept: {term}")
    if tier in {"2", "3"} and "long-running" not in section_lower and "long running" not in section_lower:
        errors.append("Tier 2/3 uberplan contracts must frame the work as a long-running goal unless explicitly downgraded")
    if "20-minute" not in section_lower and "uberslice" not in section_lower:
        errors.append("Goal execution posture must explicitly reject or justify uberslice / 20-minute collapse")


def validate_user_expectation_surprise(found: dict[str, str], tier: str, errors: list[str]) -> None:
    if tier == "0":
        return
    section_name = "user expectation / surprise assessment"
    section = found.get(section_name, "")
    if not section:
        return
    if not section_has_substance(section):
        errors.append("required section lacks completed substance: User expectation / surprise assessment")
        return
    section_lower = normalize(section)
    for label in [
        "User-visible expectation inferred",
        "Evidence for expectation",
        "Planned actions that may surprise the user",
        "Assumptions that may be wrong",
        "Choices likely to conflict with user preference",
        "Ask/flag-before-proceeding triggers",
        "Final handoff expectation check",
    ]:
        require_field(section, label, errors)
    for term in ["user", "expect", "surprise", "evidence", "assumption"]:
        if term not in section_lower:
            errors.append(f"User expectation / surprise assessment missing concept: {term}")
    if "ask" not in section_lower and "flag" not in section_lower:
        errors.append("User expectation / surprise assessment must say what to ask or flag before proceeding")
    if "final" not in section_lower and "handoff" not in section_lower:
        errors.append("User expectation / surprise assessment must define a final handoff expectation check")


def validate_operational_outcome_contract(found: dict[str, str], tier: str, errors: list[str]) -> None:
    if tier == "0":
        return
    section_name = "definition of done / operational outcome contract"
    section = found.get(section_name, "")
    if not section:
        return
    if not section_has_substance(section):
        errors.append("required section lacks completed substance: Definition of Done / Operational Outcome Contract")
        return
    section_lower = normalize(section)
    for label in [
        "Intended operational outcome",
        "What counts as implemented/operational for this plan",
        "Real-system or target-system wiring required",
        "Tests/evals/live or target-runtime proof required",
        "What does NOT count as implementation",
        "Allowed terminal states",
        "Blocked terminal-state rule",
        "Re-scoped terminal-state rule",
    ]:
        require_field(section, label, errors)
    for term in [
        "operational",
        "blocked",
        "re_scoped_with_approval",
        "proof",
        "implementation",
        "readiness gate",
        "shadow-only",
    ]:
        if term not in section_lower:
            errors.append(f"Definition of Done / Operational Outcome Contract missing concept: {term}")
    terminal_states = require_field(section, "Allowed terminal states", errors).lower()
    for state in ["operational", "blocked", "re_scoped_with_approval"]:
        if state not in terminal_states:
            errors.append(f"Allowed terminal states must include: {state}")
    operational_claim = require_field(section, "What counts as implemented/operational for this plan", errors).lower()
    not_done = require_field(section, "What does NOT count as implementation", errors).lower()
    proof_only_terms = [
        "readiness gate",
        "safe adoption spine",
        "registry",
        "plan-only",
        "eval fixture",
        "local proof",
        "shadow-only",
        "shared parent proof",
        "shared spine",
    ]
    if any(term in operational_claim for term in proof_only_terms) and not any(term in not_done for term in proof_only_terms):
        errors.append("Operational outcome contract must not count proof-only/shared-spine artifacts as operational without excluding them in NOT DONE criteria")


HIERARCHICAL_SCOPE_TERMS = [
    "child plan",
    "child plans",
    "subplan",
    "subplans",
    "sub-plan",
    "sub-plans",
    "plan tree",
    "multi-item goal",
    "multiple operational outcomes",
    "parent goal",
    "execute all plans",
    "execute all child",
    "plans that generate plans",
    "recursive",
    "soho ten-plan",
    "ten-plan",
]


def has_hierarchical_scope(found: dict[str, str]) -> bool:
    scan_sections = [
        "objective",
        "scope",
        "goal execution posture and delivery",
        "definition of done / operational outcome contract",
        "product / prd checklist",
        "task map / implementation graph",
        "verifiable subgoals and metrics",
        "parallelization plan",
        "multi-agent plan",
        "risk-to-evidence map",
    ]
    scan_text = normalize("\n".join(found.get(section, "") for section in scan_sections))
    return any(term in scan_text for term in HIERARCHICAL_SCOPE_TERMS)


def validate_recursive_pseudocode(found: dict[str, str], required: bool, errors: list[str]) -> None:
    section_name = "recursive / hierarchical execution pseudocode"
    section = found.get(section_name, "")
    if not required:
        return
    if not section:
        errors.append("hierarchical plan scope requires Recursive / Hierarchical Execution Pseudocode section")
        return
    if not section_has_substance(section):
        errors.append("required section lacks completed substance: Recursive / Hierarchical Execution Pseudocode")
        return
    section_lower = normalize(section)
    if "```text" not in section_lower:
        errors.append("Recursive / Hierarchical Execution Pseudocode must include a fenced text pseudocode block")
    for term in [
        "child",
        "parent",
        "terminal_state",
        "operational",
        "blocked",
        "re_scoped_with_approval",
        "proof",
        "shared_parent_spine",
    ]:
        if term not in section_lower:
            errors.append(f"Recursive / Hierarchical Execution Pseudocode missing concept: {term}")
    for label in [
        "Hierarchy applies?",
        "Max depth / child-count budget before asking or blocking",
        "Child status table required?",
    ]:
        require_field(section, label, errors)
    rows = table_meaningful_rows(section)
    has_child_state_table = False
    for row in rows:
        row_blob = normalize(" ".join(row))
        if "operational" in row_blob and "blocked" in row_blob and "re_scoped_with_approval" in row_blob:
            has_child_state_table = True
            break
        if len(row) >= 4 and any(term in row_blob for term in ["child", "plan"]) and "terminal" in row_blob:
            has_child_state_table = True
            break
    field_value = require_field(section, "Child status table required?", errors).lower()
    if field_value.startswith("yes") and not has_child_state_table:
        errors.append("Recursive / Hierarchical Execution Pseudocode must include a child terminal-state table when required")


def validate_plan_tree_layout(found: dict[str, str], required: bool, errors: list[str]) -> None:
    section_name = "plan tree artifact layout"
    section = found.get(section_name, "")
    if not required:
        return
    if not section:
        errors.append("hierarchical plan scope requires Plan Tree Artifact Layout section")
        return
    if not section_has_substance(section):
        errors.append("required section lacks completed substance: Plan Tree Artifact Layout")
        return
    section_lower = normalize(section)
    for term in ["root", "index", "status ledger", "child", "receipt", "final acceptance", "shared proof"]:
        if term not in section_lower:
            errors.append(f"Plan Tree Artifact Layout missing concept: {term}")
    for label in [
        "Plan tree required?",
        "Root index path",
        "Status ledger path",
        "Child plans directory",
        "Receipts directory",
        "Final acceptance receipt path",
        "Split trigger met?",
        "Parent/shared proof cannot substitute for child proof?",
    ]:
        require_field(section, label, errors)
    path_blob = " ".join(
        require_field(section, label, errors).lower()
        for label in [
            "Root index path",
            "Status ledger path",
            "Child plans directory",
            "Receipts directory",
            "Final acceptance receipt path",
        ]
    )
    for required_path_term in ["index", "status", "ledger", "children", "receipts", "acceptance"]:
        if required_path_term not in path_blob:
            errors.append(f"Plan Tree Artifact Layout paths must include: {required_path_term}")
    rows = table_meaningful_rows(section)
    if not rows:
        errors.append("Plan Tree Artifact Layout needs at least one child plan row")


def validate_target_file_tree(found: dict[str, str], lower: str, tier: str, errors: list[str]) -> None:
    if tier == "0":
        return
    section_name = "target architecture / file tree"
    section = found.get(section_name, "")
    if not section:
        return
    if not section_has_substance(section):
        errors.append("required section lacks completed substance: Target architecture / file tree")
        return
    code_scope = has_code_or_topology_scope(lower)
    section_lower = normalize(section)
    explicitly_na = "not applicable because" in section_lower
    if explicitly_na:
        if code_scope:
            errors.append("Target architecture / file tree cannot be marked not applicable when plan indicates new/moved code, refactors, or package/dependency seams")
        return
    if code_scope and "```" not in section:
        errors.append("Target architecture / file tree must include a fenced target tree for code/topology/refactor work")
    for term in ["owning", "public", "private", "test", "avoid", "separation"]:
        if term not in section_lower:
            errors.append(f"Target architecture / file tree missing concept: {term}")


def validate_code_health_dead_code_plan(found: dict[str, str], lower: str, tier: str, errors: list[str]) -> None:
    if tier == "0":
        return
    section_name = "code-health / dead-code tool plan"
    section = found.get(section_name, "")
    if not section:
        return
    if not section_has_substance(section):
        errors.append("required section lacks completed substance: Code-health / dead-code tool plan")
        return
    section_lower = normalize(section)
    code_scope = has_code_or_topology_scope(lower)
    explicitly_na = "not applicable because" in section_lower
    if explicitly_na:
        if code_scope:
            errors.append("Code-health / dead-code tool plan cannot be marked not applicable for code/refactor/topology scope")
        return
    for term in ["stack", "tool", "dynamic", "candidate", "deletion", "defer"]:
        if term not in section_lower:
            errors.append(f"Code-health / dead-code tool plan missing concept: {term}")
    if code_scope and not any(term in section_lower for term in DEAD_CODE_TOOL_TERMS):
        errors.append("Code-health / dead-code tool plan must name at least one concrete stack tool or grep/git grep/lint/test fallback")
    if code_scope and "candidate" not in section_lower:
        errors.append("Code-health / dead-code tool plan must state static findings are candidates, not deletion authority")


def validate_decision_tradeoff_register(found: dict[str, str], tier: str, errors: list[str]) -> None:
    if tier == "0":
        return
    section_name = "decision / tradeoff / surprise register"
    section = found.get(section_name, "")
    if not section:
        return
    if not section_has_substance(section):
        errors.append("required section lacks completed substance: Decision / tradeoff / surprise register")
        return
    section_lower = normalize(section)
    rows = table_meaningful_rows(section)
    if len(rows) < 1:
        errors.append("Decision / tradeoff / surprise register needs at least one meaningful row")
    for term in ["issue", "tradeoff", "choice", "surprise", "risk", "follow-up"]:
        if term not in section_lower:
            errors.append(f"Decision / tradeoff / surprise register missing concept: {term}")


def validate_plan_acceptance_gate(found: dict[str, str], tier: str, errors: list[str]) -> None:
    if tier == "0":
        return
    section_name = "plan acceptance gate"
    section = found.get(section_name, "")
    if not section:
        return
    if not section_has_substance(section):
        errors.append("required section lacks completed substance: Plan acceptance gate")
        return
    section_lower = normalize(section)
    for term in ["openclaw", "agentic architecture", "thin-harness", "fat", "source authority", "topology", "dead-code", "tradeoff", "blocker"]:
        if term not in section_lower:
            errors.append(f"Plan acceptance gate missing concept: {term}")
    blockers_clear(section, errors)
    verdict = require_field(section, "Acceptance verdict", errors)
    if verdict and "proceed? yes" not in verdict.lower():
        errors.append("Plan acceptance gate verdict must explicitly say proceed? yes")


def validate_over_orchestration_review(found: dict[str, str], tier: str, errors: list[str]) -> None:
    if tier not in {"2", "3"}:
        return
    section_name = "pre-presentation over-orchestration review"
    section = found.get(section_name, "")
    if not section:
        return
    if not section_has_substance(section):
        errors.append("required section lacks completed substance: Pre-presentation over-orchestration review")
        return
    section_lower = normalize(section)
    for label in [
        "Uberslice / 20-minute collapse checked",
        "Unnecessary agents/lanes/templates/files removed",
        "Better context/tool/source fix considered before extra process",
        "Deterministic harness / regex / router creep checked",
        "Duplicate artifacts or planning bureaucracy removed",
        "Plan revisions made before presenting",
        "Review verdict",
    ]:
        require_field(section, label, errors)
    for term in ["20-minute", "agents", "templates", "context", "tool", "source", "deterministic", "revision"]:
        if term not in section_lower:
            errors.append(f"Pre-presentation over-orchestration review missing concept: {term}")
    verdict = require_field(section, "Review verdict", errors)
    if verdict and "present? yes" not in verdict.lower():
        errors.append("Pre-presentation over-orchestration review verdict must explicitly say present? yes")


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


def validate_agent_execution_proof_ladder(found: dict[str, str], required: bool, errors: list[str]) -> None:
    section_name = "agent execution proof ladder"
    section = found.get(section_name, "")
    if not required:
        return
    if not section:
        errors.append("agentic-system scope requires Agent execution proof ladder section")
        return
    if not section_has_substance(section):
        errors.append("required section lacks completed substance: Agent execution proof ladder")
        return
    section_lower = normalize(section)
    for label in [
        "Codex subagent proof target",
        "Skills/tools/context packet",
        "If Codex subagent proof fails",
        "Codex proof evidence",
        "OpenClaw or target-runtime proof target",
        "If OpenClaw or target-runtime proof fails",
        "Parity/double-proof standard",
        "Proof verdict",
    ]:
        require_field(section, label, errors)
    for term in ["codex", "subagent", "skill", "tool", "context", "parity"]:
        if term not in section_lower:
            errors.append(f"Agent execution proof ladder missing concept: {term}")
    if "openclaw" not in section_lower and "target-runtime" not in section_lower and "target runtime" not in section_lower:
        errors.append("Agent execution proof ladder must name OpenClaw or the target runtime")
    if "twice" not in section_lower and "double" not in section_lower and "two " not in section_lower:
        errors.append("Agent execution proof ladder must require two target-runtime parity proofs before readiness")
    verdict = require_field(section, "Proof verdict", errors).lower()
    if verdict and not any(term in verdict for term in ["proceed", "block", "spike"]):
        errors.append("Agent execution proof ladder verdict must say whether the plan proceeds, is blocked, or is a spike")


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
    validate_verifiable_subgoals(found, args.tier or "1", errors)
    validate_parallelization_plan(found, args.tier or "1", errors)
    validate_testing_adaptation_gate(found, args.tier or "1", errors)
    validate_goal_execution_posture(found, args.tier or "1", errors)
    validate_user_expectation_surprise(found, args.tier or "1", errors)
    validate_operational_outcome_contract(found, args.tier or "1", errors)
    hierarchical_scope = args.tier != "0" and has_hierarchical_scope(found)
    validate_recursive_pseudocode(found, hierarchical_scope, errors)
    validate_plan_tree_layout(found, hierarchical_scope, errors)
    production_implementation_scope = args.tier != "0" and has_production_implementation_scope(found)
    validate_unattended_production_approval_plan(found, production_implementation_scope, errors)
    expensive_proof_scope = has_tier3_expensive_proof_scope(found, args.tier or "1")
    validate_tier3_expensive_proof_preflight(found, expensive_proof_scope, errors)
    validate_target_file_tree(found, lower, args.tier or "1", errors)
    validate_repository_topology(found, lower, args.tier or "1", errors)
    validate_code_health_dead_code_plan(found, lower, args.tier or "1", errors)
    validate_decision_tradeoff_register(found, args.tier or "1", errors)
    validate_over_orchestration_review(found, args.tier or "1", errors)
    validate_plan_acceptance_gate(found, args.tier or "1", errors)

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
        found.get("parallelization plan", ""),
    ]))
    behavior_scope = args.agent_behavior or (args.tier != "0" and any(term in behavior_scan_text for term in behavior_terms))
    agentic_system_scope = args.tier != "0" and (behavior_scope or has_agentic_system_scope(behavior_scan_text))
    validate_runtime_agent_topology(found, agentic_system_scope or hierarchical_scope, errors)
    validate_thin_harness_rubric(found, agentic_system_scope, errors)
    validate_agent_execution_proof_ladder(found, agentic_system_scope, errors)
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
    if args.tier != "0" and has_code_or_topology_scope(lower):
        rubric_lower = normalize(rubric)
        if "repository topology" not in rubric_lower:
            errors.append("acceptance rubric must include repository topology when plan indicates new/moved code or package seams")
        if "target file tree" not in rubric_lower:
            errors.append("acceptance rubric must include target file tree when plan indicates new/moved code, refactors, or package seams")
        if "dead code" not in rubric_lower:
            errors.append("acceptance rubric must include dead-code/code-health evidence when plan indicates code/refactor/topology scope")
    if args.tier != "0":
        rubric_lower = normalize(rubric)
        if "operational outcome" not in rubric_lower:
            errors.append("acceptance rubric must include operational outcome / Definition of Done evidence for substantial plans")
        if hierarchical_scope and "recursive" not in rubric_lower:
            errors.append("acceptance rubric must include recursive pseudocode / child terminal-state evidence for hierarchical plans")
        if hierarchical_scope and "plan tree artifact layout" not in rubric_lower:
            errors.append("acceptance rubric must include plan tree artifact layout evidence for hierarchical plans")
        if expensive_proof_scope and "tier 3 expensive-proof preflight" not in rubric_lower:
            errors.append("acceptance rubric must include Tier 3 expensive-proof preflight evidence")
        if expensive_proof_scope and "burn-in" not in rubric_lower:
            errors.append("acceptance rubric must include burn-in vs final proof evidence")
        if production_implementation_scope and "production implementation blocker gate" not in rubric_lower:
            errors.append("acceptance rubric must include production implementation blocker gate evidence")

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
