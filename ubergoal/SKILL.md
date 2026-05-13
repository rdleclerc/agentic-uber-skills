---
name: ubergoal
description: "Use when an agent needs the goal-owning lifecycle wrapper for substantial coding or agentic-system work: create or bind a Codex/platform goal by default when available, classify risk, route to uberplan for rigorous planning, run Tier 2+ specialist review-board agents when available, coordinate execution at the right tier, route to uberaccept for final proof, and route to uberskillevolver for post-run learning. Trigger for explicit goal/objective work, long plans, goal ledgers, multi-agent coding sessions, agentic-system changes, rigorous-multiagent-coding, the former monolithic ubergoal workflow, 100% confident strategy checks, final completion orchestration, or deciding which Uber subskill to use."
---

# Ubergoal

## Core rule

`ubergoal` is the **thin lifecycle wrapper**, goal owner, and bounded review-board coordinator for the Uber skill family. In runtimes with a platform goal object, explicit `ubergoal` use means create or bind that goal first, then route to focused subskills and specialist agents instead of carrying all planning and acceptance machinery itself.

Use the lightest tier that makes the work safe. Treat process as cost. Add agents, review lanes, validators, evals, templates, or subskills only when benefit is **clearly much greater than** total downstream cost.

## Routing table

| Need | Use |
|---|---|
| Rigorous planning, review-board lanes, codebase exploration, confidence gate | `$uberplan` |
| Implementation/execution coordination | main coding agent orchestrates; Tier 2+ uses bounded specialist review-board subagents when available |
| Final acceptance, evidence audit, architecture drift, dead-code/test/eval proof | `$uberaccept` |
| Complexity/modularity/dead-code simplification campaign with timestamped trail | `$ubersimplify` |
| Assess source/research signal/internal artifact before adoption | `$uberassess` |
| Post-run learning for skills/prompts/workflows/agentic systems | `$uberskillevolver` |
| Codex/platform goal ownership, compact objective, goal ledger | `ubergoal` resources |

Deferred until real usage proves benefit >> cost: `ubercode`, `ubergit`, `ubereval`, `uberui`, and standalone specialist-lane skills. Use lanes inside `uberplan`/`uberaccept` first.


## Coding-agent work contract

For Tier 1+ coding, prompt, skill, workflow, or agentic-system implementation work, use the generalized Coding Agent Work Contract before editing unless the task is tiny and deterministic:

- Guide: `/Users/claw1/agentic-architecture-guide/docs/coding-agent-work-contract.md`
- Template: `/Users/claw1/agentic-architecture-guide/.agentic/coding_agent_work_contract_template.md`

The work contract is the lightweight task-start artifact for objective, scope, orientation evidence, plan, evidence matrix, stop conditions, and learning trail. It should stay compact; do not create a second bureaucracy around it.

Artifact precedence:

- **Tier 0:** concise inline note only.
- **Tier 1:** the Coding Agent Work Contract is the plan artifact unless a concrete risk requires a fuller `uberplan` contract.
- **Tier 2/3:** `uberplan` may extend the Coding Agent Work Contract, but should not create a disconnected second plan with duplicate objective/scope/evidence sections.

## Lifecycle

1. **Classify tier.** Use Tier 0/1/2/3 and choose the lowest safe tier.
2. **Plan.** For Tier 1, use the Coding Agent Work Contract as the compact plan unless risk demands more. For Tier 2/3, invoke or follow `$uberplan` and embed/extend the work contract. For Tier 0, use a concise plan/test note.
3. **Create or bind the goal.** In Codex or any runtime with a platform goal object, explicit `ubergoal` use launches a compact goal by default for Tier 1+ work and for any task where the user explicitly names `ubergoal`. If a goal already exists, bind the work to it instead of creating a duplicate. Skip goal creation only when the user explicitly asks for no goal/lightweight mode, the runtime has no goal facility, or the task is not actually being handled through `ubergoal`.
4. **Run the review board and execute.** Keep the main agent as orchestrator. Explicit `ubergoal` use authorizes bounded specialist review-board agents for Tier 2+ work unless the user says no agents/lightweight mode. Use implementation workers only when write scopes are disjoint.
5. **Ledger.** For long work, maintain `templates/goal-ledger.md`.
6. **Assess sources/artifacts when needed.** Route source-to-recommendation due diligence to `$uberassess`; do not let assessment become implementation before approval.
7. **Simplify when needed.** Invoke or follow `$ubersimplify` for opt-in complexity/dead-code/modularity campaigns; default to Audit mode unless patching is explicitly authorized.
8. **Accept.** Invoke or follow `$uberaccept` before claiming completion or calling `update_goal(status="complete")`.
9. **Learn.** For Tier 2/3 skill, prompt, workflow, multi-agent protocol, or agentic-system changes, invoke `$uberskillevolver` after acceptance.

## Tier selection

