---
name: uberplan
description: Do not auto-trigger from task similarity. Use only when explicitly named by the user or routed by ubergoal. Plans substantial coding, refactoring, UI, prompt/skill/workflow, or agentic-system work as a long-running goal plan with thread highlights, a durable .md file, proof ladders, review lanes, topology seams, and confidence gates.
---

# Uberplan

## Core rule

Create the smallest plan that makes the work safe. Treat planning itself as a cost: add review lanes, subagents, templates, and evals only when the benefit is **clearly much greater than** total downstream cost.

`uberplan` is not an `uberslice`. Its default output is a long-running goal execution plan with checkpoints, phases, and acceptance gates. Do not collapse substantial work into a default 20-minute slice unless the user explicitly asks for a slice; bounded work packages should serve the larger goal, not replace it.

`uberplan` owns the planning phase of the Uber skill family. It does not execute the patch and does not accept the finished work. Use `uberaccept` for final proof and `uberskillevolver` for post-run learning.

Avoid duplicate planning artifacts. If a Coding Agent Work Contract already captures objective, scope, orientation evidence, plan, evidence targets, stop conditions, and gaps, use it as the Tier 1 plan artifact. For Tier 2/3, extend or embed that contract in the plan contract rather than creating an unrelated second plan.

## Basic Spine First gate

For product/rewrite/agentic-system work, planning must first name the minimum user-visible product spine, the single canonical command or live-safe check that proves it, and the current result: `pass`, `fail`, or `not available`. If the result is `fail` or `not available`, the plan may only fix/create that spine check or explicitly label the work a non-readiness spike. Do not add architecture, abstractions, agents, contracts, routers, monitors, or eval frameworks until the spine is green or the user accepts the spike boundary.

For Type0, default spine: real feed/tip/wire input → normalized signal → admission decision → lane/story assignment → story processing → fact-check/publish/reject guard → traceable result. The First-Principles Simplifier has veto authority here: a core spine gap is a blocker, not an essay-length residual risk.

## Agent execution proof ladder

For OpenClaw or agentic-system plans, make capability proof an explicit strategy, not a final wish. First prove that a Codex subagent with the right skills, tools, source access, and bounded context can execute the activity. If that fails, the plan should improve the skill/tool/context contract before adding orchestration. After the Codex proof works, prove the same activity through OpenClaw or the target runtime. If target-runtime proof fails, iterate the same contracts until parity is reached. Do not call the plan ready until parity has two successful proofs or the missing proof is labeled as a blocker/spike.

## Delivery format

Return both:

- in-thread highlights: objective, user expectation/surprise risks, critical path, top risks, proof gates, next checkpoint, and material blockers
- a durable `.md` plan file path containing the full contract

Before presenting either form, run a deletion-focused over-orchestration review. Hunt for: accidental 20-minute-slice collapse, user expectation mismatches, unnecessary agents/lanes/templates/files, duplicate artifacts, deterministic harness creep, regex/router semantic authority, and places where better skills/tools/context/source authority would beat more process. Revise the plan before showing it.

## Output contract

Return or create a plan contract with:

1. goal execution posture and delivery: long-running goal horizon, checkpoints, `.md` plan path, and thread highlights
2. User expectation / surprise assessment: what the user likely expects from the request and known preferences, what planned choices may surprise them, what assumptions need confirmation, and how the final handoff will prove no material mismatch
3. tier and why it is not overkill
4. clarified objective, scope, assumptions, and non-goals
5. a checkable Product / PRD checklist for Tier 2/3 work, so workers can mark requirements, non-goals, acceptance targets, and deferred items without inventing a second artifact
6. a detailed task map / implementation graph with stable task IDs, dependencies, owners, write scopes, done conditions, evidence, critical path, and a Mermaid diagram for Tier 2/3 work
7. verifiable subgoals with acceptance evidence plus quantitative metrics, scores, or qualitative rubrics; every subgoal must say what proves it is done
8. a parallelization plan that separates parallelizable slices from serial blockers, names disjoint write scopes, and states batching/max-concurrency policy; planning may identify parallel work even when subagents are not authorized
9. a testing adaptation and RCA-driven scope gate: stop before or at five consecutive clear failures of the same test command/failure family, or immediately for a material unexpected failure that invalidates the plan; run RCA; when RCA changes scope, create a focused child/sub-`uberplan` appendix and append or merge it into the parent plan as `scope expansion`, `scope correction`, or `blocker`; then continue under `ubergoal` only after the merged plan names the new hypothesis and evidence gate
10. affected repos/files and protected-file constraints
11. codebase exploration / pheromone trails when context risk is material
12. architecture options when the design is non-obvious
13. activated/skipped review lanes and blocker authority
14. deterministic harness responsibilities vs adaptive model policy
15. for agentic-system plans, a thin harness / fat agent rubric: deterministic harness owns contracts, state, tools, permissions, traces, and evals; agents own ambiguous interpretation, decomposition, recovery, synthesis, and tool choice inside the harness
16. for agentic-system plans, an Agent execution proof ladder: Codex subagent proof, skill/tool/context iteration rule, OpenClaw or target-runtime parity proof, and two successful target-runtime proofs before readiness
17. for agentic-system plans, a source-convention check for approved/local/public Codex and OpenClaude/Claude Code conventions; use conventions, not copied proprietary/leaked code
18. source authority, side-effect, approval, rollback, and adoption-state policy when relevant
19. target architecture/file-tree plan plus repository topology/package-seam plan for any new, moved, or meaningfully reorganized code files, including the executable gate that will catch drift
20. code-health/dead-code tool plan for Tier 2/3 work and for refactors/deletions/new modules, using repo-local tools first and language-appropriate tools such as `vulture`, `ruff`, `pyright`/`mypy`, `knip`, `ts-prune`, `depcheck`, `eslint`, `tsc`, and `grep`/`git grep`; tool findings are candidates, not deletion authority
21. Basic Spine First statement for product/rewrite/agentic-system work, or why not applicable
22. risk-to-evidence map and acceptance rubric with testable goals across unit/regression, integration, acceptance, e2e or simulation, and eval/replay evidence; use real bugs/content when available
23. decision/tradeoff/surprise register covering issues, implementation choices, accepted tradeoffs, and anything likely to surprise a future agent or reviewer
24. pre-presentation over-orchestration review that revises the plan before showing it
25. plan acceptance gate before implementation: try to reject the plan against OpenClaw/agentic architecture, thin-harness/fat-agent policy, topology, dead-code, source-authority, and evidence requirements
26. confidence verdict after trying to falsify the plan

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

