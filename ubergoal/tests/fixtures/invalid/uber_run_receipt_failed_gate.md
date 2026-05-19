# Uber Run Receipt

## Run metadata
- Run slug: bad-gate
- Date/time: 2026-05-19T13:30:00-07:00
- Project/repo: /tmp/example
- Tier: 2
- Owner/session: test-session
- Outcome: partial
- Source branch/commit: session/test abc123

## Skills used

| Skill | Used? yes/no/n/a | Evidence / artifact | Why used or skipped | Gap? |
|---|---|---|---|---|
| ubergoal | yes | ledger.md | lifecycle wrapper | none |
| uberassess | n/a | n/a | no external source | none |
| uberplan | yes | plan.md | plan/work contract | none |
| uberaccept | no | missing | skipped accidentally | acceptance gap |
| ubersimplify | no | receipt note | no deletion campaign | none |
| uberskillevolver | no | missing | not run | learning gap |
| ubershow | no | n/a | short text enough | none |
| deep-rca | n/a | n/a | no incident/RCA | none |
| skill-creator | n/a | n/a | no skill authoring | none |

## Artifacts
| Artifact | Path / URL / commit | Required? | Present? | Notes |
|---|---|---|---|---|
| Goal ledger | ledger.md | yes | yes | complete |
| Plan / work contract | plan.md | yes | yes | complete |
| Acceptance report | missing | yes | no | missing |

## Gates
| Gate | Expected for this tier? | Evidence | Result: pass/fail/n/a | Gap / owner |
|---|---|---|---|---|
| Goal created/bound or explicitly skipped | yes | ledger.md | pass | none |
| Uberplan or work-contract planning | yes | plan.md | pass | none |
| Uberaccept final proof | yes | missing | fail | owner |

## Fresh-agent replay
- Replay mode: not-run
- Replay prompt / fixture: none
- Fresh-agent or reviewer identity: none
- Result: n/a
- Missing affordances: acceptance skipped
- Follow-up: run acceptance

## Behavior verdict
- Did the run use the intended Uber skills? partial
- Did the skills change behavior versus generic planning? unknown
- Did the run avoid fat-harness / deterministic-monolith drift? yes
- Did the run produce enough evidence for `uberskillevolver`? no
- Verdict rationale: acceptance missing.

## Uberskillevolver handoff
- Learning record path: missing
- Candidate lessons: skipped acceptance
- Promote now: none
- Defer: fix receipt
- No-change rationale: none
- Safe to commit? no
