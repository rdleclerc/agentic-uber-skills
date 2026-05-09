#!/usr/bin/env python3
"""Create a timestamped Uberskillevolver learning-record directory."""
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from string import Template
import re


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "run"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".uberlearn", help="Learning root directory")
    parser.add_argument("--skill", required=True, help="Skill name, e.g. ubergoal")
    parser.add_argument("--run-slug", required=True, help="Short run slug")
    parser.add_argument("--timestamp", default=None, help="Override timestamp YYYYMMDDTHHMMSS")
    args = parser.parse_args()

    stamp = args.timestamp or datetime.now().strftime("%Y%m%dT%H%M%S")
    skill = slugify(args.skill)
    run_slug = slugify(args.run_slug)
    out_dir = Path(args.root) / skill / f"{stamp}-{run_slug}"
    out_dir.mkdir(parents=True, exist_ok=False)

    template_path = Path(__file__).resolve().parents[1] / "templates" / "post-run-learning.md"
    text = template_path.read_text()
    # Keep replacement intentionally light; templates remain editable markdown.
    replacements = {
        "- Skill(s):": f"- Skill(s): {args.skill}",
        "- Date/time:": f"- Date/time: {stamp}",
        "- Run slug:": f"- Run slug: {run_slug}",
    }
    for old, new in replacements.items():
        text = text.replace(old, new, 1)

    record = out_dir / "post-run-learning.md"
    record.write_text(text)
    print(record)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
