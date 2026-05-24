#!/usr/bin/env python3
"""Validate a completed lightweight Uber run receipt.

This is a shape/evidence-presence validator, not a semantic judge. It keeps
`uberskillevolver` from promoting lessons based only on vague prose by requiring
skill-use, artifact, gate, replay, verdict, and learning-handoff receipts.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "run metadata",
    "skills invoked",
    "artifacts",
    "operational outcome / terminal-state summary",
    "gates",
    "fresh-agent replay",
    "behavior verdict",
    "uberskillevolver handoff",
]
REQUIRED_SKILLS = [
    "ubergoal",
    "uberassess",
    "uberplan",
    "uberaccept",
    "ubersimplify",
    "uberskillevolver",
    "ubershow",
    "uberrca",
    "uber-skill-creator",
]
REQUIRED_GATES = [
    "goal created/bound or explicitly skipped",
    "uberplan or work-contract planning",
    "user expectation / surprise assessment",
    "plan acceptance / thin-harness check",
    "rca-driven testing adaptation",
    "operational outcome / child terminal states",
    "uberaccept final proof",
    "policy-adherence / openclaw architecture check",
    "skills invoked summary",
    "uberskillevolver learning decision",
]
SECTION_ALIASES = {
    "skills invoked": {"skills invoked", "skills used"},
}
SKILL_ALIASES = {
    "uber-skill-creator": {"uber-skill-creator", "skill-creator"},
}
GATE_ALIASES = {
    "rca-driven testing adaptation": {"rca-driven testing adaptation", "repeated-test-failure adaptation"},
    "skills invoked summary": {"skills invoked summary", "skills used summary"},
}
PLACEHOLDERS = {"", " ", "todo", "tbd", "yes/no", "yes/no/n/a", "pass/fail/n/a"}
TERMINAL_STATES = {"operational", "blocked", "re_scoped_with_approval"}
TOPOLOGY_TRIGGER_TERMS = [
    "ubercampaign",
    "campaign-profile",
    "plan-tree campaign",
    "multi-feature",
    "max_depth",
    "max_threads",
    "depth-3",
    "l0",
    "l1",
    "l2",
    "subagent",
]
TOPOLOGY_MODES = {"standard_6_2", "deep_8_3", "wide_10_3", "custom", "n/a", "na", "not applicable"}
PRODUCTION_IMPLEMENTATION_TERMS = [
    "production implementation",
    "production/runtime",
    "runtime implementation",
    "unattended production",
    "long-running production",
    "external or irreversible",
    "irreversible stop",
    "external stop",
    "safe predecessor",
    "runnable safe next action",
    "active_blocked",
    "hard_blocked_after_safe_action_exhaustion",
]


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def sections(markdown: str) -> dict[str, str]:
    out: dict[str, list[str]] = {}
    current: str | None = None
    for line in markdown.splitlines():
        match = re.match(r"^##\s+(.+?)\s*$", line)
        if match:
            current = normalize(match.group(1))
            out.setdefault(current, [])
        elif current:
            out[current].append(line)
    return {key: "\n".join(value).strip() for key, value in out.items()}


def section_aliases(section: str) -> set[str]:
    return SECTION_ALIASES.get(section, {section})


def find_section(found: dict[str, str], section: str) -> str:
    for alias in section_aliases(section):
        if alias in found:
            return found[alias]
    return ""


def value_aliases(value: str, aliases: dict[str, set[str]]) -> set[str]:
    return aliases.get(value, {value})


def table_rows(section: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in section.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells or all(not cell or set(cell) <= {"-", ":"} for cell in cells):
            continue
        first = cells[0].strip().lower()
        if first in {"skill", "artifact", "gate", "plan or child id"}:
            continue
        rows.append(cells)
    return rows


def require_field(section: str, label: str, errors: list[str]) -> str:
    separator = r"[ \t]*(?::)?[ \t]*" if label.endswith("?") else r"[ \t]*:[ \t]*"
    pattern = re.compile(rf"^[ \t]*-[ \t]*{re.escape(label)}{separator}(.+?)[ \t]*$", re.I | re.M)
    match = pattern.search(section)
    if not match:
        errors.append(f"missing field: {label}")
        return ""
    value = match.group(1).strip()
    if normalize(value) in PLACEHOLDERS:
        errors.append(f"placeholder field: {label}")
    return value


def parse_nonnegative_int(raw: str, label: str, errors: list[str]) -> int | None:
    match = re.search(r"\b([0-9]+)\b", raw or "")
    if not match:
        errors.append(f"{label} must contain a nonnegative integer")
        return None
    return int(match.group(1))


def has_production_implementation_scope(full_text: str) -> bool:
    text = normalize(full_text)
    return any(term in text for term in PRODUCTION_IMPLEMENTATION_TERMS)


def validate_production_blocker_gate(found: dict[str, str], required: bool, errors: list[str]) -> bool:
    section = found.get("production implementation blocker gate", "")
    if not required:
        return True
    if not section:
        errors.append("production/runtime implementation receipt requires Production implementation blocker gate section")
        return False
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
    if not normalize(values["Production implementation goal?"]).startswith("yes"):
        return True
    active = parse_nonnegative_int(values["Active blocked child count"], "Active blocked child count", errors)
    runnable = parse_nonnegative_int(values["Runnable safe next action count"], "Runnable safe next action count", errors)
    required_count = parse_nonnegative_int(values["Required child count"], "Required child count", errors)
    operational = parse_nonnegative_int(
        values["Operational or user-rescoped child count"],
        "Operational or user-rescoped child count",
        errors,
    )
    hard = parse_nonnegative_int(
        values["Hard-blocked-after-safe-action-exhaustion child count"],
        "Hard-blocked-after-safe-action-exhaustion child count",
        errors,
    )
    ok = True
    if active not in {None, 0}:
        errors.append("receipt cannot mark success with active blocked production children")
        ok = False
    if runnable not in {None, 0}:
        errors.append("receipt cannot mark success while runnable safe next actions remain")
        ok = False
    if not normalize(values["Parent completion allowed?"]).startswith("yes"):
        errors.append("Production implementation blocker gate must say parent completion allowed? yes before success")
        ok = False
    if hard and hard > 0 and not normalize(values["Safe autonomous predecessor work exhausted?"]).startswith("yes"):
        errors.append("hard-blocked production children require safe autonomous predecessor work exhausted? yes")
        ok = False
    if None not in {required_count, operational, hard} and (operational or 0) + (hard or 0) < (required_count or 0):
        errors.append("production blocker counts do not cover required child count")
        ok = False

    rows = table_rows(section)
    data_rows = [row for row in rows if row and normalize(row[0]) not in {"child id", "child"}]
    if not data_rows:
        errors.append("Production implementation blocker gate needs child rows")
        return False
    for row in data_rows:
        if len(row) < 7:
            errors.append(f"production blocker row has too few cells: {' | '.join(row)}")
            ok = False
            continue
        child = row[0]
        classification = normalize(row[2])
        runnable_cell = normalize(row[3])
        exhaustion = normalize(row[4])
        blocker = normalize(row[5])
        if "active_blocked" in classification or "active blocked" in classification:
            errors.append(f"production child remains active-blocked: {child}")
            ok = False
        if runnable_cell.startswith("yes"):
            errors.append(f"production child has runnable safe next actions: {child}")
            ok = False
        if "hard_blocked_after_safe_action_exhaustion" in classification or "hard-blocked-after" in classification:
            if "exhaust" not in exhaustion:
                errors.append(f"hard-blocked child lacks safe-predecessor exhaustion evidence: {child}")
                ok = False
            if not any(term in blocker for term in ["external", "approval", "unsafe", "irreversible", "credential", "owner"]):
                errors.append(f"hard-blocked child lacks exact external/unsafe blocker: {child}")
                ok = False
    return ok


def validate_operational_summary(found: dict[str, str], metadata: str, production_gate_ok: bool, errors: list[str]) -> None:
    section = found["operational outcome / terminal-state summary"]
    rows = table_rows(section)
    if not rows:
        errors.append("operational outcome / terminal-state summary needs at least one plan/child row")
    blocked_rows: list[str] = []
    for row in rows:
        if len(row) < 5:
            errors.append(f"operational outcome row has too few cells: {' | '.join(row)}")
            continue
        terminal = normalize(row[2])
        evidence = normalize(row[3])
        gap = normalize(row[4])
        state = next((candidate for candidate in TERMINAL_STATES if candidate in terminal), None)
        if state is None:
            errors.append(f"operational outcome row has invalid terminal state: {row[0]}={row[2]}")
            continue
        if evidence in PLACEHOLDERS or evidence in {"none", "n/a"}:
            errors.append(f"operational outcome row lacks evidence: {row[0]}")
        if state == "blocked":
            blocked_rows.append(row[0])
            if gap in PLACEHOLDERS or gap in {"none", "n/a", "no gap"}:
                errors.append(f"blocked operational outcome row lacks blocker/gap: {row[0]}")
    proof_claim = require_field(section, "Proof-only, shadow-only, local-safe-proof, or shared-spine evidence claimed as operational?", errors)
    if proof_claim and normalize(proof_claim).startswith("yes"):
        errors.append("proof-only/shadow-only/local-safe-proof/shared-spine evidence cannot be claimed as operational")
    outcome = require_field(metadata, "Outcome", errors)
    if blocked_rows and normalize(outcome) == "success" and not production_gate_ok:
        errors.append(f"receipt outcome success cannot include blocked child rows: {', '.join(blocked_rows)}")


def validate_runtime_topology(found: dict[str, str], full_text: str, errors: list[str]) -> None:
    lower = normalize(full_text)
    required = any(term in lower for term in TOPOLOGY_TRIGGER_TERMS)
    section = found.get("runtime agent topology", "")
    if not section:
        if required:
            errors.append("campaign/subagent receipts require Runtime agent topology section")
        return
    for label in [
        "Config source / observed source",
        "Topology mode",
        "Current `max_threads`",
        "Current `max_depth`",
        "Role shape",
        "Depth-3 escalation needed?",
        "User approval evidence for depth/thread escalation",
        "Restore target after campaign",
        "Restore proof / blocker",
        "Child-agent depth policy",
    ]:
        require_field(section, label, errors)
    mode = normalize(require_field(section, "Topology mode", errors))
    if mode and mode not in TOPOLOGY_MODES:
        errors.append(f"invalid topology mode: {mode}")
    depth = normalize(require_field(section, "Current `max_depth`", errors))
    threads = normalize(require_field(section, "Current `max_threads`", errors))
    approval = normalize(require_field(section, "User approval evidence for depth/thread escalation", errors))
    restore = normalize(require_field(section, "Restore target after campaign", errors))
    restore_proof = normalize(require_field(section, "Restore proof / blocker", errors))
    depth3_needed = normalize(require_field(section, "Depth-3 escalation needed?", errors))
    if mode == "standard_6_2":
        if threads != "6" or depth != "2":
            errors.append("standard_6_2 topology must record Current max_threads=6 and Current max_depth=2")
    if mode in {"deep_8_3", "wide_10_3"} or depth == "3" or depth3_needed.startswith("yes"):
        if "approval" not in approval and "approved" not in approval:
            errors.append("depth-3/thread escalation requires recorded user approval evidence")
        if "6/2" not in restore and "max_threads=6" not in restore:
            errors.append("depth-3/thread escalation requires restore target to default 6/2")
        if restore_proof in PLACEHOLDERS or restore_proof in {"none", "n/a"}:
            errors.append("depth-3/thread escalation requires restore proof or exact blocker")


def validate(path: Path, allow_template: bool = False) -> list[str]:
    text = path.read_text()
    found = sections(text)
    errors: list[str] = []
    for section in REQUIRED_SECTIONS:
        if not find_section(found, section):
            errors.append(f"missing required section: {section}")
    if allow_template:
        return errors
    if errors:
        return errors

    metadata = found["run metadata"]
    for label in ["Run slug", "Date/time", "Project/repo", "Tier", "Owner/session", "Outcome"]:
        require_field(metadata, label, errors)

    production_gate_ok = validate_production_blocker_gate(found, has_production_implementation_scope(text), errors)
    validate_operational_summary(found, metadata, production_gate_ok, errors)
    validate_runtime_topology(found, text, errors)

    skill_rows = table_rows(find_section(found, "skills invoked"))
    skill_names = {normalize(row[0]) for row in skill_rows if row}
    for skill in REQUIRED_SKILLS:
        if skill_names.isdisjoint(value_aliases(skill, SKILL_ALIASES)):
            errors.append(f"skills invoked table missing skill: {skill}")
    for row in skill_rows:
        if len(row) < 5:
            errors.append(f"skills invoked row has too few cells: {' | '.join(row)}")
            continue
        used = normalize(row[1])
        evidence = normalize(row[2])
        reason = normalize(row[3])
        if used not in {"yes", "no", "n/a", "na", "not applicable"}:
            errors.append(f"skill {row[0]} has invalid Invoked? value: {row[1]}")
        if evidence in PLACEHOLDERS:
            errors.append(f"skill {row[0]} missing evidence/artifact entry")
        if reason in PLACEHOLDERS:
            errors.append(f"skill {row[0]} missing reason used/skipped")

    artifact_rows = table_rows(found["artifacts"])
    if len(artifact_rows) < 3:
        errors.append("artifacts table needs at least three meaningful rows")
    for row in artifact_rows:
        if len(row) >= 4 and normalize(row[2]).startswith("yes") and not normalize(row[3]).startswith("yes"):
            errors.append(f"required artifact not present: {row[0]}")

    gate_rows = table_rows(found["gates"])
    gate_names = {normalize(row[0]) for row in gate_rows if row}
    for gate in REQUIRED_GATES:
        if gate_names.isdisjoint(value_aliases(gate, GATE_ALIASES)):
            errors.append(f"gates table missing gate: {gate}")
    for row in gate_rows:
        if len(row) >= 4:
            expected = normalize(row[1])
            result = normalize(row[3])
            if expected.startswith("yes") and result != "pass":
                errors.append(f"expected gate did not pass: {row[0]}={row[3]}")

    replay = found["fresh-agent replay"]
    for label in ["Replay mode", "Replay prompt / fixture", "Result", "Missing affordances", "Follow-up"]:
        require_field(replay, label, errors)

    verdict = found["behavior verdict"]
    for label in [
        "Did the run use the intended Uber skills?",
        "Did the skills change behavior versus generic planning?",
        "Did the run avoid fat-harness / deterministic-monolith drift?",
        "Did the run produce enough evidence for `uberskillevolver`?",
        "Verdict rationale",
    ]:
        require_field(verdict, label, errors)
    enough = require_field(verdict, "Did the run produce enough evidence for `uberskillevolver`?", errors)
    if enough and not normalize(enough).startswith("yes"):
        errors.append("receipt says it does not produce enough evidence for uberskillevolver")

    handoff = found["uberskillevolver handoff"]
    for label in ["Learning record path", "Candidate lessons", "Promote now", "Defer", "No-change rationale", "Safe to commit?"]:
        require_field(handoff, label, errors)
    safe = require_field(handoff, "Safe to commit?", errors)
    if safe and not normalize(safe).startswith("yes"):
        errors.append("uberskillevolver handoff is not safe to commit")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--allow-template", action="store_true")
    args = parser.parse_args()
    errors = validate(args.path, args.allow_template)
    if errors:
        print("FAIL: Uber run receipt validation failed", file=sys.stderr)
        for error in sorted(set(errors)):
            print(f"- {error}", file=sys.stderr)
        return 1
    print("PASS: Uber run receipt checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