| Tier | Use for | Wrapper behavior |
|---|---|---|
| Tier 0 | Small isolated deterministic edits | if `ubergoal` was explicitly invoked in a goal-capable runtime, create/bind the smallest goal; otherwise no goal, no subagents, short plan/tests |
| Tier 1 | Long but contained work | create/bind goal, `$uberplan` light plan, optional ledger, `$uberaccept` final proof |
| Tier 2 | Medium/high-risk work where a solo coding agent is likely to miss context, overfit a patch, mishandle dirty state, or misjudge acceptance | create/bind goal, `$uberplan` audited plan, 2-3 specialist review-board agents/lenses by default, evidence rubric, `$uberaccept`, optional learning loop |
| Tier 3 | Cross-repo, agentic-system, production/runtime, major refactor/deletion, prompt/skill/eval, concurrency/security, complex UI | create/bind goal, full `$uberplan`, batched review board plus disjoint implementation workers when useful, carefully bounded execution/audits, `$uberaccept`, `$uberskillevolver` if skill/workflow/agentic lessons exist |

If uncertain, choose the lower tier unless a concrete risk requires escalation.

## Implementation effort recommendation

When returning a plan for implementation, recommend a model reasoning-effort level. This is a recommendation, not a permission to expand scope:

| Effort | Use when | Avoid when |
|---|---|---|
| `medium` | Tier 0/1 work; localized deterministic patches; clear tests; low ambiguity; no live side effects | user is asking for architecture reset, agentic-system changes, or unresolved root-cause analysis |
| `high` | Tier 1/2 work with judgment, repo navigation, user-visible behavior, non-trivial tests/evals, or moderate uncertainty | the task is tiny, deterministic, or the extra reasoning would mostly add process |
| `xhigh` | Tier 3 work; cross-repo or runtime-impacting changes; prompt/skill/eval changes; major refactor/deletion; concurrency/security/privacy; repeated failures where hidden assumptions must be challenged | the work can be reduced to a smaller `medium`/`high` slice that preserves a working product spine |

Before recommending `xhigh`, run the deletion-first pass: can the task be split so the next implementation slice stays `high` or `medium` while preserving safety and visible progress? If yes, recommend the smaller slice instead of escalating the whole plan.

## Goal ownership

`ubergoal` is a superset of the platform goal primitive. The goal object is the durable execution spine; the Uber wrapper adds tiering, routing, subskills, agents, acceptance, and learning.

When running in Codex:

- If no goal exists and the user explicitly invoked `ubergoal`, call `create_goal` before substantial planning or execution.
- If a goal already exists, keep using it and update the goal ledger/status around it rather than creating a duplicate.
- If the user explicitly asks for no goal/lightweight mode, record that as the reason for skipping goal creation.
- If the runtime lacks a goal facility, continue with a local goal ledger and say that no platform goal object is available.

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

### Runtime thread caps

Treat active subagent/session limits as a platform policy constraint, not an agent judgment call. In Codex, assume a maximum of 4 active spawned subagents at once unless the platform explicitly reports a higher cap in the current run.

For Tier 3 or other wide review-board work:

- batch lanes in priority order instead of trying to spawn the whole board at once
- close completed agents before opening queued lanes
- if spawning fails because of a thread/session limit, record the cap hit in the ledger and rerun that lane later or perform it locally
- never count a failed spawn, unavailable lane, or queued lane as completed review evidence
- keep the main agent responsible for integration and the immediate critical path

When implementation begins:

- Tier 2 is valuable because it changes the decision shape: the orchestrator does not just think harder; it receives independent feedback from specialist context lenses.
- For Tier 2, launch 2-3 bounded review lanes when the runtime supports subagents. Default lanes are Codebase/State Scout, Architecture/Contract Steward, and Quality/Eval/Hygiene Auditor; choose fewer only when the risk is clearly narrower.
- Review-board agents inspect, challenge, and recommend. They do not mutate files unless explicitly assigned a disjoint worker write scope.
- If subagents are unavailable or the thread cap is hit, run the same specialist lenses sequentially in the main thread and report the degraded execution mode.
- keep write sets disjoint if using workers
- do not delegate the immediate critical-path blocker
- require evidence-backed outputs, not generic approval
- serialize overlapping work
- update `templates/goal-ledger.md` after major checkpoints
- stop and ask before destructive/external side effects unless already approved

## Completion rule

Do not call `update_goal(status="complete")` until `$uberaccept` says the objective is achieved, no required work remains, and every touched repo is locally committed, reverted, intentionally stashed, or explicitly user-approved as uncommitted. Final handoff must include `git status --short --branch` for each touched repo.

For “100% confident” prompts, use the scoped meaning: 100% confident within the stated scope after trying to disprove the plan/work and finding no material unresolved blocker.

## Helpful resources

- `templates/goal-ledger.md` — compact long-running goal state.
- `references/goal-objective.md` — compact goal objective guidance.
- `scripts/validate_goal_objective.py` — objective length validator.
