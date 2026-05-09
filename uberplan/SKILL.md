---
name: uberplan
description: Do not auto-trigger from task similarity. Use only when explicitly named by the user or routed by ubergoal. Plans substantial coding, refactoring, UI, prompt/skill/workflow, or agentic-system work with the smallest safe planning artifact, review lanes, topology seams, and confidence gates.
---

# Uberplan

## Core rule

Create the smallest plan that makes the work safe. Treat planning itself as a cost: add review lanes, subagents, templates, and evals only when the benefit is **clearly much greater than** total downstream cost.

`uberplan` owns the planning phase of the Uber skill family. It does not execute the patch and does not accept the finished work. Use `uberaccept` for final proof and `uberskillevolver` for post-run learning.

Avoid duplicate planning artifacts. If a Coding Agent Work Contract already captures objective, scope, orientation evidence, plan, evidence targets, stop conditions, and gaps, use it as the Tier 1 plan artifact. For Tier 2/3, extend or embed that contract in the plan contract rather than creating an unrelated second plan.

## Basic Spine First gate

For product/rewrite/agentic-system work, planning must first name the minimum user-visible product spine, the single canonical command or live-safe check that proves it, and the current result: `pass`, `fail`, or `not available`. If the result is `fail` or `not available`, the plan may only fix/create that spine check or explicitly label the work a non-readiness spike. Do not add architecture, abstractions, agents, contracts, routers, monitors, or eval frameworks until the spine is green or the user accepts the spike boundary.

For Type0, default spine: real feed/tip/wire input → normalized signal → admission decision → lane/story assignment → story processing → fact-check/publish/reject guard → traceable result. The First-Principles Simplifier has veto authority here: a core spine gap is a blocker, not an essay-length residual risk.

## Output contract

Return or create a plan contract with:

1. tier and why it is not overkill
2. clarified objective, scope, assumptions, and non-goals
3. affected repos/files and protected-file constraints
4. codebase exploration / pheromone trails when context risk is material
5. architecture options when the design is non-obvious
6. activated/skipped review lanes and blocker authority
7. deterministic harness responsibilities vs adaptive model policy
8. source authority, side-effect, approval, rollback, and adoption-state policy when relevant
9. repository topology/package-seam plan for any new or moved code files, including the executable gate that will catch drift
10. Basic Spine First statement for product/rewrite/agentic-system work, or why not applicable
11. risk-to-evidence map and acceptance rubric
12. confidence verdict after trying to falsify the plan

Use `templates/plan-contract.md` for durable plans and `templates/confidence-gate.md` for the adversarial pre-launch check.

## Tier selection

| Tier | Use for | Planning machinery |
|---|---|---|
| Tier 0 | Small isolated deterministic edits | concise plan/test note only |
| Tier 1 | Long but contained work | plan contract + inline loophole/simplifier check |
| Tier 2 | Medium/high-risk work | Architecture Steward plus the single most relevant extra lane |
| Tier 3 | Cross-repo, agentic-system, production/runtime, major refactor/deletion, prompt/skill/eval, concurrency/security, or complex UI work | full planning review board, explicit evidence rubric, optional subagents only when authorized |

If uncertain, choose the lower tier unless a concrete risk requires escalation.

## Planning review lanes

For Tier 2/3, choose lanes by risk, not by ceremony:

- **Architecture Steward** — blocks material architecture, harness/policy, source authority, durable execution, adoption, budget, or eval gaps.
- **Agent Advocate / Agent Failure RCA** — required for multi-agent work, agent errors, prompt/tool/context/memory changes, or symptom-patch risk; answers the human counterfactual.
- **Loophole Hunter / Red Team** — finds hidden assumptions, exploit paths, missing tests, unsafe side effects, race/idempotency gaps.
- **First-Principles Simplifier / Complexity Auditor** — aggressively deletes, simplifies, or substitutes; blocks complexity without benefit >> cost.
- **Codebase Scout / Cartographer** — maps unfamiliar code, extension points, tests, protected files, and existing patterns.
- **OpenClaw / Platform Steward** — required for OpenClaw, Type0, runtime, gateway, orchestration, sessions, skills, or machine ops.
- **Quality/Eval Strategist** — maps tests/evals/audits to actual risks.
- **Cost/Risk Governor** — de-escalates overbuilt plans and adds stop conditions.

