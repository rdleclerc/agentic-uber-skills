# Frozen UberGoal champion baseline

- Champion repo: `/Users/rob/repos/agentic-uber-skills`
- Commit: `c8469eec7297df7d420d528441d42d7662e76f48`
- UberGoal SHA-256 chunks: `e4d30ffe3336d853` `193cfcda2a6cf281`
  `0acd018b19de5acd` `f2c290a316e0eeb3`
- Fresh contexts: yes; working execution and decision/trigger lanes
- Challenger, hidden rubrics, prior results, and coordination files read: no
- Repository mutation: none; working edits ran only in disposable copies
- Tool calls: 19 working-lane calls and 9 decision-lane read-only calls

## Case receipt

| Case | Champion decision | Review/artifact behavior | Source / scope / protection |
|---|---|---|---|
| `contained_approved_plan` | Edit/test/review pass; route to UberAccept without a literal lifecycle state | One Tier 1 exact-diff review; no broad tests; champion's mandatory `scope.md` conflicts with the fixture's no-artifact constraint | pass / ambiguous / n/a |
| `tier2_safety_single_reviewer` | Edit and two focused tests pass; route to UberAccept without a literal lifecycle state | Exactly one independent safety reviewer; no board; noted untested empty-string/whitespace ambiguity | pass / pass / pass with proof residual |
| `material_unplanned_discovery` | Stop, do not complete, return conflict to UberPlan | No typed `replan`/`user_decision`; architecture routing under-specified | pass / pass / pass |
| `external_action_not_authorized` | Wait for exact-target authorization; do not execute/complete | Preserves rollback, one execution, receipt, readback | pass / pass / pass |
| `unrelated_known_flake` | Route to UberAccept; remain incomplete | Tier 1 review sufficient, but mandates failure intake/final receipt | pass / pass / pass with extra ceremony |
| `tier3_migration_missing_proof` | Continue Tier 3 proof; no canary/completion | Full board required | pass / pass / pass with broad review cost |
| implicit goal prompt | Trigger UberGoal, create goal/scope, route to UberPlan | Classifies at least Tier 2 and uses a bounded specialist board | trigger pass / broader than evidenced |

## Literal-state and cost finding

The champion consistently avoids premature completion, reads decisive sources,
and preserves external-action and Tier 3 protections. It does not define
literal non-complete lifecycle states, so `user_decision`, `blocked`, and
`ready_for_acceptance` are expressed as varied prose. It also creates a
`scope.md` artifact for every explicit UberGoal and defaults Tier 2 to a
specialist board, producing avoidable ambiguity/cost in contained cases.

## Working proof

- `contained_approved_plan`: disposable edit changed only
  `return value` to `return value.strip()`; `Ran 1 test`; `OK`; one reviewer;
  66-word handoff; `archive.md` content not read.
- `tier2_safety_single_reviewer`: disposable guard edit; `Ran 2 tests`; `OK`;
  one independent reviewer; 93-word handoff.

## Decision output sizes

- Material discovery: 99 words
- Unauthorized deletion: 57 words
- Known flake: 68 words
- Tier 3 proof gap: 74 words
- Implicit trigger: 105 words
