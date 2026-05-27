---
name: uberassess
description: "Do not auto-trigger from task similarity. Use only when explicitly asked to assess or deeply research a source, plan artifact, idea seed, open research question, or implementation question for possible adoption, or routed by ubergoal: X/Twitter posts, bookmarked links, articles, GitHub repos, arXiv/papers, videos, Hermes/bookmark signals, internal artifacts, draft plans, planning packets, scraps of ideas, alternatives research, and codebase/docs/forum/GitHub reconnaissance. Produces a source-grounded recommendation packet, not implementation."
---

# Uberassess

## Core rule

`uberassess` turns external signals, plan artifacts, idea seeds, and implementation questions into **source-grounded recommendations**. It owns pre-planning research: clarify what question is really being asked, inspect enough outside and local evidence to avoid stale guesses, and recommend adopt/watch/archive/reject/eval/plan. It does not implement, mutate project state, or launch work without explicit approval.

Use the lightest tier that can answer: **is this idea worth adopting, watching, archiving, rejecting, or turning into an eval seed?** Most interesting sources should not become implementation plans.

Direct-use only when explicitly named, when the user explicitly asks to assess/evaluate/research a source, plan, artifact, idea, or implementation question for adoption, or when routed by `ubergoal`.

## Relationship to Ubergoal

- `uberassess` is a pre-planning assessment phase.
- If the recommendation is approved for code/skill/workflow changes, hand off to `$ubergoal`/`$uberplan` with the packet as evidence.
- If the source suggests only memory, watchlist, or eval work, do not escalate to implementation.
- Hermes may consume or propose assessment packets as read-only candidate signals; Hermes should not mutate Type0/Gaia/OpenClaw in v0.

## Tiers

| Tier | Use for | Output |
|---|---|---|
| 0 | Quick triage of low-stakes links | save / ignore / needs deeper assessment |
| 1 | Normal source, plan, or contained idea assessment | `templates/assessment-packet.md` |
| 2 | Important idea/question likely to affect systems, architecture, skills, tools, or project direction | packet + research frame/source map + project context freshness + alternatives/prior art + benefit >> cost + eval seed |
| 3 | Likely code/skill/workflow/agentic-system change | Tier 2 + Agent Advocate RCA + `$ubergoal` handoff + evidence plan |

Escalate only for concrete risk. Do not spend Tier 3 effort on every bookmark.

## Procedure

