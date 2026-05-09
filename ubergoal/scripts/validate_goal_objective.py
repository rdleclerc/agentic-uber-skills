#!/usr/bin/env python3
"""Validate that a Codex goal objective is compact enough for continuation."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

DEFAULT_MAX_CHARS = 3_999
DEFAULT_TARGET_CHARS = 3_400
WARN_CHARS = 3_800


def objective_text(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    if text.startswith("/goal"):
        rest = text[len("/goal") :]
        if rest.startswith((" ", "\n", "\t")):
            return rest.strip()
    return text


def read_input(path: Path | None) -> str:
    if path is not None:
        return path.read_text(encoding="utf-8")
    return sys.stdin.read()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, help="File containing a /goal command or objective.")
    parser.add_argument("--max-chars", type=int, default=DEFAULT_MAX_CHARS)
    parser.add_argument("--target-chars", type=int, default=DEFAULT_TARGET_CHARS)
    parser.add_argument("--strict-target", action="store_true")
    args = parser.parse_args()

    objective = objective_text(read_input(args.path))
    count = len(objective)
    print(f"objective_chars={count}")
    print(f"target_chars={args.target_chars}")
    print(f"max_chars={args.max_chars}")
    if count > args.max_chars:
        print("error=objective exceeds Codex goal objective limit", file=sys.stderr)
        return 1
    if count >= WARN_CHARS:
        print("warning=objective is near the hard limit; compress before use", file=sys.stderr)
        return 1
    if count > args.target_chars:
        print("warning=objective exceeds target length", file=sys.stderr)
        if args.strict_target:
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
