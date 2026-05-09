---
name: ubergoal
description: "Use when an agent needs a thin lifecycle wrapper for substantial coding or agentic-system work: classify risk, route to uberplan for rigorous planning, optionally launch a compact Codex goal only when explicitly instructed, coordinate execution at the right tier, route to uberaccept for final proof, and route to uberskillevolver for post-run learning. Trigger for long plans, goal launch decisions, goal ledgers, multi-agent coding sessions, agentic-system changes, rigorous-multiagent-coding, the former monolithic ubergoal workflow, 100% confident strategy checks, final completion orchestration, or deciding which Uber subskill to use."
---

# Ubergoal

## Core rule

`ubergoal` is the **thin lifecycle wrapper** for the Uber skill family. It should route to focused subskills instead of carrying all planning and acceptance machinery itself.

Use the lightest tier that makes the work safe. Treat process as cost. Add agents, review lanes, validators, evals, templates, or subskills only when benefit is **clearly much greater than** total downstream cost.

## Routing table

| Need | Use |
|---|---|
| Rigorous planning, review-board lanes, codebase exploration, confidence gate | `$uberplan` |
| Implementation/execution coordination | main coding agent, with subagents only when explicitly authorized |
| Final acceptance, evidence audit, architecture drift, dead-code/test/eval proof | `$uberaccept` |
| Post-run learning for skills/prompts/workflows/agentic systems | `$uberskillevolver` |
| Compact goal objective and goal ledger | `ubergoal` resources |

Deferred until real usage proves benefit >> cost: `ubercode`, `ubergit`, `ubereval`, `uberui`, and standalone specialist-lane skills. Use lanes inside `uberplan`/`uberaccept` first.

## Lifecycle

1. **Classify tier.** Use Tier 0/1/2/3 and choose the lowest safe tier.
2. **Plan.** For Tier 1+, invoke or follow `$uberplan`; for Tier 0, use a concise plan/test note.
3. **Launch goal only if explicit.** Create a platform goal only when the user explicitly says to launch one.
4. **Execute.** Keep the main agent as overseer. Use subagents only when the current user request explicitly authorizes subagents, delegation, or parallel agents.
5. **Ledger.** For long work, maintain `templates/goal-ledger.md`.
6. **Accept.** Invoke or follow `$uberaccept` before claiming completion or calling `update_goal(status="complete")`.
7. **Learn.** For Tier 2/3 skill, prompt, workflow, multi-agent protocol, or agentic-system changes, invoke `$uberskillevolver` after acceptance.

## Tier selection

| Tier | Use for | Wrapper behavior |
|---|---|---|
| Tier 0 | Small isolated deterministic edits | no goal, no subagents, short plan/tests |
| Tier 1 | Long but contained work | `$uberplan` light plan, optional ledger, `$uberaccept` final proof |
| Tier 2 | Medium/high-risk work | `$uberplan` audited plan, evidence rubric, `$uberaccept`, optional learning loop |
| Tier 3 | Cross-repo, agentic-system, production/runtime, major refactor/deletion, prompt/skill/eval, concurrency/security, complex UI | full `$uberplan`, carefully bounded execution/audits, `$uberaccept`, `$uberskillevolver` if skill/workflow/agentic lessons exist |

If uncertain, choose the lower tier unless a concrete risk requires escalation.

## Goal launch

Do not create a platform goal merely because this skill is active. Only launch a goal after explicit user instruction such as “Launch this as a goal.” When running in Codex, this means do not call `create_goal` unless explicitly instructed.

When launching, keep the goal objective compact. Include:

- destination and starting point
- objective/scope and out-of-scope boundaries
- tier and plan artifact path/summary
- preserve/non-regression constraints
- verification gates and required evidence
- allowed subagent/audit shape, if useful
- done/stop conditions and approval boundaries
- success metric

Validate objective text with `scripts/validate_goal_objective.py --target-chars 3400 --strict-target`. Do not set a goal token budget unless the user explicitly gives one.

## Execution coordination

When implementation begins:

- keep write sets disjoint if using workers
- respect the Codex collaboration runtime's active subagent thread cap; assume at most 4 concurrent spawned agents unless the platform explicitly allows more
- for Tier 3 review boards with more than 4 lanes, batch them: spawn the highest-value lanes first, wait for completions, close completed agents, then spawn queued lanes
- if a spawn attempt returns a thread-limit error, do not treat that lane as complete; record the cap hit in the ledger and rerun the lane after closing another agent or perform it locally
- do not delegate the immediate critical-path blocker
- require evidence-backed outputs, not generic approval
- serialize overlapping work
- update `templates/goal-ledger.md` after major checkpoints
- stop and ask before destructive/external side effects unless already approved

## Completion rule

Do not call `update_goal(status="complete")` until `$uberaccept` says the objective is achieved and no required work remains, or the user explicitly accepts named residual gaps.

For “100% confident” prompts, use the scoped meaning: 100% confident within the stated scope after trying to disprove the plan/work and finding no material unresolved blocker.

## Helpful resources

- `templates/goal-ledger.md` — compact long-running goal state.
- `references/goal-objective.md` — compact goal objective guidance.
- `scripts/validate_goal_objective.py` — objective length validator.
