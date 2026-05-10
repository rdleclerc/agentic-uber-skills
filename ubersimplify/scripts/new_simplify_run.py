#!/usr/bin/env python3
"""Create a timestamped ubersimplify trail directory."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import re

TEMPLATES = [
    "simplify-plan.md",
    "complexity-inventory.md",
    "modularity-audit.md",
    "dead-code-audit.md",
    "test-confidence.md",
    "simplification-candidates.md",
    "patch-log.md",
    "final-simplification-report.md",
]


def slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return value or "simplify-run"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".ubersimplify", help="Trail root directory")
    parser.add_argument("--run-slug", required=True, help="Short run slug")
    parser.add_argument("--mode", choices=["audit", "plan", "patch"], default="audit")
    parser.add_argument("--timestamp", default=None, help="Override timestamp, e.g. 20260509T101500Z")
    args = parser.parse_args()

    stamp = args.timestamp or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = f"{stamp}-{slugify(args.run_slug)}"
    out = Path(args.root) / run_id
    out.mkdir(parents=True, exist_ok=False)
    template_dir = Path(__file__).resolve().parents[1] / "templates"
    for name in TEMPLATES:
        text = (template_dir / name).read_text()
        text = text.replace("- Run ID:", f"- Run ID: {run_id}")
        text = text.replace("- Timestamp:", f"- Timestamp: {stamp}")
        text = text.replace("- Mode: audit | plan | patch", f"- Mode: {args.mode}")
        text = text.replace("- Trail path:", f"- Trail path: {out}")
        (out / name).write_text(text)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
