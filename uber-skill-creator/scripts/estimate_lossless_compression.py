#!/usr/bin/env python3
"""Estimate conservative token savings for skill/plan markdown compression.

This is an estimator, not an auto-rewriter. Safe savings are whitespace-only.
Advisory savings are candidates that require human/test review before patching.
"""
from __future__ import annotations

import argparse
import glob
import json
import math
from pathlib import Path
import re
import sys
from collections import Counter

PROTECTED_PATTERNS = [
    re.compile(r"do not auto-trigger from task similarity", re.I),
    re.compile(r"^---$"),
    re.compile(r"^(name|description):", re.I),
    re.compile(r"^\s*[\"']?(user_prompt|required_behavior|expected_behavior|forbidden_behavior|id)[\"']?\s*:", re.I),
]


def estimate_tokens(text: str) -> int:
    """Approximate GPT-style tokens without external dependencies."""
    if not text:
        return 0
    # Markdown-heavy English generally lands near 3.7-4.2 chars/token.
    return max(1, math.ceil(len(text) / 4.0))


def whitespace_compress(text: str) -> str:
    lines = [line.rstrip() for line in text.splitlines()]
    out: list[str] = []
    blank_count = 0
    for line in lines:
        if line.strip():
            blank_count = 0
            out.append(line)
        else:
            blank_count += 1
            if blank_count <= 1:
                out.append("")
    return "\n".join(out).strip() + "\n"


def protected_line(line: str) -> bool:
    return any(pattern.search(line) for pattern in PROTECTED_PATTERNS)


def contraction_candidate_savings(text: str) -> tuple[int, int]:
    """Return occurrences and estimated tokens saved by do not -> don't outside protected lines."""
    occurrences = 0
    chars_saved = 0
    for line in text.splitlines():
        if protected_line(line):
            continue
        matches = re.findall(r"\b[Dd]o not\b", line)
        occurrences += len(matches)
        chars_saved += len(matches) * (len("do not") - len("don't"))
    return occurrences, estimate_tokens("x" * chars_saved) if chars_saved else 0


def repeated_line_candidates(paths: list[Path]) -> tuple[int, list[tuple[str, int, int]]]:
    lines: Counter[str] = Counter()
    for path in paths:
        for line in path.read_text(errors="replace").splitlines():
            norm = re.sub(r"\s+", " ", line.strip())
            if len(norm) < 80 or protected_line(norm) or norm.startswith("|"):
                continue
            lines[norm] += 1
    candidates: list[tuple[str, int, int]] = []
    total_chars = 0
    for line, count in lines.items():
        if count < 2:
            continue
        # Rough estimate: keep one canonical line plus 40-char pointer per duplicate.
        saved = max(0, (len(line) * (count - 1)) - (40 * (count - 1)))
        if saved:
            total_chars += saved
            candidates.append((line, count, estimate_tokens("x" * saved)))
    candidates.sort(key=lambda item: item[2], reverse=True)
    return estimate_tokens("x" * total_chars) if total_chars else 0, candidates[:10]


def analyze_file(path: Path) -> dict[str, object]:
    text = path.read_text(errors="replace")
    safe = whitespace_compress(text)
    contractions, contraction_tokens = contraction_candidate_savings(text)
    return {
        "path": str(path),
        "chars": len(text),
        "estimated_tokens": estimate_tokens(text),
        "safe_whitespace_tokens_saved": max(0, estimate_tokens(text) - estimate_tokens(safe)),
        "advisory_do_not_to_dont_occurrences": contractions,
        "advisory_do_not_to_dont_tokens_saved": contraction_tokens,
    }


def markdown_report(rows: list[dict[str, object]], repeated_tokens: int, repeated: list[tuple[str, int, int]]) -> str:
    total_tokens = sum(int(row["estimated_tokens"]) for row in rows)
    safe = sum(int(row["safe_whitespace_tokens_saved"]) for row in rows)
    contraction_tokens = sum(int(row["advisory_do_not_to_dont_tokens_saved"]) for row in rows)
    contraction_occ = sum(int(row["advisory_do_not_to_dont_occurrences"]) for row in rows)
    out = [
        "# Lossless Compression Estimate",
        "",
        "Estimator notes: token counts are approximate (`ceil(chars / 4)`). Safe savings are whitespace-only. Advisory savings require human/test review before editing.",
        "",
        "## Totals",
        "",
        f"- Files scanned: {len(rows)}",
        f"- Estimated tokens now: {total_tokens}",
        f"- Safe whitespace-only estimated savings: {safe}",
        f"- Advisory `do not` → `don't` occurrences outside protected lines: {contraction_occ}",
        f"- Advisory `do not` → `don't` estimated savings: {contraction_tokens}",
        f"- Advisory repeated-line extraction estimated savings: {repeated_tokens}",
        "",
        "## Per file",
        "",
        "| File | Est. tokens | Safe whitespace saved | `do not` candidates | `do not` est. saved |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in sorted(rows, key=lambda r: int(r["estimated_tokens"]), reverse=True):
        out.append(
            f"| `{row['path']}` | {row['estimated_tokens']} | {row['safe_whitespace_tokens_saved']} | "
            f"{row['advisory_do_not_to_dont_occurrences']} | {row['advisory_do_not_to_dont_tokens_saved']} |"
        )
    if repeated:
        out.extend(["", "## Top repeated-line extraction candidates", "", "| Count | Est. saved | Line |", "|---:|---:|---|"])
        for line, count, tokens in repeated:
            safe_line = line.replace("|", "\\|")
            out.append(f"| {count} | {tokens} | `{safe_line}` |")
    return "\n".join(out) + "\n"


def resolve_paths(inputs: list[str]) -> list[Path]:
    paths: list[Path] = []
    for item in inputs:
        path = Path(item)
        if path.is_dir():
            if (path / "SKILL.md").exists():
                paths.append(path / "SKILL.md")
                paths.extend(sorted(path.glob("**/*.md")))
            else:
                skill_files = sorted(path.glob("*/SKILL.md"))
                paths.extend(skill_files)
                if not skill_files:
                    paths.extend(sorted(path.glob("*.md")))
        elif path.exists():
            paths.append(path)
        else:
            matches = sorted(Path(match) for match in glob.glob(item, recursive=True))
            paths.extend(match for match in matches if match.is_file())
    seen: set[Path] = set()
    unique: list[Path] = []
    for path in paths:
        resolved = path.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(path)
    return unique


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="Skill root(s), SKILL.md files, plan markdown files, or globs")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    paths = resolve_paths(args.paths)
    if not paths:
        print("no input files matched", file=sys.stderr)
        return 2
    rows = [analyze_file(path) for path in paths]
    repeated_tokens, repeated = repeated_line_candidates(paths)
    if args.format == "json":
        print(json.dumps({"files": rows, "advisory_repeated_line_tokens_saved": repeated_tokens}, indent=2))
    else:
        print(markdown_report(rows, repeated_tokens, repeated))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
