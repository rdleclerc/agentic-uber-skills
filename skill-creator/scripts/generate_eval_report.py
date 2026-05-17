#!/usr/bin/env python3
"""Generate a compact static HTML review report for skill eval iterations."""
from __future__ import annotations

import argparse
import html
import json
from collections import Counter
from pathlib import Path

VALID_VERDICTS = {"pass", "partial", "fail", "blocked"}


def esc(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def normalize_verdict(value: object) -> str:
    verdict = str(value or "blocked").strip().lower()
    return verdict if verdict in VALID_VERDICTS else "blocked"


def render_report(data: dict) -> str:
    cases = data.get("cases") or []
    counts = Counter(normalize_verdict(case.get("verdict")) for case in cases if isinstance(case, dict))
    skill_name = esc(data.get("skill_name", "skill"))
    iteration = esc(data.get("iteration", "iteration"))
    rows: list[str] = []
    for index, case in enumerate(cases, start=1):
        if not isinstance(case, dict):
            continue
        verdict = normalize_verdict(case.get("verdict"))
        rows.append(
            f"""
            <article class="case verdict-{verdict}">
              <header>
                <span class="case-id">{esc(case.get("id", f"eval-{index}"))}</span>
                <span class="verdict">{esc(verdict)}</span>
              </header>
              <h2>{esc(case.get("prompt", "Untitled eval"))}</h2>
              <dl>
                <dt>Expected</dt><dd>{esc(case.get("expected", ""))}</dd>
                <dt>With Skill</dt><dd>{esc(case.get("with_skill", ""))}</dd>
                <dt>Without Skill</dt><dd>{esc(case.get("without_skill", ""))}</dd>
                <dt>Notes</dt><dd>{esc(case.get("notes", ""))}</dd>
              </dl>
            </article>
            """
        )

    tuning = data.get("description_tuning") if isinstance(data.get("description_tuning"), dict) else {}
    held_out = tuning.get("held_out_examples") or []
    held_out_items = "\n".join(f"<li>{esc(item)}</li>" for item in held_out)
    summary_counts = " ".join(
        f'<span class="pill {verdict}">{verdict}: {counts.get(verdict, 0)}</span>'
        for verdict in ["pass", "partial", "fail", "blocked"]
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{skill_name} Eval Report</title>
  <style>
    :root {{ color-scheme: light; --ink:#17202a; --muted:#586575; --line:#d8dee8; --bg:#f7f9fc; --panel:#ffffff; }}
    body {{ margin:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; color:var(--ink); background:var(--bg); }}
    main {{ max-width:1100px; margin:0 auto; padding:32px 20px 48px; }}
    header.hero {{ border-bottom:1px solid var(--line); margin-bottom:22px; padding-bottom:18px; }}
    h1 {{ margin:0 0 8px; font-size:28px; letter-spacing:0; }}
    p {{ line-height:1.5; }}
    .meta, .counts {{ color:var(--muted); display:flex; flex-wrap:wrap; gap:8px; }}
    .pill {{ border:1px solid var(--line); border-radius:999px; padding:4px 9px; background:var(--panel); font-size:13px; }}
    .pass {{ border-color:#7bc99a; }} .partial {{ border-color:#e5bd5a; }} .fail {{ border-color:#dc7d7d; }} .blocked {{ border-color:#9ba7b7; }}
    .case {{ background:var(--panel); border:1px solid var(--line); border-left-width:5px; border-radius:8px; padding:18px; margin:16px 0; }}
    .verdict-pass {{ border-left-color:#34a853; }} .verdict-partial {{ border-left-color:#d59b00; }} .verdict-fail {{ border-left-color:#c5221f; }} .verdict-blocked {{ border-left-color:#748094; }}
    .case header {{ display:flex; justify-content:space-between; gap:12px; align-items:center; }}
    .case-id {{ color:var(--muted); font-size:13px; }}
    .verdict {{ font-weight:700; text-transform:uppercase; font-size:12px; }}
    .case h2 {{ font-size:18px; margin:10px 0 14px; }}
    dl {{ display:grid; grid-template-columns:minmax(110px, 160px) 1fr; gap:10px 14px; margin:0; }}
    dt {{ color:var(--muted); font-weight:700; }}
    dd {{ margin:0; white-space:pre-wrap; }}
    section {{ margin-top:28px; }}
    code {{ background:#eef2f7; padding:1px 4px; border-radius:4px; }}
  </style>
</head>
<body>
  <main>
    <header class="hero">
      <h1>{skill_name} Eval Report</h1>
      <div class="meta"><span>{iteration}</span><span>{len(rows)} cases</span></div>
      <p>{esc(data.get("summary", ""))}</p>
      <div class="counts">{summary_counts}</div>
    </header>
    <section aria-label="Eval cases">
      {''.join(rows)}
    </section>
    <section aria-label="Description tuning">
      <h2>Description Tuning</h2>
      <dl>
        <dt>Old</dt><dd>{esc(tuning.get("old", ""))}</dd>
        <dt>New</dt><dd>{esc(tuning.get("new", ""))}</dd>
        <dt>Held-out examples</dt><dd><ul>{held_out_items}</ul></dd>
      </dl>
    </section>
  </main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Eval report JSON path")
    parser.add_argument("output", type=Path, help="HTML output path")
    args = parser.parse_args()
    data = json.loads(args.input.read_text())
    if not isinstance(data, dict):
        raise SystemExit("input JSON must be an object")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_report(data))
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
