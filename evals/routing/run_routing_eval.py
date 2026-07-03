#!/usr/bin/env python3
"""Generate and grade R13 fresh-agent routing eval packets.

This harness is runner-agnostic and never spawns agents itself.

Fresh-agent packet examples:
- Claude Code Agent tool: give one emitted packet to a fresh agent and require the answer fields exactly as requested.
- codex exec: `python3 evals/routing/run_routing_eval.py --case-id R01` and paste the emitted packet into `codex exec`.

Grade examples:
- `python3 evals/routing/run_routing_eval.py --grade evals/routing/fixtures/sample_answers_pass.md`
- `python3 evals/routing/run_routing_eval.py --grade evals/routing/fixtures/sample_answers_under_tier_fail.md`
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_KEY = ROOT / "evals" / "routing" / "answer-key.md"


@dataclass(frozen=True)
class RoutingCase:
    case_id: str
    prompt: str
    expected_tier: str
    expected_artifact: str
    expected_gates: str
    artifact_keyword_sets: list[list[str]]
    routing_keyword_sets: list[list[str]]
    gate_keyword_sets: list[list[str]]
    grade_gates: bool
    must_escalate: bool


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def clean_keyword(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("`", "").replace("$", "")).strip()


def parse_keyword_sets(value: str) -> list[list[str]]:
    sets: list[list[str]] = []
    for option in value.split(";"):
        keywords = [clean_keyword(part) for part in option.split("+") if clean_keyword(part)]
        if keywords:
            sets.append(keywords)
    return sets


def normalize(value: str) -> str:
    value = value.replace("`", "").replace("$", "")
    value = value.replace("_", " ")
    return re.sub(r"\s+", " ", value.lower()).strip()


def contains_keyword(text: str, keyword: str) -> bool:
    return normalize(keyword) in normalize(text)


def matches_any_keyword_set(text: str, keyword_sets: list[list[str]]) -> bool:
    if not keyword_sets:
        return True
    return any(all(contains_keyword(text, keyword) for keyword in keyword_set) for keyword_set in keyword_sets)


def parse_answer_key(path: Path = DEFAULT_KEY) -> list[RoutingCase]:
    lines = path.read_text(encoding="utf-8").splitlines()
    table_lines = [line for line in lines if line.startswith("|") and not re.fullmatch(r"\|(?:[-: ]+\|)+", line)]
    if not table_lines:
        raise ValueError(f"no markdown table found in {path}")
    header = [normalize(cell) for cell in split_row(table_lines[0])]
    rows = [split_row(line) for line in table_lines[1:]]
    required = [
        "prompt",
        "expected tier",
        "expected artifact",
        "expected gate(s)",
        "artifact keyword sets",
        "routing keyword sets",
        "gate keyword sets",
        "grade gates",
    ]
    missing = [name for name in required if name not in header]
    if missing:
        raise ValueError(f"answer key missing column(s): {', '.join(missing)}")
    index = {name: header.index(name) for name in required}
    cases: list[RoutingCase] = []
    for row_number, row in enumerate(rows, start=1):
        if len(row) < len(header):
            row.extend([""] * (len(header) - len(row)))
        prompt = row[index["prompt"]]
        case_id = f"R{row_number:02d}"
        cases.append(
            RoutingCase(
                case_id=case_id,
                prompt=prompt,
                expected_tier=row[index["expected tier"]],
                expected_artifact=row[index["expected artifact"]],
                expected_gates=row[index["expected gate(s)"]],
                artifact_keyword_sets=parse_keyword_sets(row[index["artifact keyword sets"]]),
                routing_keyword_sets=parse_keyword_sets(row[index["routing keyword sets"]]),
                gate_keyword_sets=parse_keyword_sets(row[index["gate keyword sets"]]),
                grade_gates=normalize(row[index["grade gates"]]) == "yes",
                must_escalate="EXPECT-ESCALATION" in prompt,
            )
        )
    return cases


def render_packet(case: RoutingCase) -> str:
    marker = " MUST-ESCALATE" if case.must_escalate else ""
    return f"""## {case.case_id}{marker}

Fresh-agent routing eval packet.

Contract:
- Read ONLY `ubergoal/SKILL.md` from this pack.
- Do not read `evals/routing/answer-key.md`, other skills, coordination docs, or prior transcripts.
- Do not implement the requested work.
- Return exactly these fields:
  - case_id: {case.case_id}
  - tier:
  - artifact:
  - routing:
  - gates:
  - one_line_justification:

