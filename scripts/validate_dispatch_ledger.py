#!/usr/bin/env python3
"""Validate dispatch ledger table rows and duplicate-cull discipline."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED = ["id", "work_item", "root", "launched_at", "exit", "output_path", "retry_count"]
EMPTY = {"", "todo", "tbd", "n/a", "none", "<id>", "<path>"}


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")


def table_rows(text: str) -> tuple[list[str], list[dict[str, str]]]:
    lines = [line for line in text.splitlines() if line.strip().startswith("|")]
    if not lines:
        return [], []
    header = [normalize(cell) for cell in lines[0].strip().strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for line in lines[1:]:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells or all(set(cell) <= {"-", ":", " "} for cell in cells):
            continue
        cells.extend([""] * (len(header) - len(cells)))
        rows.append(dict(zip(header, cells)))
    return header, rows


def validate(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"{path}: cannot read ledger: {exc}"]
    header, rows = table_rows(text)
    errors: list[str] = []
    missing = [name for name in REQUIRED if name not in header]
    if missing:
        errors.append(f"{path}: missing required column(s): {', '.join(missing)}")
        return errors
    if not rows:
        return [f"{path}: no dispatch ledger rows found"]
    non_retry_by_work_item: dict[str, str] = {}
    for row_no, row in enumerate(rows, start=1):
        for field in REQUIRED:
            if row.get(field, "").strip().lower() in EMPTY:
                errors.append(f"{path}: row {row_no} empty field: {field}")
        retry_raw = row.get("retry_count", "")
        if not re.fullmatch(r"\d+", retry_raw.strip()):
            errors.append(f"{path}: row {row_no} retry_count must be a nonnegative integer")
            continue
        if int(retry_raw) == 0:
            work_item = row["work_item"].strip()
            if work_item in non_retry_by_work_item:
                errors.append(
                    f"{path}: duplicate non-retry work_item {work_item!r} "
                    f"rows {non_retry_by_work_item[work_item]} and {row_no}"
                )
            non_retry_by_work_item[work_item] = str(row_no)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    args = parser.parse_args()
    errors = validate(args.ledger)
    if errors:
        print("FAIL: dispatch ledger validation failed", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"PASS: dispatch ledger {args.ledger} is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
