# Uber Run Receipt

Use this as the thin tracing artifact for an `ubergoal` run. It is not an orchestration log or hidden judge. It records enough evidence for `uberskillevolver` and future fresh-agent replay to decide whether the Uber skills actually helped.

## Run metadata
- Run slug:
- Date/time:
- Project/repo:
- Tier:
- Owner/session:
- Outcome: success | partial | failed | aborted
- Source branch/commit:

## Scope fidelity

- Operator original instruction, verbatim or exact artifact path:
- Goal objective / agent interpreted scope:
- Proposed narrowed scope, if any:
- Explicit deferrals / non-goals:
- Approval evidence for narrowing/deferrals:
- Diff between original and goal scope:
- Scope fidelity verdict: pass / fail / uncertain:

## Runtime agent topology

- Config source / observed source:
- Topology mode: standard_6_2 | deep_8_3 | wide_10_3 | custom | n/a
- Current `max_threads`:
- Current `max_depth`:
- Role shape:
- Depth-3 escalation needed? yes/no/n/a, why:
- User approval evidence for depth/thread escalation:
- Restore target after campaign:
- Restore proof / blocker:
- Child-agent depth policy:

## Skills invoked

`Invoked?` means the skill instructions were intentionally loaded/followed. Use `no` for consulted-only source reading and explain that distinction instead of quietly omitting a relevant skill.

| Skill | Invoked? yes/no/n/a | Evidence / artifact | Why invoked, skipped, consulted-only, or n/a | Gap? |
|---|---|---|---|---|
| ubergoal | yes |  | lifecycle wrapper |  |
| uberassess | yes/no/n/a |  | source assessment only when applicable |  |
| uberplan | yes/no/n/a |  | plan/work contract |  |
| uberaccept | yes/no/n/a |  | final acceptance/policy-adherence |  |
| ubersimplify | yes/no/n/a |  | complexity/dead-code/modularity |  |
| uberskillevolver | yes/no/n/a |  | post-run learning |  |
| ubershow | yes/no/n/a |  | visual artifact if useful |  |
| uberrca | yes/no/n/a |  | class-level RCA if applicable |  |
| uber-skill-creator | yes/no/n/a |  | skill creation/update if applicable |  |

## Artifacts

| Artifact | Path / URL / commit | Required? | Present? | Notes |
|---|---|---|---|---|
| Goal ledger |  | yes/no | yes/no |  |
| Plan / work contract |  | yes/no | yes/no |  |
| Acceptance report |  | yes/no | yes/no |  |
| Tests/evals/audits |  | yes/no | yes/no |  |
| Diff / commit / PR |  | yes/no | yes/no |  |
| Learning record |  | yes/no | yes/no |  |

## Operational outcome / terminal-state summary

| Plan or child ID | Intended operational outcome | Terminal state: operational / blocked / re_scoped_with_approval | Evidence | Remaining gap |
|---|---|---|---|---|
|  |  |  |  |  |

- Proof-only, shadow-only, local-safe-proof, or shared-spine evidence claimed as operational? yes/no, explain:

## Production implementation blocker gate

Required for production/runtime implementation goals, long unattended production goals, or goals with external/unsafe/irreversible stop points; otherwise state why it is not applicable. A blocked child with runnable safe next actions is active work, not completion.

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

## Gates

| Gate | Expected for this tier? | Evidence | Result: pass/fail/n/a | Gap / owner |
|---|---|---|---|---|
| Goal created/bound or explicitly skipped |  |  |  |  |
| Uberplan or work-contract planning |  |  |  |  |
| User expectation / surprise assessment |  |  |  |  |
| Plan acceptance / thin-harness check |  |  |  |  |
| RCA-driven testing adaptation |  |  |  |  |
| Operational outcome / child terminal states |  |  |  |  |
| Uberaccept final proof |  |  |  |  |
| Policy-adherence / OpenClaw architecture check |  |  |  |  |
| Skills invoked summary |  |  |  |  |
| Uberskillevolver learning decision |  |  |  |  |

## Fresh-agent replay
- Replay mode: not-run | dry-run | fresh-agent | manual-review
- Replay prompt / fixture:
- Fresh-agent or reviewer identity:
- Result: pass | partial | fail | n/a
- Missing affordances:
- Follow-up:

## Behavior verdict
- Did the run use the intended Uber skills? yes/no/partial
- Did the skills change behavior versus generic planning? yes/no/unknown
- Did the run avoid fat-harness / deterministic-monolith drift? yes/no/partial
- Did the run produce enough evidence for `uberskillevolver`? yes/no/partial
- Verdict rationale:

## Uberskillevolver handoff
- Learning record path:
- Candidate lessons:
- Promote now:
- Defer:
- No-change rationale:
- Safe to commit? yes/no