Probe prompt:
{case.prompt}
"""


def parse_json_answers(path: Path) -> dict[str, dict[str, str]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        records = payload
    elif isinstance(payload, dict) and "answers" in payload:
        records = payload["answers"]
    elif isinstance(payload, dict):
        records = [{"case_id": key, **value} for key, value in payload.items()]
    else:
        raise ValueError("answers JSON must be a list, a case-id map, or an object with answers")
    answers: dict[str, dict[str, str]] = {}
    for record in records:
        if not isinstance(record, dict) or "case_id" not in record:
            raise ValueError("each answer record must contain case_id")
        case_id = str(record["case_id"]).strip()
        answers[case_id] = {normalize(str(key)): str(value) for key, value in record.items()}
    return answers


def parse_markdown_answers(path: Path) -> dict[str, dict[str, str]]:
    answers: dict[str, dict[str, str]] = {}
    current: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        heading = re.match(r"^##\s+(R\d{2})\b", line.strip())
        if heading:
            current = heading.group(1)
            answers[current] = {"case id": current}
            continue
        if current and ":" in line:
            key, value = line.split(":", 1)
            key = normalize(key.strip("- "))
            if key in {"case id", "case_id", "tier", "artifact", "routing", "gates", "one line justification"}:
                answers[current][key.replace("_", " ")] = value.strip()
    return answers


def parse_answers(path: Path) -> dict[str, dict[str, str]]:
    if path.suffix == ".json":
        return parse_json_answers(path)
    return parse_markdown_answers(path)


def answer_field(answer: dict[str, str], field: str) -> str:
    return answer.get(field, "")


def grade_case(case: RoutingCase, answer: dict[str, str] | None) -> tuple[bool, list[str]]:
    if answer is None:
        return False, ["missing answer"]
    failures: list[str] = []
    actual_tier = answer_field(answer, "tier")
    if normalize(actual_tier) != normalize(case.expected_tier):
        failures.append(f"tier expected={case.expected_tier!r} actual={actual_tier!r}")
    if not matches_any_keyword_set(answer_field(answer, "artifact"), case.artifact_keyword_sets):
        failures.append(f"artifact missing keyword set actual={answer_field(answer, 'artifact')!r}")
    if not matches_any_keyword_set(answer_field(answer, "routing"), case.routing_keyword_sets):
        failures.append(f"routing missing keyword set actual={answer_field(answer, 'routing')!r}")
    if case.grade_gates and not matches_any_keyword_set(answer_field(answer, "gates"), case.gate_keyword_sets):
        failures.append(f"gates missing keyword set actual={answer_field(answer, 'gates')!r}")
    if case.must_escalate and failures:
        failures.insert(0, "MUST_ESCALATE case failed")
    return not failures, failures


def grade_answers(cases: list[RoutingCase], answers: dict[str, dict[str, str]]) -> tuple[int, str]:
    lines: list[str] = []
    failed = 0
    for case in cases:
        passed, failures = grade_case(case, answers.get(case.case_id))
        if passed:
            gate_status = "gates=graded" if case.grade_gates else "gates=skipped"
            marker = " MUST_ESCALATE" if case.must_escalate else ""
            lines.append(f"PASS {case.case_id}{marker} {gate_status}")
            continue
        failed += 1
        marker = " MUST_ESCALATE" if case.must_escalate else ""
        lines.append(f"FAIL {case.case_id}{marker}: {'; '.join(failures)}")
    passed_count = len(cases) - failed
    lines.append(f"SUMMARY passed={passed_count} failed={failed} total={len(cases)}")
    return (1 if failed else 0), "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--answer-key", type=Path, default=DEFAULT_KEY)
    parser.add_argument("--case-id", help="emit only one case packet, e.g. R01")
    parser.add_argument("--grade", type=Path, help="grade a markdown or JSON answers file")
    args = parser.parse_args()

    cases = parse_answer_key(args.answer_key)
    if args.grade:
        code, output = grade_answers(cases, parse_answers(args.grade))
        sys.stdout.write(output)
        return code
    selected = [case for case in cases if args.case_id is None or case.case_id == args.case_id]
    if args.case_id and not selected:
        print(f"ERROR: unknown case id {args.case_id}", file=sys.stderr)
        return 2
    sys.stdout.write("\n".join(render_packet(case) for case in selected).rstrip() + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