0. **Frame the assessment question.** Restate the seed in one sentence, identify whether this is source-first, plan-artifact, idea-first, implementation-question, or mixed, and name the research mode: quick source assessment or Deep Research Assessment. If the input is vague, define the smallest useful question instead of asking the user to over-specify.
1. **Clarify before broad research when it matters.** Ask one to three targeted questions when the answer would materially change research direction, source lanes, cost, privacy/side-effect boundaries, or adoption criteria. Do not send a generic questionnaire. If the ambiguity is low-risk or the user asked for speed, state assumptions and proceed; record unanswered clarifications as coverage gaps.
2. **Resolve the source or seed.** Capture raw source handles before summarizing. For source-first work, use source-specific tools/skills when available, e.g. X bookmark/Type0 resolvers, GitHub tooling, arXiv/PDF extraction, web fetch/browser, or transcript/OCR sidecars. For plan-artifact work, capture the draft plan as the raw source and label it `plan_artifact`. For idea-first work, record the user's wording as the raw seed and label it `idea_seed`, `implementation_question`, or `open_research_question`. Record failures and uninspected media.
3. **Create a Source Packet.** Use `templates/source-packet.md` or embed its fields in the assessment packet. Separate raw source/seed, linked sources, retrieval limits, synthesis, and uncertainty.
4. **Build the research map.** For Deep Research Assessment, intentionally choose lanes: local codebase/source-of-truth, primary docs/specs, GitHub alternatives/prior art, issues/forums/practitioner discussion, papers/blogs where relevant, and contradiction search. State coverage claimed and not claimed; never imply exhaustive research when only a slice was inspected.
5. **Check project context.** Inspect the relevant project/source-of-truth paths/cards/docs enough to avoid stale or duplicate recommendations. Use local adapter references when present (for example Type0/Gaia/Soho/Hermes on Rob's machine), but do not force unrelated local projects into portable assessments. Record context freshness and gaps.
6. **Extract ideas and claims.** Distinguish user/source/author claims from your inferences. Record evidence quality, contradiction risk, local fit, and what is actually actionable.
7. **Compare alternatives.** For implementation questions and architecture/tool ideas, produce an alternatives/prior-art matrix. Include the "do nothing / note / eval-only / improve context or skill" option alongside new machinery.
8. **Run benefit >> cost.** Ask what to delete or simplify first. Prefer notes, eval seeds, or tool/context fixes over new machinery unless benefit is clearly much greater than hidden cost.
9. **Run Agent Advocate when agent systems are involved.** Ask the human counterfactual: would a competent human with the same context/tools have made the error? If not, identify the missing context, source authority, tool feedback, memory, affordance, or approval boundary.
10. **Decide.** Choose Adopt now, Watch, Archive, Reject, Needs more research, or Convert to eval only.
11. **Set approval boundary.** State `Implementation before approval: no`. If approved, provide a compact `$ubergoal`/`$uberplan` handoff and evidence plan.
12. **Leave a learning trail.** For accepted/rejected high-signal assessments, note how outcome should feed `$uberskillevolver` or Hermes later.

## Deep Research Assessment mode

Use this mode when the user says "boil the ocean," asks for deep research, requests alternatives or state-of-the-art, gives only a scrap of an idea, or asks an implementation/architecture question before planning. The job is not to gather every possible source; it is to make the research boundary honest and broad enough that a later plan is not built on vibes.

Minimum lanes to consider:

- **Seed/source capture** — exact user wording, source URL, linked artifacts, raw media/transcripts, and retrieval limits.
- **Question framing and clarification** — what decision this assessment must support, what would be overreach, and what targeted user feedback would materially improve the research.
- **Local project context** — current codebase, skills, docs, tests, policies, and duplicate/prior attempts.
- **Primary docs/specs** — official docs and source-of-truth references such as OpenClaw docs when relevant.
- **Alternatives/prior art** — GitHub repos, libraries, patterns, architecture options, and why they do or do not transfer.
- **Practitioner evidence** — issues, discussions, forums, postmortems, or threads that reveal real pain and edge cases.
- **Contradiction search** — evidence the idea is stale, solved, unsafe, too expensive, or better handled by deletion/simplification.
- **Adoption fit** — whether the output should be a memory note, watch item, eval seed, rejected idea, or `$ubergoal`/`$uberplan` handoff.

Stop research when additional sources are unlikely to change the recommendation, the coverage gap itself is the recommendation, or approval is needed for paid/private/side-effecting access.

## Plan Artifact Assessment mode

Use this mode when the user asks `uberassess` to assess a plan, or when `uberplan` needs a review of a draft plan before hardening or implementation. Treat the plan as the source artifact: assess whether it matches the user's intent, asks the right clarifying questions, has enough research coverage, names assumptions and gaps honestly, maps risks to evidence, and deserves adoption, revision, or rejection.

A plan assessment should usually answer:

- **Intent fit** — does the plan solve the user's actual problem, or did it drift into a nearby process?
- **Clarification need** — what one to three questions would materially improve the plan before broad work?
- **Research sufficiency** — does the plan need source/code/docs/forum/GitHub research before implementation?
- **Alternatives and deletion** — what simpler/no-build/eval-only route should be considered?
- **Evidence and adoption** — what proof is required before the plan can move to implementation?
- **Revision decision** — approve as-is, revise then proceed, run deeper assessment, convert to eval/watch, or reject.

## Output contract

For Tier 1+, produce an assessment packet with:

- source URL/type and raw capture status
- assessment mode, research question, and clarification checkpoint
- for plan artifacts: intent fit, assumptions, evidence gaps, and revision decision
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

## Optional Claude adversary

Use this only when the user explicitly asks for Claude review, e.g. `with Claude`, `Claude review`, `Claude debate`, or `Claude for 2 rounds`. Do not invoke Claude from task similarity or ordinary `uberassess` use. Codex remains assessment owner and reconciler; Claude is an adversarial reviewer, not a co-author, final authority, or acceptance substitute. If available, read `../references/claude-adversary.md`; keep the essentials here because references may not auto-load.

Default to one Claude challenge round; run two or three only when requested or when material unresolved risk remains. Each Claude challenge must name a claim, causal layer, why it matters, falsifying/satisfying evidence, and minimum impact threshold. If more than one challenge is raised, the first two challenges must use distinct causal layers; a single-challenge round must say why only one challenge is material. Codex reconciliation must classify each challenge as `Accepted`, `Risk added`, `Rejected`, `Uncertain`, or `No material impact`; `No material impact` is non-evidence: it proves a review ran, not that the artifact is acceptable. Bind the ledger to the artifact version/section reviewed.

For `uberassess`, ask exactly:

1. **Source-lane sufficiency.** Causal layer: source authority. Did assessment consult the relevant source lane, or stop at the first confirming source? Evidence: source map plus coverage gap. Minimum impact: inspect the missing lane or limit the claim.
2. **Actionability boundary.** Causal layer: ownership/approval. Is the recommendation directly actionable by the agent, or does it require human escalation? Evidence: next action plus owner. Minimum impact: change decision to watch/archive/escalate if not actionable.
3. **90-day falsifier.** Causal layer: freshness. What would change this recommendation in 90 days? Evidence: named trigger/source. Minimum impact: add watch trigger or reduce confidence.

## Helpful resources

- `templates/assessment-packet.md` — canonical recommendation packet.
- `templates/source-packet.md` — source capture subtemplate.
- `templates/project-context-card.md` — lightweight project context card.
- `references/source-resolvers.md` — source-type handling and limitations.
- `references/project-routing.md` — routing destinations and non-goals.
- `references/hermes-and-approval.md` — Hermes/read-only and approval policy.
- `scripts/validate_assessment_packet.py` — packet validator.
- `evals/golden_skill_invocations.json` — trigger/non-trigger examples for routing changes; load only when tuning assessment triggers.
