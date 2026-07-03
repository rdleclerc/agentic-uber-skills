---
name: ubergoal
description: "Use when an agent needs the goal-owning lifecycle wrapper for substantial coding or agentic-system work: create or bind a Codex/platform goal by default when available, classify risk, route to uberplan for rigorous planning, run Tier 2+ specialist review-board agents when available, coordinate execution at the right tier, route to uberaccept for final proof, and route to uberskillevolver for post-run learning. Trigger for explicit goal/objective work, long plans, goal ledgers, multi-agent coding sessions, agentic-system changes, rigorous-multiagent-coding, the former monolithic ubergoal workflow, 100% confident strategy checks, final completion orchestration, or deciding which Uber subskill to use."
---

# Ubergoal

## Core Rule

`ubergoal` is the thin lifecycle wrapper, goal owner, and bounded review-board coordinator. When invoked, create/bind the platform goal, classify risk, then route. Loop: observe, choose one action, act, verify evidence, record `proved`/`weak`/`missing`/`contradicted`, and continue only if the next action changes a decision or closes a gap. Benefit >> cost.

## Routing Table

| Need | Use |
|---|---|
| Goal/objective launch | platform goal primitive; `references/goal-objective.md`; validate with `scripts/validate_goal_objective.py --target-chars 3400 --strict-target` |
| Coding Agent Work Contract | guide `${UBER_GUIDE_ROOT:-~/repos/agentic-architecture-guide}/docs/coding-agent-work-contract.md`; template `${UBER_GUIDE_ROOT:-~/repos/agentic-architecture-guide}/.agentic/coding_agent_work_contract_template.md` |
| misunderstanding-prevention review | `$uberplan` Task Understanding Review |
| Rigorous planning, review-board lanes, codebase exploration, confidence gate, user expectation / surprise assessment | `$uberplan` |
| Architecture-shaped failures: concurrency, queues, workers, orchestration, backpressure, repeated timeouts, symptom patches | route to `$uberarchitect` before `$uberplan` |
| Execution coordination | main agent; Tier 2+ uses bounded specialist review-board agents/lenses |
| Dispatch / parallel sessions | `../references/dispatch-and-sessions.md` |
| Everyday defect / bug fix | `../references/debug-loop.md`; repeats or incidents -> `$uberrca` |
| Final acceptance, policy-adherence, architecture drift, dead-code/test/eval proof, surprises | `$uberaccept` |
| Complexity/modularity/dead-code campaign | `$ubersimplify` |
| Source/research/internal-artifact assessment before adoption | `$uberassess` |
| Post-run learning for skills/prompts/workflows/agentic systems | `$uberskillevolver` |
| Reword a fingerprinted rule | update `references/drift-fingerprints.toml` same commit; drift check gates |
| Repeated or material unexpected test failures | stop before five consecutive failures; `$uberrca`; revise via `$uberplan`; append/merge child scope change |
| Refactor campaign / HOT-file audit | `references/refactor-campaign-profile.md` |
| `ubercampaign`, product campaign, multi-feature/feature-list/plan-tree campaign | `references/campaign-profile.md` |
| Tier 3 agentic/runtime/production-replacement expensive proof, burn-in, soak, canary expansion, final proof | `$uberplan` with `templates/tier3-expensive-proof-plan-tree.md` validator |
| Recurring loop mode: watch, monitor, rerun, keep fixing, scheduled, unattended | mark `loop_mode`; read `../references/loop-engineering.md`; contract `$uberplan`; acceptance `$uberaccept`; lessons `$uberskillevolver`; do not create `uberloop` |
| Runtime topology, parent/child terminal states, active/hard blockers | `../references/operational-states.md` |

## Review Ladder

| Tier | Work class | Required review |
|---|---|---|
| 0 | typo/cosmetic only — nothing that fixes observed misbehavior | none; commit carries a `tier0:` trailer |
| 1 | contained single-surface change, clear tests | one exact-diff review pass by a capable lane, including a one-line scope echo against the operator-original ask |
| 2 | cross-repo doctrine/pointer edits; behavior surfaces (prompts/skills/evals); medium-risk code | exact-diff review + independent adversarial lane (different vendor or fresh context) + scope-fidelity verdict |
| 3 | production/runtime services; live-injected context surfaces; provider routing; security/data-subject surfaces; major refactor / mass deletion | full 4-phase ladder (plan review, exact-diff, adversarial, acceptance) on the highest-capability Claude lane + review-board lanes |

Riders + audit rule: spine §Review ladder is canonical; receipts record tier + one-line justification; reviewer's first check is tier correctness. If uncertain, take the higher tier. Effort scales with tier; xhigh only where a smaller slice cannot preserve safety.


## Micro-intent fast path

For Tier 0/1 low-risk work, use one micro-intent artifact when no runtime/provider/security/data-subject surface or cross-boundary ambiguity is present: 2-3 sentences of scope / intent, acceptance criteria, explicit out-of-scope note, and verification evidence. Escalate ambiguity, agentic/runtime risk, irreversible side effects, or many criteria to `$uberplan`. Micro-intent artifacts carry `failure_case_id | case_updated | not_applicable_with_reason`.

## Scope fidelity gate

For Tier 1+ or explicit `ubergoal`, create/update `coordination/<task-slug>/scope.md` from `templates/scope.md`. Preserve operator original instruction, agent-interpreted scope, proposed narrowed scope, explicit deferrals/non-goals, approval evidence, constraints, and dated changes.

## Completion Rule

Do not call `update_goal(status="complete")` until `$uberaccept` says done, failure intake is filed, every touched repo is committed/reverted/approved-dirty, and final handoff includes git status, Skills invoked summary, receipt path, and unresolved gaps.

## Optional Claude adversary

Use only on explicit Claude review or cross-model review. Do not invoke Claude or alternate reviewer from task similarity. Contract: references/claude-adversary.md (`../references/claude-adversary.md`; subprocess reference-following proven — `coordination/process-rearchitecture-202607/wave2-v3-probe.md`).

For `ubergoal`, ask exactly:

1. **Load-bearing goal?** Is this goal actually load-bearing, or a routing artifact?
2. **Skip test.** What is lost if we skip the goal wrapper and execute directly?
3. **Testable decomposition.** Does this decompose into three or fewer testable sub-outcomes?

## Helpful Resources

- `templates/uber-run-receipt.md`
- `templates/scope.md`
- `references/goal-objective.md`
- `references/refactor-campaign-profile.md`, `references/campaign-profile.md`
- `../references/operational-states.md`, `../references/loop-engineering.md`, `../references/claude-adversary.md`