## Parallel exploration and execution planning

Always map the critical path before suggesting parallel work. If the repo is complex or unfamiliar and subagents are explicitly authorized, split exploration into non-overlapping slices. Each scout must leave a reusable trail: key files with line references, discovered invariants, commands/tests, unknowns, false leads, and recommended next angles. Use `templates/exploration-trail.md`.

Even when subagents are not authorized or available, the plan should still identify which tasks are parallelizable in principle, which tasks are serial blockers, and which write scopes must remain disjoint. This helps future coding agents batch safely without guessing.

Do not spawn multiple agents over the same context. Parallelism pays when it reduces context overload or wall-clock time with disjoint work, not when it creates shallow duplicate summaries.

## RCA-driven scope expansion

Use this when testing exposes a key, unexpected problem that makes the current plan wrong, not merely incomplete. First preserve the failing command/output and run `deep-rca` to name the missing invariant. Then create a focused child/sub-`uberplan` appendix for the RCA result. The parent plan remains the source of truth: append or merge the child plan into the parent task map, evidence gates, risks, and decision register, labeling the change as `scope expansion`, `scope correction`, or `blocker`. Resume only after the parent plan says what changed, which new tasks/evidence were added, and why the added scope is worth its cost.

### Runtime thread caps

Treat subagent/session limits as a hard platform policy. In Codex, assume at most 4 active spawned subagents at once unless the platform explicitly reports a higher cap in the current run.

When a planning board has more useful lanes than the cap allows:

- batch lanes in priority order and run the highest-risk lanes first
- wait for completions and close completed agents before spawning queued lanes
- record queued lanes, skipped lanes, and cap hits in the plan or goal ledger
- if a spawn fails with a thread/session-limit error, rerun that lane later or perform it locally
- never count a failed spawn, unavailable lane, or queued lane as completed review evidence

## Repository topology and file-tree gate

For any task that adds, moves, or meaningfully reorganizes code files, the plan must propose the target file tree before implementation, name the intended package/module destination, separate public seams from private implementation files, state where tests/evals belong, and name the repo-local guard that enforces it (for example `tests/test_package_topology.py`, an import-boundary test, or a dependency-map check). If no such guard exists and the task is non-trivial, add the smallest useful guard before or with the feature/refactor. Do not rely on prose-only hierarchy guidance.

A good plan should make ugly structure hard: no root-level convenience dumps, no random helper piles, no mixed-concern folders, and no orphan generated artifacts in source lanes unless explicitly approved.

## Code-health and dead-code planning

For Tier 2/3 plans, refactors, deletions, new modules, or package moves, name the code-health tools that will be run or explicitly unavailable. Prefer repo-local commands first, then language-appropriate tools:

- Python: `vulture`, `ruff`, `pyright`/`mypy`, `pytest`, plus `grep`/`git grep`/call-site review.
- TypeScript/JavaScript: `knip`, `ts-prune`, `depcheck`, `eslint`, `tsc`, tests, plus route/config/build entrypoint review.
- General: package topology tests, import-boundary/dependency-map checks, generated-artifact audits, secret scans when relevant, and dynamic-reference review for CLIs, framework routes, configs, migrations, prompts, tools, plugins, and external callers.

Dead-code tools produce deletion candidates, not authority. Deletion still needs Chesterton/dynamic-reference/rollback proof and enough tests or characterization coverage for the touched slice.

## Agentic system planning bias

For agentic-system plans, prefer thin harness / fat agent. The harness should be small, deterministic, inspectable, and testable: schemas, tool contracts, state, permissions, budgets, source authority, replay, traces, and evals. The agent should carry the adaptive work: ambiguous intent, context selection, tool choice, task decomposition, plan revision, recovery, synthesis, and judgment.

The plan must actively reject deterministic monolith drift: giant routers, keyword/regex semantic authority, broad blob files, hardcoded example branches, hidden state bags, and tools that secretly absorb agent policy. Prefer reusable skills and tools with encapsulated dependencies. A wrapper tool may call downstream tools, but it must keep its boundary explicit.

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

## Plan acceptance and confidence gates

Before implementation or a goal launch, perform plan acceptance: actively look for OpenClaw/agentic architecture violations, fat deterministic harnesses, hidden policy in tools/routers, missing source authority, weak topology/file-tree structure, unplanned dead-code cleanup, and unreported tradeoffs or surprises. Record issues, implementation choices, and surprising decisions even when accepted.

Then falsify the plan. Do not say “100% confident” if a material blocker remains. Required verdict:

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
