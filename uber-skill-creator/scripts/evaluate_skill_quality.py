#!/usr/bin/env python3
"""Evaluate portable SKILL.md package quality without mutating files."""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from html import escape
from pathlib import Path
from typing import Any

MAX_SKILL_LINES = 500
LONG_SKILL_LINES = 400
MIN_DESCRIPTION_CHARS = 80
MAX_DESCRIPTION_CHARS = 1024

TRIGGER_PATTERNS = [
    r"\buse when\b",
    r"\buse for\b",
    r"\buse this\b",
    r"\bwhen (?:the user|codex|agents?|asked|working|creating|updating|evaluating)\b",
    r"\bdo not auto-trigger\b",
    r"\bonly when explicitly\b",
    r"\brouted by\b",
]
VERIFICATION_PATTERNS = [
    r"\bverify\b",
    r"\bvalidate\b",
    r"\btest\b",
    r"\beval\b",
    r"\bproof\b",
    r"\bevidence\b",
    r"\bacceptance\b",
    r"\breceipt\b",
]
SIDE_EFFECT_PATTERNS = [
    r"\bwrite\b",
    r"\bdelete\b",
    r"\bcommit\b",
    r"\bpush\b",
    r"\bpost\b",
    r"\bsend\b",
    r"\bpublish\b",
    r"\bdeploy\b",
    r"\bautomation\b",
    r"\bmcp\b",
    r"\bapi\b",
    r"\bslack\b",
    r"\bemail\b",
]
SIDE_EFFECT_POLICY_PATTERNS = [
    r"\bapproval\b",
    r"\bwithout explicit\b",
    r"\bread-only\b",
    r"\bno implementation\b",
    r"\bdo not\b",
    r"\bnever\b",
    r"\bside effects?\b",
    r"\bpermission\b",
]
ANTI_RATIONALIZATION_PATTERNS = [
    r"\bdo not\b",
    r"\bnever\b",
    r"\bavoid\b",
    r"\bforbidden\b",
    r"\bmust not\b",
    r"\banti-bloat\b",
    r"\bskip\b",
    r"\brationali[sz]",
    r"\bfailure\b",
    r"\bstop\b",
]


@dataclass(frozen=True)
class Issue:
    severity: str
    category: str
    message: str
    suggestion: str

    def as_dict(self) -> dict[str, str]:
        return {
            "severity": self.severity,
            "category": self.category,
            "message": self.message,
            "suggestion": self.suggestion,
        }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = re.match(r"^---\n(.*?)\n---\n?", text, flags=re.S)
    if not match:
        return {}, text
    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        data[key.strip()] = value
    return data, text[match.end() :]


def has_any(patterns: list[str], text: str) -> bool:
    return any(re.search(pattern, text, flags=re.I) for pattern in patterns)


def words(text: str) -> set[str]:
    stop = {
        "a",
        "an",
        "and",
        "as",
        "by",
        "for",
        "from",
        "in",
        "into",
        "is",
        "it",
        "of",
        "on",
        "or",
        "the",
        "to",
        "use",
        "when",
        "with",
    }
    return {token for token in re.findall(r"[a-z0-9]+", text.lower()) if len(token) > 2 and token not in stop}


def immediate_skill_dirs(path: Path) -> list[Path]:
    path = path.resolve()
    if (path / "SKILL.md").exists():
        return [path]
    skills = sorted(child for child in path.iterdir() if child.is_dir() and (child / "SKILL.md").exists())
    if skills:
        return skills
    return sorted({skill.parent for skill in path.rglob("SKILL.md")})


def score_from_issues(issues: list[Issue]) -> int:
    penalties = {"error": 18, "warn": 9, "info": 3}
    return max(0, 100 - sum(penalties.get(issue.severity, 3) for issue in issues))


