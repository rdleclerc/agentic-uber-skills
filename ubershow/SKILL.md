---
name: ubershow
description: "Use when the user needs high-bandwidth visual communication rather than a text wall: browser-first HTML decision boards, implementation plans, questionnaires, architecture/source/code-review maps, status or incident reports, visual briefs, or interactive decision receipts for Codex/Claude coding workflows. Produces local self-contained HTML artifacts as generated views while preserving Markdown/source/ledger authority."
---

# Ubershow

## Core rule

Use the smallest visual artifact that materially improves the user's decision speed. Do **not** turn every answer into HTML. Text, Markdown, a table, or Mermaid is still better for simple answers, small diffs, and canonical records.

`ubershow` is a browser-first presentation/decision-surface skill for Codex/Claude coding work. It helps the user see, compare, tune, and choose. It does **not** replace source documents, ledgers, specs, tests, or session logs.

## Decision registration

HTML clicks do not automatically register with the agent. For v0, every decision artifact that asks the user to choose must include a **copyable decision receipt**.

Protocol:

1. User opens/reviews the HTML artifact.
2. User selects/edits the decision in the artifact.
3. User clicks **Copy decision for Codex/Claude**.
4. User pastes the receipt into chat.
5. Agent records the receipt in the canonical session log, ADR, issue, or Markdown handoff and proceeds.

Do not imply that selecting an option in HTML alone is durable. A local write-back server or JSON decision sink is a future upgrade only when repeated usage justifies the extra machinery.

## Source authority

HTML artifacts are generated **views**, not canonical truth.

Canonical layers stay in their normal homes:

1. raw sources / original records
2. ledgers / approvals / side-effect receipts
3. curated Markdown, ADRs, session logs, issues, or project docs
4. generated HTML / screenshots / dashboards
5. retrieval/search/index results

If the artifact influences a durable decision, write or update the appropriate Markdown/ledger/source note. If another agent must continue the work, include a concise handoff summary in text or Markdown, not only HTML.

Obsidian/Soho House is optional archive context only. Ubershow artifacts are for browser/Codex/Claude coding surfaces first; do not design around Obsidian-native interactive rendering.

## When to use

Use for:

- decision boards and option comparisons
- implementation plans with milestones, flows, risky code, or approval gates
- questionnaires or answer collection
- architecture/system explainers
- codebase maps and PR/change explainers
- research reports with source maps and evidence cards
- status reports, incident timelines, operational dashboards
- visual design/prototype review
- prompt/config/taste tuners with sliders/toggles/copy buttons
- any explicit request like “show me visually,” “make this easier to understand,” “I need to decide fast,” or “Markdown/text is not enough.”

Skip for:

- short factual answers
- small code edits
- purely canonical docs/specs where diffability matters most
- sensitive data that should not be rendered into a shareable artifact
- cases where a simple table or Mermaid diagram is enough

## Choose an output mode

Pick one mode; do not overbuild.

| Mode | Template | Purpose |
|---|---|---|
| Visual brief | `templates/visual-brief.html` | fast situational awareness, verdict, evidence cards, next actions |
| Decision board | `templates/decision-board.html` | choose among options, tradeoffs, recommendation, receipt |
| Implementation plan | `templates/implementation-plan.html` | milestones, data/control flow, risk table, approval receipt |
| Questionnaire | `templates/questionnaire.html` | grouped choices, notes, copyable answer receipt |
| Architecture map | `templates/architecture-map.html` | lanes, contracts, source authority, failure modes |
| Code review map | `templates/code-review-map.html` | file risk map, blockers, review decision receipt |
| Status timeline | `templates/status-timeline.html` | current state, metrics, timeline, proceed/pause receipt |

Use `schemas/decision-board.schema.json` only when structured input helps. Do not invent a schema system for every artifact unless repeated failures prove it is needed.

## Workflow

1. **Clarify the job.** State the decision or understanding task the artifact accelerates.
2. **Choose the smallest mode.** Prefer one self-contained page over a mini-app.
3. **Gather sources.** Cite file paths, URLs, commits, traces, logs, or notes used to build the artifact.
4. **Copy a template if useful.** Start from one file under `templates/`; edit inline. Final artifacts must be self-contained.
5. **Place it safely.** Use a generated-artifact directory such as `/Users/claw1/.openclaw/runtime/ubershow/`, repo `runtime/reports/`, `/tmp`, or a project-specific generated folder. Do not put generated HTML in canonical source lanes unless explicitly requested.
6. **Include a receipt.** Any artifact requiring a choice must include a `decision-receipt` block and copy button.
7. **Render/verify when possible.** Open or screenshot the artifact and fix obvious rendering issues.
8. **Summarize in text.** Final response includes artifact path plus concise recommendation/status.
9. **Record durable decisions separately.** Move final choices into Markdown/session log/ADR/issue as needed.

## Artifact constraints

- Self-contained HTML by default: no CDN, remote fonts, analytics, or external script/style dependencies.
- Scope budget: one page and one output mode by default.
- Collision safety: timestamp generated filenames; do not overwrite existing artifacts unless asked.
- Responsive and accessible: semantic headings, `<main>`, `<section>`, real `<button>`/form controls, sufficient contrast, keyboard-friendly controls.
- Decision-first: recommendation/open questions visible above the fold.
- Evidence-visible: show source handles and confidence/uncertainty.
- Copyable outputs: include copy blocks/buttons for decisions, prompts, configs, answers, or next instructions when useful.
- Diff-aware: if the artifact matters long-term, also create or update a small Markdown handoff because HTML diffs are noisy.
- Privacy-aware: do not render secrets, credentials, private messages, health/financial/legal data, or personal contact details unless the user explicitly approved that lane and destination.
- Secret check: when source material may contain private data, run a lightweight secret/privacy scan or manual check before finalizing.

## Suggested generated filenames

```text
/Users/claw1/.openclaw/runtime/ubershow/YYYY-MM-DD-topic-decision-board.html
/Users/claw1/.openclaw/runtime/ubershow/YYYY-MM-DD-topic-implementation-plan.html
<repo>/runtime/reports/YYYY-MM-DD-pr-123-review-map.html
/tmp/ubershow-<slug>.html
```

If rendering a screenshot:

```text
/Users/claw1/.openclaw/runtime/ubershow/YYYY-MM-DD-topic-decision-board.png
```

## Quality check before final

- Does the artifact answer a concrete decision or comprehension need?
- Is it clearly better than a normal text/table response?
- Are sources and uncertainty visible?
- Is generated HTML clearly non-canonical?
- Is there a decision receipt if the user must choose?
- Is there a text/Markdown handoff when future agents need to continue?
- Are secrets/private lanes protected?
- Did you verify it renders if tooling was available?

## First-principles simplifier

Before spending time on a visual artifact, ask: “Can the same decision be made with a five-line answer or a simple table?” If yes, skip `ubershow` and answer normally.
