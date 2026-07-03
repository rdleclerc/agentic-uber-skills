#!/usr/bin/env python3
"""Validate a completed ubergoal final acceptance report.

By default this validates completed artifacts, not blank templates. Use
--allow-template only for bundled template structure checks.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "implementation summary",
    "files changed",
    "scope fidelity verdict",
    "rubric scores",
    "commands and artifacts",
    "spec fidelity and standards review",
    "claim-state ledger",
    "planning review reconciliation",
    "user expectation / surprise delta",
    "agent advocate final check",
    "architecture steward final check",
    "adversarial acceptance check",
    "confidence verdict",
]

EVIDENCE_TERMS = [
    "unit",
    "regression",
    "integration",
    "ui/browser",
    "eval",
    "architecture",
    "topology",
    "dependency",
    "dead-code",
    "security",
    "privacy",
    "concurrency",
    "idempotency",
]

CLAIM_STATES = {
    "implemented",
    "tested",
    "operational",
    "live",
    "adopted",
    "proof-only",
    "shadow-only",
    "blocked",
    "re_scoped_with_approval",
}
HIGH_CLAIM_STATES = {"operational", "live", "adopted"}
LOWER_CLAIM_STATES = {"implemented", "tested", "proof-only", "shadow-only"}
GENERIC_DONE_STATES = {"done", "ready", "complete", "yes", "success", "passed"}
PROOF_ONLY_TOKENS = [
    "proof-only",
    "shadow-only",
    "local-safe-proof",
    "local proof",
    "shared-spine",
    "shared spine",
    "shared parent proof",
    "safe proof spine",
    "readiness gate",
    "registry",
    "plan-only",
    "eval fixture",
]
ACCEPTANCE_STATUSES = {"accepted", "rejected", "blocked_with_failure_intake"}
INTAKE_FIELDS = ["failure_case_id", "case_updated", "not_applicable_with_reason"]
INTAKE_PLACEHOLDERS = {"", "todo", "tbd", "n/a", "none", "<id>", "<text>"}
HIGH_STATE_PROOF_TERMS = {
    "operational": ["target", "runtime", "wired", "validator", "unit", "regression", "smoke", "real-system", "system"],
    "live": ["live", "production", "runtime", "route", "log", "traffic", "user-facing"],
    "adopted": ["adopted", "default", "routing", "canonical", "migration", "retired", "install", "sync"],
}
DEFECT_FIX_RE = re.compile(r"\bfix(?:e[sd])?\b|\bfixing\b", re.I)
DEFECT_TERM_RE = re.compile(r"\b(?:bug|defect|regression)s?\b", re.I)
FAKE_STANDIN_RE = re.compile(r"\b(?:fake|fakes|stub|stubs|mock|mocks|mocked)\b", re.I)
EXTERNAL_INTERFACE_RE = re.compile(
    r"\b(?:external|interface|api|service|provider|integration|client|database|db|slack|gmail|launchd)\b",
    re.I,
)
RECEIPT_PLACEHOLDERS = {"", "todo", "tbd", "yes/no", "<text>"}
RED_RECEIPT_TERMS = {"command", "output", "log", "fixture", "test", "before", "red", "stdout", "stderr", "artifact"}


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


def require_field(text: str, label: str, errors: list[str]) -> str:
    escaped = re.escape(label)
    separator = r"[ \t]*(?::)?[ \t]*" if label.endswith("?") else r"[ \t]*:[ \t]*"
    pattern = re.compile(rf"^[ \t]*-[ \t]*{escaped}{separator}(.+?)[ \t]*$", re.I | re.M)
    match = pattern.search(text)
    if not match:
        errors.append(f"missing field: {label}")
        return ""
    value = match.group(1).strip()
    if not value or value.lower() in {"yes/no", "tbd", "todo", "n/a"}:
        errors.append(f"empty or placeholder field: {label}")
    return value


def optional_field(text: str, label: str) -> str:
    pattern = re.compile(rf"^[ \t]*(?:-[ \t]*)?{re.escape(label)}[ \t]*:[ \t]*(.+?)[ \t]*$", re.I | re.M)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def claim_segments(text: str) -> list[str]:
    """Return conservative line/sentence chunks for natural-language heuristics."""
    segments: list[str] = []
    for line in text.splitlines():
        for segment in re.split(r"(?<=[.!?])\s+", line):
            if segment.strip():
                segments.append(segment.strip())
    return segments


def claims_defect_fix(text: str) -> bool:
    """Conservative trigger: the same sentence/paragraph must claim fix + bug/defect/regression."""
    return any(DEFECT_FIX_RE.search(segment) and DEFECT_TERM_RE.search(segment) for segment in claim_segments(text))


def mentions_external_fake_standin(text: str) -> bool:
    """Trigger only when fake/stub/mock language is tied to an external-interface term."""
    return any(FAKE_STANDIN_RE.search(segment) and EXTERNAL_INTERFACE_RE.search(segment) for segment in claim_segments(text))


def receipt_value_is_present(value: str, *, allow_na: bool = False) -> bool:
    low = normalize(value)
    if allow_na and low == "n/a":
        return True
    return bool(value.strip()) and low not in RECEIPT_PLACEHOLDERS and low not in INTAKE_PLACEHOLDERS


def red_receipt_is_usable(value: str) -> bool:
    if not receipt_value_is_present(value):
        return False
    low = normalize(value)
    return "`" in value or "/" in value or any(term in low for term in RED_RECEIPT_TERMS)


def acceptance_status(text: str, errors: list[str]) -> str:
    value = optional_field(text, "acceptance_status")
    if not value:
        return "accepted"
    normalized = normalize(value)
    if normalized not in ACCEPTANCE_STATUSES:
        errors.append(f"invalid acceptance_status: {value}")
        return normalized
    return normalized


def validate_failure_intake(text: str, status: str, errors: list[str]) -> tuple[str, str] | None:
    present: list[tuple[str, str]] = []
    for field in INTAKE_FIELDS:
        value = optional_field(text, field)
        if value and normalize(value) not in INTAKE_PLACEHOLDERS:
            present.append((field, value))
    allowed = INTAKE_FIELDS
    if status == "blocked_with_failure_intake":
        allowed = ["failure_case_id", "case_updated"]
        disallowed = [field for field, _value in present if field not in allowed]
        if disallowed:
            errors.append("blocked_with_failure_intake requires failure_case_id or case_updated, not not_applicable_with_reason")
    if len(present) != 1:
        grammar = "failure_case_id | case_updated"
        if status != "blocked_with_failure_intake":
            grammar = "failure_case_id | case_updated | not_applicable_with_reason"
        errors.append(
            "failure intake requires exactly one non-empty field: "
            f"{grammar}"
        )
        return None
    field, value = present[0]
    if field not in allowed:
        return None
    return field, value


def warn_missing_failure_case(referenced: tuple[str, str] | None, cases_dir: Path | None, warnings: list[str]) -> None:
    if cases_dir is None or referenced is None:
        return
    field, value = referenced
    if field != "failure_case_id":
        return
    case_id = value.strip()
    if not case_id:
        return
    if not (cases_dir / f"{case_id}.md").exists():
        warnings.append(f"failure_case_id has no case file under {cases_dir}: {case_id}")


def validate_defect_fix_receipt(text: str, errors: list[str]) -> None:
    if not claims_defect_fix(text):
        return
    reproduced_red = optional_field(text, "reproduced_red")
    no_repro_reason = optional_field(text, "no_repro_reason")
    if red_receipt_is_usable(reproduced_red) or receipt_value_is_present(no_repro_reason):
        return
    errors.append(
        "defect-fix claim requires reproduced_red with command/output evidence "
        "or no_repro_reason"
    )


def validate_interface_shape_receipt(text: str, errors: list[str]) -> None:
    if not mentions_external_fake_standin(text):
        return
    value = optional_field(text, "interface_shape_receipt")
    if receipt_value_is_present(value, allow_na=True):
        return
    errors.append("external fake/stub/mock stand-in requires interface_shape_receipt")


def validate_terminal_failure_report(found: dict[str, str], full_text: str, status: str, errors: list[str]) -> None:
    if status not in {"rejected", "blocked_with_failure_intake"}:
        return
    status_line = optional_field(full_text, "acceptance_status")
    if not status_line:
        errors.append("terminal failure report missing acceptance_status line")
    candidate_sections = [
        found.get("adversarial acceptance check", ""),
        found.get("confidence verdict", ""),
        found.get("findings", ""),
        found.get("blockers", ""),
        found.get("rubric scores", ""),
    ]
    combined = "\n".join(section for section in candidate_sections if section)
    if not meaningful_lines(combined):
        errors.append("terminal failure report needs a truthful blocker/finding section")
        return
    lower = normalize(combined)
    if not any(term in lower for term in ["blocker", "finding", "reject", "rejected", "blocked", "fail", "missing"]):
        errors.append("terminal failure report blocker/finding section must name the blocker or finding")
    if status == "rejected" and "no material blockers" in lower:
        errors.append("rejected acceptance report cannot claim no material blockers")


def meaningful_lines(section: str) -> list[str]:
    lines: list[str] = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        low = stripped.lower()
        if stripped in {"-", "|  |  |", "|  |  |  |", "|  |  |  |  |"}:
            continue
        if re.match(r"^\|\s*-+", low):
            continue
        if re.match(r"^\|?\s*(dimension|layer|---)", low):
            continue
        if re.match(r"^-\s*[^:]{1,80}:\s*$", stripped):
            continue
        if any(phrase in low for phrase in ["try to prove", "confirm every", "for agent behavior", "confirm the implementation"]):
            continue
        lines.append(stripped)
    return lines


def parse_rubric_rows(section: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in section.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        first = cells[0].lower()
        if first in {"dimension", "---"} or set(first) <= {"-", ":"}:
            continue
        rows.append({"dimension": cells[0], "score": cells[1], "evidence": cells[2], "gap": cells[3]})
    return rows


def score_value(raw: str) -> int | None:
    match = re.fullmatch(r"\s*(?:\*\*)?([0-3])(?:\*\*)?\s*", raw)
    if not match:
        return None
    return int(match.group(1))


def table_rows(section: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in section.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells or all(not cell or set(cell) <= {"-", ":"} for cell in cells):
            continue
        first = cells[0].strip().lower()
        if first in {"dimension", "layer", "workstream/child", "---"} or set(first) <= {"-", ":"}:
            continue
        rows.append(cells)
    return rows


def extract_claim_state(raw: str) -> str | None:
    low = normalize(raw)
    for state in sorted(CLAIM_STATES, key=len, reverse=True):
        if state in low:
            return state
    if low in GENERIC_DONE_STATES:
        return "generic"
    return None


def validate_claim_state_ledger(found: dict[str, str], full_text: str, errors: list[str]) -> None:
    section = found.get("claim-state ledger", "")
    if not section:
        return
    if not meaningful_lines(section):
        errors.append("Claim-state ledger lacks completed substance")
        return
    for label in [
        "Operational Outcome Contract source",
        "Highest state claimed in final handoff",
        "Highest state actually proven",
        "Any lower-state child limiting parent completion",
        "Wording that must be avoided in final handoff",
        "Proof-only / shadow-only / local-safe-proof / shared-spine evidence claimed as operational?",
        "Multi-child goal?",
        "Plan tree artifacts inspected, if applicable",
    ]:
        require_field(section, label, errors)

    rows = table_rows(section)
    if not rows:
        errors.append("Claim-state ledger needs at least one workstream/child table row")
    for row in rows:
        if len(row) < 5:
            errors.append(f"claim-state row has too few cells: {' | '.join(row)}")
            continue
        target_raw = row[1]
        accepted_raw = row[2]
        evidence = normalize(row[3])
        gap = normalize(row[4])
        target_state = extract_claim_state(target_raw)
        accepted_state = extract_claim_state(accepted_raw)
        if accepted_state is None:
            errors.append(f"claim-state row missing accepted state: {row[0]}")
            continue
        if accepted_state == "generic":
            errors.append(f"claim-state row uses generic completion language instead of claim state: {row[0]}={accepted_raw}")
            continue
        if accepted_state in HIGH_CLAIM_STATES:
            required_terms = HIGH_STATE_PROOF_TERMS[accepted_state]
            if not any(term in evidence for term in required_terms):
                errors.append(f"{accepted_state} claim lacks state-specific proof terms for row: {row[0]}")
        if target_state in HIGH_CLAIM_STATES and accepted_state in LOWER_CLAIM_STATES and gap in {"", "none", "n/a", "no gap"}:
            errors.append(f"target {target_state} row accepted as {accepted_state} needs named residual gap/blocker: {row[0]}")
        if accepted_state == "blocked" and gap in {"", "none", "n/a", "no gap"}:
            errors.append(f"blocked claim-state row needs blocker/gap evidence: {row[0]}")

    proof_claim = require_field(section, "Proof-only / shadow-only / local-safe-proof / shared-spine evidence claimed as operational?", errors).lower()
    final_recommendation = require_field(full_text, "Goal completion recommendation", errors).lower()
    if proof_claim.startswith("yes") and any(term in final_recommendation for term in ["complete", "ready", "accept"]):
        errors.append("cannot recommend completion while proof-only/shared-spine evidence is claimed as operational")


def validate_spec_fidelity_and_standards_review(found: dict[str, str], errors: list[str]) -> None:
    section = found.get("spec fidelity and standards review", "")
    if not section:
        return
    if not meaningful_lines(section):
        errors.append("Spec fidelity and standards review lacks completed substance")
        return
    for label in [
        "Spec source",
        "Standards sources inspected",
        "Spec fidelity verdict",
        "Repo standards verdict",
        "If spec source missing, standards-only review not treated as product correctness?",
        "Unapproved scope creep found?",
    ]:
        require_field(section, label, errors)
    rows = table_rows(section)
    axes = {normalize(row[0]) for row in rows if row}
    if "spec fidelity" not in axes:
        errors.append("Spec fidelity and standards review needs a Spec fidelity table row")
    if "repo standards" not in axes:
        errors.append("Spec fidelity and standards review needs a Repo standards table row")


def blockers_clear(text: str, errors: list[str], label: str = "Material blockers") -> None:
    value = require_field(text, label, errors)
    if not value:
        return
    if value.lower() not in {"none", "no", "none.", "resolved", "no material blockers"}:
        errors.append(f"{label} is not clear: {value}")


NEW_MOVED_OR_TOPOLOGY_PATTERNS = [
    r"\bnew/moved code\b",
    r"\bnew/moved code files?\b",
    r"\bnew (?:module|package|file|script|validator)\b",
    r"\badd(?:s|ed|ing)? (?:a )?(?:new )?(?:module|package|file|script|validator)\b",
    r"\broot[- ]level (?:module|file)\b",
    r"\bmove(?:s|d|ing)? (?:code|module|file|package)\b",
    r"\bpackage move\b",
    r"\brefactor\b",
    r"\bpackage seam (?:change|changes|changed)\b",
    r"\bpackage boundary (?:change|changes|changed)\b",
    r"\bimport boundary\b",
    r"\bdependency boundary\b",
]


def has_new_moved_or_topology_scope(full_text: str) -> bool:
    return any(re.search(pattern, full_text, re.I) for pattern in NEW_MOVED_OR_TOPOLOGY_PATTERNS)


def find_rubric_row(rows: list[dict[str, str]], dimension: str) -> dict[str, str] | None:
    wanted = normalize(dimension)
    for row in rows:
        if normalize(row["dimension"]) == wanted:
            return row
    return None


def evidence_is_not_applicable(text: str) -> bool:
    low = normalize(text)
    return "not applicable" in low or "no code files" in low or "no new/moved code" in low


BOUNDARY_SENTINEL_TERMS = [
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

RUNTIME_TOPOLOGY_TERMS = [
    "campaign",
    "plan-tree",
    "multi-agent",
    "subagent",
    "max_threads",
    "max_depth",
    "depth-3",
    "l0",
    "l1",
    "l2",
]

EXPENSIVE_PROOF_TERMS = [
    "expensive-proof",
    "expensive proof",
    "replacement proof",
    "production replacement",
    "runtime replacement",
    "burn-in",
    "burn in",
    "final proof",
    "canary expansion",
    "soak",
    "true e2e",
    "true-e2e",
]

PRODUCTION_IMPLEMENTATION_TERMS = [
    "production implementation",
    "production/runtime",
    "runtime implementation",
    "unattended production",
    "long-running production",
    "long-running implementation goal",
    "external or irreversible",
    "irreversible stop",
    "external stop",
    "safe predecessor",
    "runnable safe next action",
    "active blocker",
    "active_blocked",
    "hard-blocked-after-exhaustion",
    "hard_blocked_after_safe_action_exhaustion",
]


def has_production_implementation_acceptance_scope(full_text: str) -> bool:
    text = normalize(full_text)
    return any(term in text for term in PRODUCTION_IMPLEMENTATION_TERMS)


def parse_nonnegative_int(raw: str, label: str, errors: list[str]) -> int | None:
    match = re.search(r"\b([0-9]+)\b", raw or "")
    if not match:
        errors.append(f"{label} must contain a nonnegative integer")
        return None
    return int(match.group(1))


def yesish(raw: str) -> bool:
    return normalize(raw).startswith(("yes", "true", "0 ", "0."))


def noish(raw: str) -> bool:
    return normalize(raw).startswith(("no", "none", "0", "n/a", "not applicable"))


def has_semantic_pattern_scope(text: str) -> bool:
    return any(term in text for term in SEMANTIC_PATTERN_SCOPE_TERMS)


def validate_regex_keyword_semantic_acceptance(found: dict[str, str], errors: list[str]) -> None:
    section = found.get("regex / keyword semantic gate final check", "")
    if not section:
        errors.append("agentic or regex/keyword acceptance requires Regex / keyword semantic gate final check section")
        return
    section_lower = normalize(section)
    if not meaningful_lines(section):
        errors.append("Regex / keyword semantic gate final check lacks completed substance")
        return
    for term in ["regex", "keyword", "mechanical", "candidate", "semantic authority", "natural language"]:
        if term not in section_lower:
            errors.append(f"Regex / keyword semantic gate final check missing: {term}")
    if "unapproved semantic authority" not in section_lower and "no semantic authority" not in section_lower:
        errors.append("Regex / keyword semantic gate final check must state no unapproved semantic authority")
    if "eval" not in section_lower and "replay" not in section_lower:
        errors.append("Regex / keyword semantic gate final check must mention eval/replay coverage")
    if "rollback" not in section_lower:
        errors.append("Regex / keyword semantic gate final check must mention rollback")


def validate_agent_boundary_acceptance(found: dict[str, str], errors: list[str]) -> None:
    section = found.get("agent boundary contract final check", "")
    if not section:
        errors.append("agent behavior acceptance requires Agent Boundary Contract final check section")
        return
    section_lower = normalize(section)
    if not meaningful_lines(section):
        errors.append("Agent Boundary Contract final check lacks completed substance")
        return
    for term in ["shape", "authority", "isolation", "failure", "observability", "replay", "eval", "evidence"]:
        if term not in section_lower:
            errors.append(f"Agent Boundary Contract final check missing: {term}")
    if "sentinel" not in section_lower:
        errors.append("Agent Boundary Contract final check must mention relevant sentinel probes")
    if not any(term in section_lower for term in BOUNDARY_SENTINEL_TERMS):
        errors.append("Agent Boundary Contract final check must name at least one recurring failure probe")


def validate_user_expectation_delta(found: dict[str, str], errors: list[str]) -> None:
    section = found.get("user expectation / surprise delta", "")
    if not section:
        return
    section_lower = normalize(section)
    for label in [
        "Expected outcome inferred before/during plan",
        "Evidence for expectation",
        "Actual implementation/result",
        "Differences or surprises",
        "Material mismatch requiring user approval",
        "Final handoff wording",
    ]:
        require_field(section, label, errors)
    for term in ["expect", "evidence", "actual", "surprise", "mismatch", "handoff"]:
        if term not in section_lower:
            errors.append(f"User expectation / surprise delta missing: {term}")
    mismatch = require_field(section, "Material mismatch requiring user approval", errors).lower()
    if mismatch and not any(term in mismatch for term in ["no", "none", "approved", "needs approval", "flagged", "blocked"]):
        errors.append("User expectation / surprise delta must say whether material mismatch is none, approved, flagged, or blocked")


def validate_runtime_topology_acceptance(found: dict[str, str], full_text: str, required: bool, errors: list[str]) -> None:
    if not required and not any(term in normalize(full_text) for term in RUNTIME_TOPOLOGY_TERMS):
        return
    section = found.get("runtime agent topology acceptance", "")
    if not section:
        errors.append("campaign/subagent acceptance requires Runtime agent topology acceptance section")
        return
    section_lower = normalize(section)
    if "not applicable because" in section_lower and required:
        errors.append("Runtime agent topology acceptance cannot be marked not applicable for agent-behavior/campaign scope")
        return
    for label in [
        "Config source / observed source",
        "Topology mode",
        "Current `max_threads`",
        "Current `max_depth`",
        "Role shape",
        "Depth-3 escalation used?",
        "User approval evidence for depth/thread escalation",
        "Restore target",
        "Restore proof / blocker",
        "Child-agent depth policy",
        "Topology acceptance verdict",
    ]:
        require_field(section, label, errors)
    for term in ["max_threads", "max_depth", "role", "depth", "approval", "restore", "child-agent"]:
        if term not in section_lower:
            errors.append(f"Runtime agent topology acceptance missing: {term}")
    depth = normalize(require_field(section, "Current `max_depth`", errors))
    mode = normalize(require_field(section, "Topology mode", errors))
    approval = normalize(require_field(section, "User approval evidence for depth/thread escalation", errors))
    restore = normalize(require_field(section, "Restore target", errors))
    restore_proof = normalize(require_field(section, "Restore proof / blocker", errors))
    if mode in {"deep_8_3", "wide_10_3"} or depth == "3":
        if "approval" not in approval and "approved" not in approval:
            errors.append("depth-3 acceptance requires explicit approval evidence")
        if "6/2" not in restore and "max_threads=6" not in restore:
            errors.append("depth-3 acceptance requires restore target to default 6/2")
        if not restore_proof or restore_proof.lower() in {"none", "n/a", "todo", "tbd"}:
            errors.append("depth-3 acceptance requires restore proof or exact blocker")


def has_expensive_proof_acceptance_scope(full_text: str) -> bool:
    text = normalize(full_text)
    return any(term in text for term in EXPENSIVE_PROOF_TERMS)


def validate_expensive_proof_acceptance(found: dict[str, str], required: bool, errors: list[str]) -> None:
    if not required:
        return
    section = found.get("tier 3 expensive-proof acceptance", "")
    if not section:
        errors.append("Tier 3 expensive-proof/replacement proof requires Tier 3 expensive-proof acceptance section")
        return
    if not meaningful_lines(section):
        errors.append("Tier 3 expensive-proof acceptance lacks completed substance")
        return
    section_lower = normalize(section)
    for label in [
        "Expensive-proof scope applies?",
        "Plan validator command/result",
        "Risk/failure-class inventory inspected",
        "Observability / telemetry preflight evidence",
        "Phase-boundary / contract-fuzz preflight evidence",
        "Burn-in vs final-proof separation evidence",
        "Stop/replan evidence",
        "Child-plan/status-ledger evidence",
        "Flat-plan exception / bypass approval",
        "Expensive-proof acceptance verdict",
    ]:
        require_field(section, label, errors)
    for term in ["validator", "risk", "observability", "telemetry", "phase", "contract", "burn-in", "final", "stop", "replan"]:
        if term not in section_lower:
            errors.append(f"Tier 3 expensive-proof acceptance missing: {term}")
    child = normalize(require_field(section, "Child-plan/status-ledger evidence", errors))
    bypass = normalize(require_field(section, "Flat-plan exception / bypass approval", errors))
    if not all(term in child for term in ["child", "status", "ledger"]):
        if not any(term in bypass for term in ["approval", "approved", "bypass"]):
            errors.append("flat expensive-proof acceptance requires child/status ledger evidence or approved bypass")
    verdict = normalize(require_field(section, "Expensive-proof acceptance verdict", errors))
    if "accept" not in verdict and "pass" not in verdict:
        errors.append("Expensive-proof acceptance verdict must explicitly pass/accept or block")


def validate_production_implementation_blocker_gate(found: dict[str, str], required: bool, errors: list[str]) -> None:
    if not required:
        return
    section_name = "production implementation blocker gate"
    section = found.get(section_name, "")
    if not section:
        errors.append("production/runtime implementation acceptance requires Production implementation blocker gate section")
        return
    if not meaningful_lines(section):
        errors.append("Production implementation blocker gate lacks completed substance")
        return

    labels = [
        "Production implementation goal?",
        "Upfront approval packet status",
        "Required child count",
        "Operational or user-rescoped child count",
        "Hard-blocked-after-safe-action-exhaustion child count",
        "Active blocked child count",
        "Runnable safe next action count",
        "Safe autonomous predecessor work exhausted?",
        "Parent completion allowed?",
        "Next safe action if parent completion is not allowed",
    ]
    values = {label: require_field(section, label, errors) for label in labels}
    applies = normalize(values["Production implementation goal?"]).startswith("yes")
    if not applies:
        return

    active_count = parse_nonnegative_int(values["Active blocked child count"], "Active blocked child count", errors)
    runnable_count = parse_nonnegative_int(values["Runnable safe next action count"], "Runnable safe next action count", errors)
    required_count = parse_nonnegative_int(values["Required child count"], "Required child count", errors)
    operational_count = parse_nonnegative_int(
        values["Operational or user-rescoped child count"],
        "Operational or user-rescoped child count",
        errors,
    )
    hard_count = parse_nonnegative_int(
        values["Hard-blocked-after-safe-action-exhaustion child count"],
        "Hard-blocked-after-safe-action-exhaustion child count",
        errors,
    )

    if active_count not in {None, 0}:
        errors.append("production implementation parent cannot complete with active blocked children")
    if runnable_count not in {None, 0}:
        errors.append("production implementation parent cannot complete while runnable safe next actions remain")

    parent_allowed = normalize(values["Parent completion allowed?"])
    if not parent_allowed.startswith("yes"):
        errors.append("Production implementation blocker gate must explicitly allow parent completion only after active/runnable counts are zero")

    if hard_count and hard_count > 0:
        exhausted = normalize(values["Safe autonomous predecessor work exhausted?"])
        if not exhausted.startswith("yes"):
            errors.append("hard-blocked production children require safe autonomous predecessor work exhausted? yes")

    if None not in {required_count, operational_count, hard_count} and (operational_count or 0) + (hard_count or 0) < (required_count or 0):
        errors.append("production implementation child counts do not cover the required child count")

    rows = table_rows(section)
    data_rows = [row for row in rows if row and normalize(row[0]) not in {"child id", "child"}]
    if not data_rows:
        errors.append("Production implementation blocker gate needs at least one child row")
        return
    for row in data_rows:
        if len(row) < 7:
            errors.append(f"production blocker row has too few cells: {' | '.join(row)}")
            continue
        child = row[0]
        classification = normalize(row[2])
        runnable = normalize(row[3])
        exhaustion = normalize(row[4])
        blocker = normalize(row[5])
        unblock = normalize(row[6])
        if "active_blocked" in classification or "active blocked" in classification:
            errors.append(f"production child remains active-blocked: {child}")
        if runnable.startswith("yes") or "yes" in runnable[:12]:
            errors.append(f"production child has runnable safe next actions: {child}")
        if "hard_blocked_after_safe_action_exhaustion" in classification or "hard-blocked-after" in classification:
            if "exhaust" not in exhaustion:
                errors.append(f"hard-blocked child lacks safe-predecessor exhaustion evidence: {child}")
            if not any(term in blocker for term in ["external", "approval", "unsafe", "irreversible", "credential", "owner"]):
                errors.append(f"hard-blocked child lacks exact external/unsafe blocker: {child}")
            if unblock in {"", "none", "n/a", "no gap"}:
                errors.append(f"hard-blocked child needs next unblock owner/action: {child}")


def validate_safe_work_exhaustion_review(found: dict[str, str], required: bool, errors: list[str]) -> None:
    if not required:
        return
    section_name = "safe-work exhaustion adversarial review"
    section = found.get(section_name, "")
    if not section:
        errors.append("production/runtime implementation acceptance requires Safe-work exhaustion adversarial review section")
        return
    if not meaningful_lines(section):
        errors.append("Safe-work exhaustion adversarial review lacks completed substance")
        return

    labels = [
        "Review scope applies?",
        "Blocked children inspected",
        "Plausible safe next actions enumerated?",
        "Any runnable safe next action found?",
        "If runnable safe action found, parent completion blocked?",
        "Reviewer conclusion",
    ]
    values = {label: require_field(section, label, errors) for label in labels}
    applies = normalize(values["Review scope applies?"]).startswith("yes")
    if not applies:
        return

    enumerated = normalize(values["Plausible safe next actions enumerated?"])
    if not enumerated.startswith("yes"):
        errors.append("Safe-work exhaustion adversarial review must enumerate plausible safe next actions for blocked children")
    found_runnable = normalize(values["Any runnable safe next action found?"])
    if not found_runnable.startswith("no"):
        errors.append("Safe-work exhaustion adversarial review found runnable safe next actions; parent completion must be blocked")
    conclusion = normalize(values["Reviewer conclusion"])
    for term in ["safe", "action", "exhaust"]:
        if term not in conclusion:
            errors.append(f"Safe-work exhaustion reviewer conclusion missing: {term}")

    rows = table_rows(section)
    data_rows = [row for row in rows if row and normalize(row[0]) not in {"blocked child", "child"}]
    if not data_rows:
        errors.append("Safe-work exhaustion adversarial review needs blocked-child rows or an explicit none row")
        return
    for row in data_rows:
        if len(row) < 5:
            errors.append(f"safe-work exhaustion row has too few cells: {' | '.join(row)}")
            continue
        child = normalize(row[0])
        if child in {"none", "no blocked children"}:
            continue
        action = normalize(row[1])
        evidence = normalize(row[2])
        verdict = normalize(row[3])
        followup = normalize(row[4])
        if not any(term in action for term in ["safe", "action", "dry-run", "validation", "test", "audit", "inspect", "rehearsal", "none"]):
            errors.append(f"safe-work exhaustion row must name plausible safe action considered: {row[0]}")
        if "exhaust" not in evidence and "not safe" not in evidence and "unsafe" not in evidence and "none" not in evidence:
            errors.append(f"safe-work exhaustion row lacks exhaustion/not-safe evidence: {row[0]}")
        if "runnable_safe_action_remains" in verdict or "runnable safe action remains" in verdict:
            errors.append(f"safe-work exhaustion review leaves runnable safe action: {row[0]}")
        if "exhausted" not in verdict and "none" not in verdict and "not safe" not in verdict:
            errors.append(f"safe-work exhaustion row verdict must be exhausted, none, or not safe: {row[0]}")
        if followup in {"", "todo", "tbd"}:
            errors.append(f"safe-work exhaustion row needs follow-up/owner or none: {row[0]}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Markdown final acceptance report path")
    parser.add_argument("--agent-behavior", action="store_true", help="Require Agent Advocate / human-counterfactual acceptance evidence")
    parser.add_argument("--allow-template", action="store_true", help="Validate template structure without filled-in evidence")
    parser.add_argument("--cases-dir", type=Path, default=None, help="Warn if failure_case_id does not exist under this cases directory")
    args = parser.parse_args()

    text = args.path.read_text()
    lower = normalize(text)
    found = sections(text)
    errors: list[str] = []
    warnings: list[str] = []
    missing_required_sections: list[str] = []

    for section in REQUIRED_SECTIONS:
        if section not in found:
            missing_required_sections.append(f"missing required section: {section}")

    if args.allow_template:
        if missing_required_sections:
            print("FAIL: acceptance template structure validation failed", file=sys.stderr)
            for error in missing_required_sections:
                print(f"- {error}", file=sys.stderr)
            return 1
        print("PASS: acceptance template structure checks passed")
        return 0

    status = acceptance_status(text, errors)
    referenced_failure = validate_failure_intake(text, status, errors)
    warn_missing_failure_case(referenced_failure, args.cases_dir, warnings)
    validate_defect_fix_receipt(text, errors)
    validate_interface_shape_receipt(text, errors)
    if status in {"rejected", "blocked_with_failure_intake"}:
        validate_terminal_failure_report(found, text, status, errors)
        if errors:
            print("FAIL: acceptance report validation failed", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            for warning in warnings:
                print(f"warning: {warning}", file=sys.stderr)
            return 1
        print("PASS: acceptance report terminal-status checks passed")
        for warning in warnings:
            print(f"warning: {warning}")
        return 0

    errors.extend(missing_required_sections)

    for section in REQUIRED_SECTIONS:
        if section in found and not meaningful_lines(found[section]):
            errors.append(f"required section lacks completed substance: {section}")

    rows = parse_rubric_rows(found.get("rubric scores", ""))
    if not rows:
        errors.append("rubric scores table has no completed rows")
    if find_rubric_row(rows, "Spec fidelity vs repo standards") is None:
        errors.append("rubric scores must include Spec fidelity vs repo standards row")
    if find_rubric_row(rows, "Claim-language / operational outcome") is None:
        errors.append("rubric scores must include Claim-language / operational outcome row")
    runtime_topology_required = args.agent_behavior or any(term in lower for term in RUNTIME_TOPOLOGY_TERMS)
    if runtime_topology_required and find_rubric_row(rows, "Runtime agent topology") is None:
        errors.append("rubric scores must include Runtime agent topology row for campaign/subagent work")
    expensive_proof_required = has_expensive_proof_acceptance_scope(text)
    if expensive_proof_required and find_rubric_row(rows, "Tier 3 expensive-proof") is None:
        errors.append("rubric scores must include Tier 3 expensive-proof row for expensive proof work")
    production_implementation_required = has_production_implementation_acceptance_scope(text)
    if production_implementation_required and find_rubric_row(rows, "Production implementation blocker gate") is None:
        errors.append("rubric scores must include Production implementation blocker gate row for production/runtime implementation work")
    if production_implementation_required and find_rubric_row(rows, "Safe-work exhaustion adversarial review") is None:
        errors.append("rubric scores must include Safe-work exhaustion adversarial review row for production/runtime implementation work")
    code_files_changed = has_new_moved_or_topology_scope(text)
    topology_row = find_rubric_row(rows, "Repository topology")
    if topology_row is None:
        errors.append("rubric scores must include Repository topology row")
    for row in rows:
        score = score_value(row["score"])
        if score is None:
            errors.append(f"rubric row has missing/non-numeric score: {row['dimension']}")
            continue
        if score in {0, 1}:
            errors.append(f"rubric row has blocking/weak score {score}: {row['dimension']}")
        if not row["evidence"] or row["evidence"].lower() in {"", "tbd", "todo"}:
            errors.append(f"rubric row lacks evidence: {row['dimension']}")
        if score == 2:
            gap = row["gap"].strip().lower()
            evidence = row["evidence"].strip().lower()
            if gap in {"", "none", "n/a"} and "not applicable" not in evidence:
                errors.append(f"score 2 row needs named residual gap or explicit not-applicable evidence: {row['dimension']}")
    if topology_row is not None:
        topology_score = score_value(topology_row["score"])
        topology_evidence = topology_row["evidence"].strip().lower()
        topology_gap = topology_row["gap"].strip().lower()
        if code_files_changed:
            if evidence_is_not_applicable(topology_evidence + " " + topology_gap):
                errors.append("Repository topology cannot be not applicable when the report indicates new/moved code, root-level modules, refactors, or package/dependency seams")
            if not any(term in topology_evidence for term in ["topology", "dependency", "gate", "test", "lint", "validator", "validate", "command"]):
                errors.append("Repository topology row must name topology/dependency gate evidence for changed code files")
            if topology_score == 2 and not topology_gap:
                errors.append("Repository topology score 2 needs an explicitly accepted residual gap")

    command_lines = [line for line in found.get("commands and artifacts", "").splitlines() if line.strip().startswith("|")]
    meaningful_command_rows = []
    for line in command_lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and cells[0].lower() not in {"layer", "---"} and not all(not cell for cell in cells):
            if len(cells) >= 3 and all(cells[:3]):
                meaningful_command_rows.append(cells)
    if not meaningful_command_rows:
        errors.append("commands and artifacts table needs at least one completed row")
    if code_files_changed:
        command_blob = normalize(found.get("commands and artifacts", ""))
        if not any(term in command_blob for term in ["topology", "dependency", "lint", "validator", "validate", "package", "gate"]):
            errors.append("commands and artifacts must include topology/dependency gate evidence when the report indicates new/moved code, refactors, or package/dependency seams")

    validate_spec_fidelity_and_standards_review(found, errors)
    validate_claim_state_ledger(found, text, errors)
    validate_user_expectation_delta(found, errors)
    validate_runtime_topology_acceptance(found, text, runtime_topology_required, errors)
    validate_expensive_proof_acceptance(found, expensive_proof_required, errors)
    validate_production_implementation_blocker_gate(found, production_implementation_required, errors)
    validate_safe_work_exhaustion_review(found, production_implementation_required, errors)

    verdict = require_field(text, "100% confident within scope?", errors)
    if verdict and not verdict.lower().startswith("yes"):
        errors.append(f"final confidence verdict is not yes: {verdict}")
    blockers_clear(text, errors)
    recommendation = require_field(text, "Goal completion recommendation", errors)
    if recommendation and not any(term in recommendation.lower() for term in ["complete", "ready", "accept"]):
        errors.append(f"goal completion recommendation is not complete/ready/accept: {recommendation}")

    if args.agent_behavior:
        agent_section = normalize(found.get("agent advocate final check", ""))
        for phrase in ["human counterfactual", "human-parity", "failed invariant"]:
            if phrase not in agent_section and phrase not in lower:
                errors.append(f"agent behavior acceptance missing: {phrase}")
        if "symptom" not in agent_section:
            errors.append("agent behavior acceptance must state why this is not a symptom patch")
        validate_agent_boundary_acceptance(found, errors)
    if args.agent_behavior or has_semantic_pattern_scope(lower):
        validate_regex_keyword_semantic_acceptance(found, errors)

    evidence_hits = [term for term in EVIDENCE_TERMS if term in lower]
    if len(evidence_hits) < 4:
        warnings.append("few evidence layers mentioned; confirm this was a low-risk tier or add explicit non-applicability notes")

    if errors:
        print("FAIL: acceptance report validation failed", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        for warning in warnings:
            print(f"warning: {warning}", file=sys.stderr)
        return 1

    print("PASS: acceptance report sanity checks passed")
    for warning in warnings:
        print(f"warning: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