def evaluate_skill(skill_dir: Path) -> dict[str, Any]:
    skill_md = skill_dir / "SKILL.md"
    text = read_text(skill_md)
    meta, body = frontmatter(text)
    name = meta.get("name", "")
    description = meta.get("description", "")
    lines = text.splitlines()
    body_lower = body.lower()
    issues: list[Issue] = []

    if not name:
        issues.append(Issue("error", "frontmatter", "Missing frontmatter name.", "Add a stable hyphen-case name."))
    elif name != skill_dir.name:
        issues.append(
            Issue(
                "warn",
                "frontmatter",
                f"Frontmatter name {name!r} does not match folder {skill_dir.name!r}.",
                "Align the name and folder unless this is an adapter copy.",
            )
        )

    if not description:
        issues.append(Issue("error", "triggering", "Missing frontmatter description.", "Add trigger-focused description text."))
    else:
        if len(description) < MIN_DESCRIPTION_CHARS:
            issues.append(
                Issue(
                    "warn",
                    "triggering",
                    f"Description is short ({len(description)} chars).",
                    "Include what the skill does and concrete contexts that should trigger it.",
                )
            )
        if len(description) > MAX_DESCRIPTION_CHARS:
            issues.append(
                Issue(
                    "error",
                    "triggering",
                    f"Description exceeds {MAX_DESCRIPTION_CHARS} chars.",
                    "Move non-trigger instructions into SKILL.md or references.",
                )
            )
        if not has_any(TRIGGER_PATTERNS, description):
            issues.append(
                Issue(
                    "warn",
                    "triggering",
                    "Description lacks an explicit trigger phrase.",
                    "Use phrasing like 'Use when...' or 'Do not auto-trigger...' so routers see the boundary.",
                )
            )

    if len(lines) > MAX_SKILL_LINES:
        issues.append(
            Issue(
                "error",
                "conciseness",
                f"SKILL.md has {len(lines)} lines, above the {MAX_SKILL_LINES}-line target.",
                "Move details into references, templates, scripts, or delete low-value prose.",
            )
        )
    elif len(lines) > LONG_SKILL_LINES:
        issues.append(
            Issue(
                "warn",
                "conciseness",
                f"SKILL.md has {len(lines)} lines and is approaching the {MAX_SKILL_LINES}-line target.",
                "Check whether detailed examples belong in a reference file.",
            )
        )

    resource_dirs = {
        "scripts": skill_dir / "scripts",
        "references": skill_dir / "references",
        "templates": skill_dir / "templates",
        "assets": skill_dir / "assets",
        "evals": skill_dir / "evals",
    }
    present_resources = sorted(name for name, resource in resource_dirs.items() if resource.exists())
    for resource in present_resources:
        if resource not in body_lower:
            issues.append(
                Issue(
                    "info",
                    "progressive_disclosure",
                    f"{resource}/ exists but is not named in SKILL.md.",
                    f"Briefly explain when to load or run {resource}/, or remove it if unused.",
                )
            )
    if len(lines) > 220 and not any(resource in present_resources for resource in ["scripts", "references", "templates"]):
        issues.append(
            Issue(
                "warn",
                "progressive_disclosure",
                "Long SKILL.md has no scripts/references/templates directory.",
                "Split durable details into bundled resources if they are still needed.",
            )
        )

    if not has_any(VERIFICATION_PATTERNS, body):
        issues.append(
            Issue(
                "warn",
                "verification",
                "Body does not describe verification, tests, proof, or acceptance evidence.",
                "Add the smallest evidence requirement needed before claiming completion.",
            )
        )

    has_side_effect_surface = has_any(SIDE_EFFECT_PATTERNS, body + "\n" + description)
    if has_side_effect_surface and not has_any(SIDE_EFFECT_POLICY_PATTERNS, body + "\n" + description):
        issues.append(
            Issue(
                "warn",
                "side_effect_policy",
                "Skill mentions side-effectful surfaces without an approval or read-only boundary.",
                "State when writes/posts/commits/API actions are allowed and when to stop.",
            )
        )

    if not (skill_dir / "agents" / "openai.yaml").exists():
        issues.append(
            Issue(
                "info",
                "package_shape",
                "Missing agents/openai.yaml.",
                "Add runtime UI metadata when this skill should be discoverable in Codex-style skill lists.",
            )
        )
    if "evals" not in present_resources and "eval" not in body_lower:
        issues.append(
            Issue(
                "info",
                "eval_coverage",
                "No evals/ directory or eval guidance found.",
                "Add golden invocations or document why runtime evals are not useful for this skill.",
            )
        )
    if not has_any(ANTI_RATIONALIZATION_PATTERNS, body):
        issues.append(
            Issue(
                "info",
                "anti_rationalization",
                "No explicit anti-shortcut or anti-rationalization guidance found.",
                "Name the common agent shortcut this skill must prevent, or leave absent if there is no real failure class.",
            )
        )

    categories = sorted({issue.category for issue in issues})
    return {
        "path": str(skill_dir),
        "name": name or skill_dir.name,
        "description_chars": len(description),
        "line_count": len(lines),
        "resources": present_resources,
        "score": score_from_issues(issues),
        "issue_count": len(issues),
        "issue_categories": categories,
        "issues": [issue.as_dict() for issue in issues],
    }


