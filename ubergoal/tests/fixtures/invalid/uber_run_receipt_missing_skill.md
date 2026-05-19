# Uber Run Receipt

## Run metadata
- Run slug: bad
- Date/time: 2026-05-19T13:30:00-07:00
- Project/repo: /tmp/example
- Tier: 2
- Owner/session: test-session
- Outcome: success
- Source branch/commit: session/test abc123

## Skills used

| Skill | Used? yes/no/n/a | Evidence / artifact | Why used or skipped | Gap? |
|---|---|---|---|---|
| ubergoal | yes | ledger.md | lifecycle wrapper | none |
| uberplan | yes | plan.md | plan/work contract | none |

## Artifacts
| Artifact | Path / URL / commit | Required? | Present? | Notes |
|---|---|---|---|---|
| Goal ledger | ledger.md | yes | yes | complete |

## Gates
| Gate | Expected for this tier? | Evidence | Result: pass/fail/n/a | Gap / owner |
|---|---|---|---|---|
| Uberplan or work-contract planning | yes | plan.md | pass | none |

## Fresh-agent replay
- Replay mode: not-run
- Replay prompt / fixture: none
- Fresh-agent or reviewer identity: none
- Result: n/a
- Missing affordances: none
- Follow-up: none

## Behavior verdict
- Did the run use the intended Uber skills? partial
- Did the skills change behavior versus generic planning? unknown
- Did the run avoid fat-harness / deterministic-monolith drift? yes
- Did the run produce enough evidence for `uberskillevolver`? partial
- Verdict rationale: incomplete skills table.

## Uberskillevolver handoff
- Learning record path: none
- Candidate lessons: none
- Promote now: none
- Defer: record missing
- No-change rationale: none
- Safe to commit? no
