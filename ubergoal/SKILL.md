---
name: ubergoal
description: "Use when coding or agentic-system work runs as a goal/objective; needs a long plan, goal ledger, multi-agent session, 100%-confidence strategy check, final completion orchestration, or the former monolithic UberGoal workflow; or asks which Uber subskill to use. Binds plan authority and routes proof to UberAccept."
---

# Ubergoal

## Core rule

`ubergoal` is the thin lifecycle wrapper and goal owner. When invoked, create or bind
the goal, classify risk, bind `$uberplan` or a Tier 0/1 micro-intent by
path/revision, execute only that authority, then send diff/evidence to
`$uberaccept`. Benefit >> cost.

## Routing

| Need | Route |
|---|---|
| Goal/objective launch | platform goal primitive; `references/goal-objective.md`; validate with `scripts/validate_goal_objective.py --target-chars 3400 --strict-target` |
| Tier 0/1 plan | `${UBER_GUIDE_ROOT:-~/repos/agentic-architecture-guide}/docs/coding-agent-work-contract.md` |
| misunderstanding-prevention | `$uberplan` Task Understanding Review |
| Rigorous plan, code reading, confidence, user expectation / surprise assessment | `$uberplan` |
| Everyday defect; repeated incident | `../references/debug-loop.md`; repeated -> `$uberrca` |
| Architecture-shaped failure | route to `$uberarchitect` before `$uberplan` |
| policy-adherence / final proof | `$uberaccept` |
| Complexity/dead code | `$ubersimplify` |
| Source or artifact adoption research | `$uberassess` |
| Post-run learning | `$uberskillevolver` |
| Dispatch or runtime states | `../references/dispatch-and-sessions.md`; `../references/operational-states.md` |
| Refactor campaign / `ubercampaign` | `references/refactor-campaign-profile.md`; `references/campaign-profile.md` |

For material unexpected test failures, stop before five consecutive failures,
run `$uberrca`, revise through `$uberplan`, and merge any changed scope. For
Recurring loop mode: set `loop_mode`, read `../references/loop-engineering.md`,
and do not create `uberloop`. Use `templates/uber-run-receipt.md` only when a
durable receipt is activated.

## Approved-plan execution boundary

Before editing, record plan identity, scope, non-goals, criteria, proof, and
surfaces. Read sources named by operator/plan, then owner, caller/consumer, and
focused proof. Read any stated conflict/evidence artifact; contradiction
requires replanning.

- Execute planned work, repository-mandatory gates, and evidence-activated
  safety protections.
- `fix_within_scope` permits only a bounded correction already authorized.
- `replan` applies when evidence changes the implementation contract without
  changing operator authority.
- `user_decision` applies before changing operator-owned product scope,
  ownership, architecture/dependency commitments, public behavior, acceptance,
  or external-action authority; internal contract changes stay `replan`.
- Planning never authorizes an external action. Preserve exact target,
  authorization, idempotency, rollback, receipt, and authoritative readback.
- Do not add generic docs, refactors, broad tests/evals, reviewers, subagents,
  or lifecycle artifacts unless the plan, repository contract, or observed risk
  activates them.

After each step, record proof and the next state: `continue`,
`fix_within_scope`, `ready_for_acceptance`, `replan`, `user_decision`, or
`blocked`. Use `continue` only when the next approved step is runnable and no
required gate is missing. Missing operator authority is `user_decision`;
missing or unavailable review, rollback, canary, runtime readback, or another
proof gate is `blocked`. Return the literal state; do not rename either as
paused or a generic blocker. Name the barrier and list safe next actions.

`ubergoal` never issues `accepted`, `complete`, or `SHIP`. No reviewer verdict
is UberAccept. After plan, proof, and tier review pass, return
`ready_for_acceptance` and invoke `$uberaccept`.

## Review ladder

| Tier | Work class | Required review |
|---|---|---|
| 0 | typo/cosmetic only — nothing that fixes observed misbehavior | none; commit carries a `tier0:` trailer |
| 1 | contained single-surface change, clear tests | one exact-diff review pass by a capable lane, including a one-line scope echo against the operator-original ask |
| 2 | cross-repo doctrine/pointer edits; behavior surfaces (prompts/skills/evals); medium-risk code | exact-diff review + independent adversarial lane (different vendor or fresh context) + scope-fidelity verdict |
| 3 | production/runtime services; live-injected context surfaces; provider routing; security/data-subject surfaces; major refactor / mass deletion | full 4-phase ladder (plan review, exact-diff, adversarial, acceptance) using fresh independent reviewer contexts at the highest model and effort allowed by active project policy + review-board lanes |

Tier 2 uses one independent risk-specific lane. Tier 3 keeps review-board lanes; risk
activates specialists. Effort scales with tier; active project policy binds
model and effort. Repository ladder is canonical; if uncertain, take the
higher tier.

## Micro-intent fast path

For Tier 0/1 low-risk work without runtime/provider/security/data-subject or
cross-boundary ambiguity, use 2-3 sentences of scope / intent, criteria,
non-goals, and verification. Include
`failure_case_id | case_updated | not_applicable_with_reason`.

## Scope fidelity and completion

Preserve the operator original instruction, agent-interpreted scope,
proposed narrowed scope, explicit deferrals/non-goals, approval evidence, and Scope
fidelity verdict in the plan/micro-intent. Use a separate ledger only for
requested, long-running, resumable, multi-owner, or handoff work.

Do not call `update_goal(status="complete")` until `$uberaccept` returns
`accepted`, each touched repo is committed/reverted/approved-dirty, and the
handoff reports git state and gaps. Other states remain non-complete. File
failure intake only when the terminal state requires it.

## Optional Claude adversary

Use only when the operator explicitly requests Claude by name. A generic cross-model request does not authorize selecting Claude. Do not invoke Claude or alternate reviewer from task similarity. Contract (subprocess reference-following proven):
`../references/claude-adversary.md`.

Ask: **Load-bearing goal?** **Skip test.** **Testable decomposition.**