def add_overlap_findings(results: list[dict[str, Any]]) -> None:
    descriptions = []
    for result in results:
        skill_md = Path(result["path"]) / "SKILL.md"
        meta, _ = frontmatter(read_text(skill_md))
        descriptions.append((result, words(meta.get("description", ""))))
    for index, (left, left_words) in enumerate(descriptions):
        overlaps = []
        for right, right_words in descriptions[index + 1 :]:
            if not left_words or not right_words:
                continue
            score = len(left_words & right_words) / len(left_words | right_words)
            if score >= 0.42:
                overlaps.append({"skill": right["name"], "similarity": round(score, 2)})
                right.setdefault("overlap_candidates", []).append({"skill": left["name"], "similarity": round(score, 2)})
        if overlaps:
            left.setdefault("overlap_candidates", []).extend(overlaps)
    for result in results:
        if result.get("overlap_candidates"):
            result["issues"].append(
                Issue(
                    "info",
                    "overlap",
                    "Description resembles another evaluated skill.",
                    "Review whether the skills should share a reference, clarify boundaries, or merge.",
                ).as_dict()
            )
            result["issue_count"] = len(result["issues"])
            result["issue_categories"] = sorted({issue["category"] for issue in result["issues"]})
            result["score"] = max(0, result["score"] - 3)


def evaluate_paths(paths: list[Path]) -> dict[str, Any]:
    skill_dirs: list[Path] = []
    for path in paths:
        skill_dirs.extend(immediate_skill_dirs(path))
    unique_dirs = sorted({skill.resolve() for skill in skill_dirs})
    results = [evaluate_skill(skill_dir) for skill_dir in unique_dirs]
    if len(results) > 1:
        add_overlap_findings(results)
    severity_counts: dict[str, int] = {"error": 0, "warn": 0, "info": 0}
    for result in results:
        for issue in result["issues"]:
            severity_counts[issue["severity"]] = severity_counts.get(issue["severity"], 0) + 1
    return {
        "summary": {
            "skill_count": len(results),
            "average_score": round(sum(result["score"] for result in results) / len(results), 1) if results else 0,
            "severity_counts": severity_counts,
        },
        "skills": results,
    }


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Skill Quality Report",
        "",
        f"- Skills evaluated: {summary['skill_count']}",
        f"- Average score: {summary['average_score']}",
        f"- Issues: {summary['severity_counts']}",
        "",
        "| Skill | Score | Lines | Issues | Categories |",
        "|---|---:|---:|---:|---|",
    ]
    for result in report["skills"]:
        categories = ", ".join(result["issue_categories"]) or "none"
        lines.append(
            f"| {escape(result['name'])} | {result['score']} | {result['line_count']} | "
            f"{result['issue_count']} | {escape(categories)} |"
        )
    lines.append("")
    for result in report["skills"]:
        if not result["issues"]:
            continue
        lines.extend([f"## {result['name']}", ""])
        if result.get("overlap_candidates"):
            overlaps = ", ".join(f"{item['skill']} ({item['similarity']})" for item in result["overlap_candidates"])
            lines.extend([f"Overlap candidates: {overlaps}", ""])
        for issue in result["issues"]:
            lines.append(f"- **{issue['severity']} / {issue['category']}**: {issue['message']} {issue['suggestion']}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_output(text: str, output: Path | None) -> None:
    if output is None:
        sys.stdout.write(text)
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    print(f"Wrote {output}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="Skill directory or pack root to evaluate")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    parser.add_argument("--output", type=Path, help="Write report to this path")
    args = parser.parse_args()

    report = evaluate_paths(args.paths)
    if args.format == "json":
        write_output(json.dumps(report, indent=2, sort_keys=True) + "\n", args.output)
    else:
        write_output(render_markdown(report), args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