Use `templates/planning-review-board.md` for board synthesis.

## Parallel exploration and pheromone trails

If the repo is complex or unfamiliar and subagents are explicitly authorized, split exploration into non-overlapping slices. Each scout must leave a reusable trail: key files with line references, discovered invariants, commands/tests, unknowns, false leads, and recommended next angles. Use `templates/exploration-trail.md`.

Do not spawn multiple agents over the same context. Parallelism pays when it reduces context overload, not when it creates shallow duplicate summaries.

### Runtime thread caps

Treat subagent/session limits as a hard platform policy. In Codex, assume at most 4 active spawned subagents at once unless the platform explicitly reports a higher cap in the current run.

When a planning board has more useful lanes than the cap allows:

- batch lanes in priority order and run the highest-risk lanes first
- wait for completions and close completed agents before spawning queued lanes
- record queued lanes, skipped lanes, and cap hits in the plan or goal ledger
- if a spawn fails with a thread/session-limit error, rerun that lane later or perform it locally
- never count a failed spawn, unavailable lane, or queued lane as completed review evidence

## Repository topology gate

For any task that adds, moves, or meaningfully reorganizes code files, the plan must name the intended package/module destination and the repo-local guard that enforces it (for example `tests/test_package_topology.py`, an import-boundary test, or a dependency-map check). If no such guard exists and the task is non-trivial, add the smallest useful guard before or with the feature/refactor. Do not rely on prose-only hierarchy guidance.

## First-principles simplification

Before hardening the plan, ask:

- What requirement, artifact, abstraction, process, or agent can be deleted?
- Can the outcome be achieved by removing a moving part?
- Is benefit **clearly much greater than** implementation, maintenance, debugging, context, coordination, eval, latency, rollback, and operator-attention cost?
- What first-principles alternative changes the material/tool/architecture instead of optimizing the proposed solution locally?
- What direct experiment could disprove an expensive assumption?

Use `templates/first-principles-simplifier-report.md` when the simplification pass must be durable.

## Agent Advocate / failure RCA

For agentic systems or fixes to agent mistakes, ask what the agent actually experienced. Inspect or request traces, prompts, loaded context, tool outputs/errors, state, memory retrieval, source conflicts, handoffs, feedback, retries, stop conditions, and authority boundaries.

Run the human counterfactual: would a competent human with normal context/tools have made this error? If not, fix the missing context, affordance, feedback, source authority, memory, handoff, approval boundary, or deterministic guard. Use `templates/agent-failure-rca.md`.

## Confidence gate

Before implementation or a goal launch, falsify the plan. Do not say “100% confident” if a material blocker remains. Required verdict:

```text
Confidence verdict:
- 100% confident within scope? yes/no
- Scope:
- Material blockers:
- Non-blocking residual risks:
- Required revisions:
- Evidence required before completion:
```

## Helpful resources

- `templates/plan-contract.md` — full plan contract.
- `templates/confidence-gate.md` — adversarial pre-launch confidence check.
- `templates/planning-review-board.md` — lane synthesis.
- `templates/exploration-trail.md` — scout handoff trail.
- `templates/agent-failure-rca.md` — Agent Advocate/human-counterfactual RCA.
- `templates/architecture-steward-report.md` — planning architecture review.
- `templates/first-principles-simplifier-report.md` — deletion/simplification review.
- `templates/agent-brief.md` — bounded worker/auditor handoff.
- `references/tiering-and-rubric.md` — tier/rubric details.
- `references/agentic-architecture-checklist.md` — architecture checklist.
- `scripts/validate_plan_contract.py` — deterministic plan sanity checks.
