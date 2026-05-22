---
name: uberassess
description: "Do not auto-trigger from task similarity. Use only when explicitly asked to assess or deeply research a source, idea seed, open research question, or implementation question for possible adoption, or routed by ubergoal: X/Twitter posts, bookmarked links, articles, GitHub repos, arXiv/papers, videos, Hermes/bookmark signals, internal artifacts, scraps of ideas, alternatives research, and codebase/docs/forum/GitHub reconnaissance. Produces a source-grounded recommendation packet, not implementation."
---

# Uberassess

## Core rule

`uberassess` turns external signals, idea seeds, and implementation questions into **source-grounded recommendations**. It owns pre-planning research: clarify what question is really being asked, inspect enough outside and local evidence to avoid stale guesses, and recommend adopt/watch/archive/reject/eval/plan. It does not implement, mutate project state, or launch work without explicit approval.

Use the lightest tier that can answer: **is this idea worth adopting, watching, archiving, rejecting, or turning into an eval seed?** Most interesting sources should not become implementation plans.

Direct-use only when explicitly named, when the user explicitly asks to assess/evaluate/research a source, artifact, idea, or implementation question for adoption, or when routed by `ubergoal`.

## Relationship to Ubergoal

- `uberassess` is a pre-planning assessment phase.
- If the recommendation is approved for code/skill/workflow changes, hand off to `$ubergoal`/`$uberplan` with the packet as evidence.
- If the source suggests only memory, watchlist, or eval work, do not escalate to implementation.
- Hermes may consume or propose assessment packets as read-only candidate signals; Hermes should not mutate Type0/Gaia/OpenClaw in v0.

## Tiers

| Tier | Use for | Output |
|---|---|---|
| 0 | Quick triage of low-stakes links | save / ignore / needs deeper assessment |
| 1 | Normal source or contained idea assessment | `templates/assessment-packet.md` |
| 2 | Important idea/question likely to affect systems, architecture, skills, tools, or project direction | packet + research frame/source map + project context freshness + alternatives/prior art + benefit >> cost + eval seed |
| 3 | Likely code/skill/workflow/agentic-system change | Tier 2 + Agent Advocate RCA + `$ubergoal` handoff + evidence plan |

Escalate only for concrete risk. Do not spend Tier 3 effort on every bookmark.

## Procedure

0. **Frame the assessment question.** Restate the seed in one sentence, identify whether this is source-first, idea-first, implementation-question, or mixed, and name the research mode: quick source assessment or Deep Research Assessment. If the input is vague, define the smallest useful question instead of asking the user to over-specify.
1. **Resolve the source or seed.** Capture raw source handles before summarizing. For source-first work, use source-specific tools/skills when available, e.g. X bookmark/Type0 resolvers, GitHub tooling, arXiv/PDF extraction, web fetch/browser, or transcript/OCR sidecars. For idea-first work, record the user's wording as the raw seed and label it `idea_seed`, `implementation_question`, or `open_research_question`. Record failures and uninspected media.
2. **Create a Source Packet.** Use `templates/source-packet.md` or embed its fields in the assessment packet. Separate raw source/seed, linked sources, retrieval limits, synthesis, and uncertainty.
3. **Build the research map.** For Deep Research Assessment, intentionally choose lanes: local codebase/source-of-truth, primary docs/specs, GitHub alternatives/prior art, issues/forums/practitioner discussion, papers/blogs where relevant, and contradiction search. State coverage claimed and not claimed; never imply exhaustive research when only a slice was inspected.
4. **Check project context.** Inspect the relevant project/source-of-truth paths/cards/docs enough to avoid stale or duplicate recommendations. Use local adapter references when present (for example Type0/Gaia/Soho/Hermes on Rob's machine), but do not force unrelated local projects into portable assessments. Record context freshness and gaps.
5. **Extract ideas and claims.** Distinguish user/source/author claims from your inferences. Record evidence quality, contradiction risk, local fit, and what is actually actionable.
6. **Compare alternatives.** For implementation questions and architecture/tool ideas, produce an alternatives/prior-art matrix. Include the "do nothing / note / eval-only / improve context or skill" option alongside new machinery.
7. **Run benefit >> cost.** Ask what to delete or simplify first. Prefer notes, eval seeds, or tool/context fixes over new machinery unless benefit is clearly much greater than hidden cost.
8. **Run Agent Advocate when agent systems are involved.** Ask the human counterfactual: would a competent human with the same context/tools have made the error? If not, identify the missing context, source authority, tool feedback, memory, affordance, or approval boundary.
9. **Decide.** Choose Adopt now, Watch, Archive, Reject, Needs more research, or Convert to eval only.
10. **Set approval boundary.** State `Implementation before approval: no`. If approved, provide a compact `$ubergoal`/`$uberplan` handoff and evidence plan.
11. **Leave a learning trail.** For accepted/rejected high-signal assessments, note how outcome should feed `$uberskillevolver` or Hermes later.

## Deep Research Assessment mode

Use this mode when the user says "boil the ocean," asks for deep research, requests alternatives or state-of-the-art, gives only a scrap of an idea, or asks an implementation/architecture question before planning. The job is not to gather every possible source; it is to make the research boundary honest and broad enough that a later plan is not built on vibes.

Minimum lanes to consider:

- **Seed/source capture** — exact user wording, source URL, linked artifacts, raw media/transcripts, and retrieval limits.
- **Question framing** — what decision this assessment must support and what would be overreach.
- **Local project context** — current codebase, skills, docs, tests, policies, and duplicate/prior attempts.
- **Primary docs/specs** — official docs and source-of-truth references such as OpenClaw docs when relevant.
- **Alternatives/prior art** — GitHub repos, libraries, patterns, architecture options, and why they do or do not transfer.
- **Practitioner evidence** — issues, discussions, forums, postmortems, or threads that reveal real pain and edge cases.
- **Contradiction search** — evidence the idea is stale, solved, unsafe, too expensive, or better handled by deletion/simplification.
- **Adoption fit** — whether the output should be a memory note, watch item, eval seed, rejected idea, or `$ubergoal`/`$uberplan` handoff.

Stop research when additional sources are unlikely to change the recommendation, the coverage gap itself is the recommendation, or approval is needed for paid/private/side-effecting access.

## Output contract

For Tier 1+, produce an assessment packet with:

- source URL/type and raw capture status
- assessment mode and research question
- research/source map with coverage claimed and not claimed
- linked sources/media inspected and retrieval limitations
- key ideas, author claims, and model inferences
- alternatives/prior-art matrix when implementation or architecture choices are implicated
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
