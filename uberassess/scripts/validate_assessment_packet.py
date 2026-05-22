#!/usr/bin/env python3
"""Validate an uberassess assessment packet."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "Source packet",
    "Research frame and source map",
    "Key ideas and claims",
    "Alternatives and adoption options",
    "Project relevance matrix",
    "Source authority and uncertainty",
    "Benefit vs complexity cost",
    "Recommendation",
    "Handoff",
    "Outcome learning trail",
]
REQUIRED_FIELDS = [
    "Assessment tier:",
    "Assessment mode:",
    "Decision:",
    "Suggested next step:",
    "Implementation before approval:",
    "Confidence:",
    "Confidence scope:",
    "Known gaps:",
    "Research question:",
    "Source kind:",
    "Source URL:",
    "Source title:",
    "Source author:",
    "Source date:",
    "Retrieval date:",
    "Raw source captured:",
    "Linked sources inspected:",
    "Linked sources not inspected:",
    "Media/transcript/OCR inspected:",
    "Retrieval limitations:",
    "Source authority role:",
    "Local codebase/docs inspected:",
    "External primary docs inspected:",
    "Alternatives/prior art inspected:",
    "Forums/issues/practitioner discussion inspected:",
    "Contradiction search performed:",
    "Coverage claimed:",
    "Coverage not claimed:",
    "Project context checked:",
    "Evidence quality:",
    "Missing evidence:",
    "Possible hype or sales bias:",
    "Benefit >> cost?:",
    "Potential benefit:",
    "Implementation cost:",
    "Maintenance cost:",
    "Complexity added:",
    "Delete or simplify instead?:",
    "Complexity posture:",
    "Approval required before:",
    "Recommended destination:",
    "Do not do:",
    "Evidence layers completed:",
    "Evidence layers deferred:",
]
VALID_DECISIONS = {
    "adopt now",
    "watch",
    "archive",
    "reject",
    "needs more research",
    "convert to eval only",
}
VALID_SOURCE_KINDS = {
    "x_post",
    "x_thread",
    "article",
    "github_repo",
    "arxiv_paper",
    "pdf",
    "video",
    "internal_artifact",
    "idea_seed",
    "implementation_question",
    "open_research_question",
    "mixed",
    "unknown",
}
IMPLEMENTATION_FORBIDDEN_PATTERNS = [
    r"implementation before approval:\s*(yes|allowed|approved)\b",
    r"approval required before:\s*none\b.*\b(code|skill|automation|mcp|server|workflow|config)",
]
PLACEHOLDER_VALUES = {
    "",
    "-",
    "destination",
    "<destination>",
    "<project>",
    "<project a>",
    "project a",
    "project b",
    "none/low/med/high",
    "<high/med/low/none>",
}


def read(path: Path) -> str:
    try:
        return path.read_text()
    except Exception as exc:  # pragma: no cover - argparse path guard covers most cases
        raise SystemExit(f"could not read {path}: {exc}") from exc


def field_value(text: str, field: str) -> str:
    match = re.search(rf"^{re.escape(field)}\s*(.+)$", text, flags=re.I | re.M)
    return match.group(1).strip() if match else ""


def has_section(text: str, section: str) -> bool:
    return bool(re.search(rf"^##\s+{re.escape(section)}\s*$", text, flags=re.I | re.M))


def project_matrix_rows(text: str) -> list[list[str]]:
    match = re.search(r"^##\s+Project relevance matrix\s*$", text, flags=re.I | re.M)
    if not match:
        return []
    start = match.end()
    next_section = re.search(r"^##\s+", text[start:], flags=re.M)
    body = text[start : start + next_section.start()] if next_section else text[start:]
    rows: list[list[str]] = []
    for line in body.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 6:
            continue
        first = cells[0].strip().lower()
        if first in {"destination", "---"} or set(first) <= {"-", ":"}:
            continue
        if first in PLACEHOLDER_VALUES or any(cell.strip().lower() in PLACEHOLDER_VALUES for cell in cells[:2]):
            continue
        rows.append(cells)
    return rows


def section_table_rows(text: str, section: str) -> list[list[str]]:
    match = re.search(rf"^##\s+{re.escape(section)}\s*$", text, flags=re.I | re.M)
    if not match:
        return []
    start = match.end()
    next_section = re.search(r"^##\s+", text[start:], flags=re.M)
    body = text[start : start + next_section.start()] if next_section else text[start:]
    rows: list[list[str]] = []
    for line in body.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        first = cells[0].strip().lower()
        if first in {"lane", "option", "---"} or set(first) <= {"-", ":"}:
            continue
        if first in PLACEHOLDER_VALUES or any(cell.strip().lower() in PLACEHOLDER_VALUES for cell in cells[:2]):
            continue
        rows.append(cells)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("--tier", type=int, choices=[0, 1, 2, 3], default=None)
    parser.add_argument("--agent-system", action="store_true", help="Require Agent Advocate/human-counterfactual fields")
    parser.add_argument("--implementation-likely", action="store_true", help="Require ubergoal handoff, evidence plan, rollback/stop condition")
    parser.add_argument("--allow-template", action="store_true", help="Allow placeholder template values")
    args = parser.parse_args()

    text = read(args.packet)
    lower = text.lower()
    errors: list[str] = []

    if "<" in text and ">" in text and not args.allow_template:
        errors.append("packet appears to contain template placeholders; pass --allow-template only for templates")

    for section in REQUIRED_SECTIONS:
        if not has_section(text, section):
            errors.append(f"missing section: {section}")
    for field in REQUIRED_FIELDS:
        if not re.search(rf"^{re.escape(field)}", text, flags=re.I | re.M):
            errors.append(f"missing field: {field}")

    decision = field_value(text, "Decision:").split("/")[0].strip().lower()
    if decision and decision not in VALID_DECISIONS and not args.allow_template:
        errors.append(f"Decision must be one of {sorted(VALID_DECISIONS)}; found {decision!r}")

    kind = field_value(text, "Source kind:").split("/")[0].strip().lower()
    if kind and kind not in VALID_SOURCE_KINDS and not args.allow_template:
        errors.append(f"Source kind must be one of {sorted(VALID_SOURCE_KINDS)}; found {kind!r}")

    if not args.allow_template and not project_matrix_rows(text):
        errors.append("project relevance matrix needs at least one completed destination row; project names are adapter-specific, not hardcoded by the portable validator")
    if not args.allow_template and not section_table_rows(text, "Research frame and source map"):
        errors.append("research frame/source map needs at least one completed source-map row")
    if not args.allow_template and not section_table_rows(text, "Alternatives and adoption options"):
        errors.append("alternatives/adoption options needs at least one completed option row")

    impl = field_value(text, "Implementation before approval:").lower()
    if impl and impl != "no" and not args.allow_template:
        errors.append("Implementation before approval must be exactly: no")
    for pattern in IMPLEMENTATION_FORBIDDEN_PATTERNS:
        if re.search(pattern, lower, flags=re.S):
            errors.append(f"forbidden approval-boundary pattern: {pattern}")

    if args.tier is not None:
        tier_value = field_value(text, "Assessment tier:")
        if tier_value and not tier_value.startswith(str(args.tier)) and not args.allow_template:
            errors.append(f"Assessment tier field does not match --tier {args.tier}")
    tier_num = args.tier
    if tier_num is None:
        tv = field_value(text, "Assessment tier:")
        if tv[:1].isdigit():
            tier_num = int(tv[:1])

    if tier_num is not None and tier_num >= 2:
        for phrase in [
            "Project context checked:",
            "Freshness risk:",
            "Simpler alternative:",
            "Evidence layers completed:",
            "Evidence layers deferred:",
            "Coverage claimed:",
            "Coverage not claimed:",
            "Contradiction search performed:",
        ]:
            if not re.search(rf"^{re.escape(phrase)}", text, flags=re.I | re.M):
                errors.append(f"Tier {tier_num} requires field: {phrase}")
        if "benefit >> cost?: unclear" in lower:
            errors.append(f"Tier {tier_num} cannot be complete with Benefit >> cost?: unclear")

    if kind in {"idea_seed", "implementation_question", "open_research_question"}:
        mode = field_value(text, "Assessment mode:").lower()
        if "deep" not in mode and not args.allow_template:
            errors.append(f"{kind} assessments should use Assessment mode: deep research assessment or mixed")

    if args.agent_system or (tier_num is not None and tier_num >= 3):
        if not has_section(text, "Agent Advocate / human counterfactual"):
            errors.append("agent-system assessment requires Agent Advocate / human counterfactual section")
        for phrase in ["Human counterfactual:", "Agent affordance gap:", "Root layer to fix before behavior-policing:"]:
            if not re.search(rf"^{re.escape(phrase)}", text, flags=re.I | re.M):
                errors.append(f"agent-system assessment requires field: {phrase}")

    if args.implementation_likely or (tier_num is not None and tier_num >= 3):
        for phrase in ["Ubergoal handoff:", "Evidence plan:", "Rollback/stop condition:"]:
            value = field_value(text, phrase)
            if not value:
                errors.append(f"implementation-likely assessment requires field: {phrase}")
            elif value.lower() in {"n/a", "na", "none"} and not args.allow_template:
                errors.append(f"implementation-likely assessment cannot leave {phrase} as {value!r}")

    if errors:
        print("FAIL: assessment packet invalid", file=sys.stderr)
        for error in sorted(set(errors)):
            print(f"- {error}", file=sys.stderr)
        return 1
    print("PASS: assessment packet valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
