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

## Skills used

| Skill | Used? yes/no/n/a | Evidence / artifact | Why used or skipped | Gap? |
|---|---|---|---|---|
| ubergoal | yes |  | lifecycle wrapper |  |
| uberassess | yes/no/n/a |  | source assessment only when applicable |  |
| uberplan | yes/no/n/a |  | plan/work contract |  |
| uberaccept | yes/no/n/a |  | final acceptance/policy-adherence |  |
| ubersimplify | yes/no/n/a |  | complexity/dead-code/modularity |  |
| uberskillevolver | yes/no/n/a |  | post-run learning |  |
| ubershow | yes/no/n/a |  | visual artifact if useful |  |
| deep-rca | yes/no/n/a |  | class-level RCA if applicable |  |
| skill-creator | yes/no/n/a |  | skill creation/update if applicable |  |

## Artifacts

| Artifact | Path / URL / commit | Required? | Present? | Notes |
|---|---|---|---|---|
| Goal ledger |  | yes/no | yes/no |  |
| Plan / work contract |  | yes/no | yes/no |  |
| Acceptance report |  | yes/no | yes/no |  |
| Tests/evals/audits |  | yes/no | yes/no |  |
| Diff / commit / PR |  | yes/no | yes/no |  |
| Learning record |  | yes/no | yes/no |  |

## Gates

| Gate | Expected for this tier? | Evidence | Result: pass/fail/n/a | Gap / owner |
|---|---|---|---|---|
| Goal created/bound or explicitly skipped |  |  |  |  |
| Uberplan or work-contract planning |  |  |  |  |
| User expectation / surprise assessment |  |  |  |  |
| Plan acceptance / thin-harness check |  |  |  |  |
| Repeated-test-failure adaptation |  |  |  |  |
| Uberaccept final proof |  |  |  |  |
| Policy-adherence / OpenClaw architecture check |  |  |  |  |
| Skills used summary |  |  |  |  |
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
