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
    "rubric scores",
    "commands and artifacts",
    "planning review reconciliation",
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Markdown final acceptance report path")
    parser.add_argument("--agent-behavior", action="store_true", help="Require Agent Advocate / human-counterfactual acceptance evidence")
    parser.add_argument("--allow-template", action="store_true", help="Validate template structure without filled-in evidence")
    args = parser.parse_args()

    text = args.path.read_text()
    lower = normalize(text)
    found = sections(text)
    errors: list[str] = []
    warnings: list[str] = []

    for section in REQUIRED_SECTIONS:
        if section not in found:
            errors.append(f"missing required section: {section}")

    if args.allow_template:
        if errors:
            print("FAIL: acceptance template structure validation failed", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 1
        print("PASS: acceptance template structure checks passed")
        return 0

    for section in REQUIRED_SECTIONS:
        if section in found and not meaningful_lines(found[section]):
            errors.append(f"required section lacks completed substance: {section}")

    rows = parse_rubric_rows(found.get("rubric scores", ""))
    if not rows:
        errors.append("rubric scores table has no completed rows")
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
