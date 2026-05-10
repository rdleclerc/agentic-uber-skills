---
name: uberassess
description: "Do not auto-trigger from task similarity. Use only when explicitly asked to assess a source/research signal for possible adoption or routed by ubergoal: X/Twitter posts, bookmarked links, articles, GitHub repos, arXiv/papers, videos, Hermes/bookmark signals, or internal artifacts. Produces a source-grounded recommendation packet, not implementation."
---

# Uberassess

## Core rule

`uberassess` turns external signals into **source-grounded recommendations**. It does not implement, mutate project state, or launch work without explicit approval.

Use the lightest tier that can answer: **is this idea worth adopting, watching, archiving, rejecting, or turning into an eval seed?** Most interesting sources should not become implementation plans.

Direct-use only when explicitly named, when the user explicitly asks to assess/evaluate a source or artifact for adoption, or when routed by `ubergoal`.

## Relationship to Ubergoal

- `uberassess` is a pre-planning assessment phase.
- If the recommendation is approved for code/skill/workflow changes, hand off to `$ubergoal`/`$uberplan` with the packet as evidence.
- If the source suggests only memory, watchlist, or eval work, do not escalate to implementation.
- Hermes may consume or propose assessment packets as read-only candidate signals; Hermes should not mutate Type0/Gaia/OpenClaw in v0.

## Tiers

| Tier | Use for | Output |
|---|---|---|
| 0 | Quick triage of low-stakes links | save / ignore / needs deeper assessment |
| 1 | Normal source assessment | `templates/assessment-packet.md` |
| 2 | Important idea likely to affect systems | packet + project context freshness + benefit >> cost + eval seed |
| 3 | Likely code/skill/workflow/agentic-system change | Tier 2 + Agent Advocate RCA + `$ubergoal` handoff + evidence plan |

Escalate only for concrete risk. Do not spend Tier 3 effort on every bookmark.

## Procedure

1. **Resolve the source.** Capture raw source handles before summarizing. Use source-specific tools/skills when available, e.g. X bookmark/Type0 resolvers, GitHub tooling, arXiv/PDF extraction, web fetch/browser, or transcript/OCR sidecars. Record failures and uninspected media.
2. **Create a Source Packet.** Use `templates/source-packet.md` or embed its fields in the assessment packet. Separate raw source, linked sources, retrieval limits, synthesis, and uncertainty.
3. **Check project context.** Inspect the relevant project/source-of-truth paths/cards/docs enough to avoid stale or duplicate recommendations. Use local adapter references when present (for example Type0/Gaia/Soho/Hermes on Rob's machine), but do not force unrelated local projects into portable assessments. Record context freshness and gaps.
4. **Extract ideas and claims.** Distinguish author claims from your inferences. Record evidence quality and contradiction risk.
5. **Run benefit >> cost.** Ask what to delete or simplify first. Prefer notes, eval seeds, or tool/context fixes over new machinery unless benefit is clearly much greater than hidden cost.
6. **Run Agent Advocate when agent systems are involved.** Ask the human counterfactual: would a competent human with the same context/tools have made the error? If not, identify the missing context, source authority, tool feedback, memory, affordance, or approval boundary.
7. **Decide.** Choose Adopt now, Watch, Archive, Reject, Needs more research, or Convert to eval only.
8. **Set approval boundary.** State `Implementation before approval: no`. If approved, provide a compact `$ubergoal` handoff and evidence plan.
9. **Leave a learning trail.** For accepted/rejected high-signal assessments, note how outcome should feed `$uberskillevolver` or Hermes later.

## Output contract

For Tier 1+, produce an assessment packet with:

- source URL/type and raw capture status
- linked sources/media inspected and retrieval limitations
- key ideas, author claims, and model inferences
- project relevance matrix and project context freshness
- source authority, uncertainty, contradictions, and freshness
- benefit >> complexity cost analysis and simpler alternatives
- decision and rationale
- approval boundary and side effects
- if implementation is likely: `$ubergoal` handoff, evidence plan, rollback/stop condition
- if agentic systems are implicated: Agent Advocate human counterfactual and affordance gap
- outcome-learning trail for future evolver/Hermes review

Use `scripts/validate_assessment_packet.py` before treating a Tier 1+ packet as complete.

## Do not build yet by default

Do not create MCP servers, scrapers, vector indexes, scheduled automation, model swaps, or new persistent state during assessment. Recommend them only after repeated usage proves a stable interface and benefit >> cost.

## Helpful resources

- `templates/assessment-packet.md` — canonical recommendation packet.
- `templates/source-packet.md` — source capture subtemplate.
- `templates/project-context-card.md` — lightweight project context card.
- `references/source-resolvers.md` — source-type handling and limitations.
- `references/project-routing.md` — routing destinations and non-goals.
- `references/hermes-and-approval.md` — Hermes/read-only and approval policy.
- `scripts/validate_assessment_packet.py` — packet validator.
