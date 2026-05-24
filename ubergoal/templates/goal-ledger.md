# Goal Ledger

## Goal objective


## Current phase


## Uber run receipt

- Receipt path:
- Validator command:
- Receipt status: not-started | draft | pass | partial | failed

## Completed

-

## Open risks

-

## Cost/complexity watch

- Added machinery still justified? yes/no:
- Simpler path discovered:
- Deferred machinery still deferred? yes/no:

## User expectation / surprise assessment

- User-visible expectation inferred:
- Evidence for expectation:
- Potential surprises or expectation mismatches:
- Ask/flag before proceeding:
- Final handoff expected-vs-actual check:

## Testing adaptation gate

- Current repeated-failure streak:
- Failure family / command:
- Stop threshold: stop before or at five consecutive clear failures of the same command/failure family.
- Material unexpected failure trigger:
- RCA status: not-needed | pending | complete
- RCA-driven scope decision: no scope change | scope expansion | scope correction | blocker
- Child/sub-uberplan appendix:
- Parent plan append/merge actions:
- Resume condition:

## Operational outcome / child terminal states

Allowed terminal states: `operational`, `blocked`, `re_scoped_with_approval`. Parent goals with children remain incomplete until every child has a terminal state. Shared parent proof does not complete children unless each child explicitly scoped that proof as its final outcome.

For production/runtime implementation goals, distinguish `active_blocked` from `hard_blocked_after_safe_action_exhaustion`. A blocked child with runnable safe next actions remains active work and cannot count toward parent completion. A hard blocker requires safe autonomous predecessor work exhausted, exact external/unsafe/irreversible blocker, and next unblock owner/action.

- Plan tree root index path, if used:
- Plan tree status ledger path, if used:

| Child ID | Child plan path | Intended operational outcome | Terminal state | Proof / blocker / re-scope evidence | Remaining gap |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## Production implementation blocker gate

Complete only for production/runtime implementation goals, long unattended production goals, or external/unsafe/irreversible stop points; otherwise record not applicable.

- Production implementation goal? yes/no, why:
- Upfront approval packet status:
- Required child count:
- Operational or user-rescoped child count:
- Hard-blocked-after-safe-action-exhaustion child count:
- Active blocked child count:
- Runnable safe next action count:
- Safe autonomous predecessor work exhausted? yes/no/n/a, evidence:
- Parent completion allowed? yes/no, why:
- Next safe action if parent completion is not allowed:

| Child ID | Required? | Classification: operational / re_scoped_with_approval / hard_blocked_after_safe_action_exhaustion / active_blocked | Runnable safe next actions? | Safe predecessor exhaustion evidence | Exact external/unsafe blocker | Next unblock owner/action |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

## Runtime agent topology

- Config source / observed source:
- Topology mode: standard_6_2 | deep_8_3 | wide_10_3 | custom | n/a
- Current `max_threads`:
- Current `max_depth`:
- Role shape:
- Depth-3 escalation needed? yes/no, why:
- User approval evidence for depth/thread escalation:
- Restore target after campaign:
- Restore proof / blocker:
- Child-agent depth policy:

## Decisions

| Decision | Reason | Date |
|---|---|---|
|  |  |  |

## Skills invoked summary

Record the custom skills actually invoked so the final handoff proves the run used the created Uber skill system instead of generic planning. `Invoked?` means the skill instructions were intentionally loaded/followed; `no` can still mean consulted-only source reading, and should say so.

| Skill | Invoked? yes/no/n/a | Where / artifact | Why invoked, skipped, consulted-only, or n/a | Gap? |
|---|---|---|---|---|
| ubergoal | yes |  | lifecycle wrapper / goal ledger |  |
| uberassess | yes/no |  | source assessment only when applicable |  |
| uberplan | yes/no |  | planning contract / work contract |  |
| uberaccept | yes/no |  | final acceptance / policy-adherence check |  |
| ubersimplify | yes/no |  | complexity/dead-code/modularity audit when applicable |  |
| uberskillevolver | yes/no |  | post-run learning when applicable |  |
| ubershow | yes/no |  | visual artifact when useful |  |
| uberrca | yes/no |  | class-level RCA when applicable |  |
| uber-skill-creator | yes/no |  | skill creation/update when applicable |  |

## Tests/evals/audits

| Evidence layer | Command/artifact | Result | Gap? |
|---|---|---|---|
| Unit/regression |  |  |  |
| Integration |  |  |  |
| UI/browser |  |  |  |
| Evals |  |  |  |
| Architecture audit |  |  |  |
| Code-health/dead-code audit |  |  |  |
| Security/privacy/concurrency/idempotency review |  |  |  |

## Known gaps

-

## Next checkpoint
