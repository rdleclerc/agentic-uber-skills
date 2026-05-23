# Uber Run Receipt

## Run metadata
- Run slug: sample-uber-run
- Date/time: 2026-05-19T13:30:00-07:00
- Project/repo: /tmp/example
- Tier: 2
- Owner/session: test-session
- Outcome: success
- Source branch/commit: session/test abc123

## Skills invoked

| Skill | Invoked? yes/no/n/a | Evidence / artifact | Why invoked, skipped, consulted-only, or n/a | Gap? |
|---|---|---|---|---|
| ubergoal | yes | ledger.md | lifecycle wrapper | none |
| uberassess | n/a | n/a | no external source | none |
| uberplan | yes | plan.md | plan/work contract | none |
| uberaccept | yes | acceptance.md | final acceptance/policy-adherence | none |
| ubersimplify | no | receipt note | no deletion campaign | none |
| uberskillevolver | yes | learning.md | post-run learning | none |
| ubershow | no | n/a | short text enough | none |
| deep-rca | n/a | n/a | no incident/RCA | none |
| uber-skill-creator | n/a | n/a | no skill authoring | none |

## Artifacts

| Artifact | Path / URL / commit | Required? | Present? | Notes |
|---|---|---|---|---|
| Goal ledger | ledger.md | yes | yes | complete |
| Plan / work contract | plan.md | yes | yes | complete |
| Acceptance report | acceptance.md | yes | yes | complete |
| Tests/evals/audits | test.log | yes | yes | pass |
| Diff / commit / PR | abc123 | yes | yes | local commit |
| Learning record | learning.md | yes | yes | complete |

## Gates

| Gate | Expected for this tier? | Evidence | Result: pass/fail/n/a | Gap / owner |
|---|---|---|---|---|
| Goal created/bound or explicitly skipped | yes | ledger.md | pass | none |
| Uberplan or work-contract planning | yes | plan.md | pass | none |
| User expectation / surprise assessment | yes | plan.md and final handoff | pass | none |
| Plan acceptance / thin-harness check | yes | plan.md | pass | none |
| RCA-driven testing adaptation | yes | ledger.md | pass | no repeated clear failures or unexpected scope changes; gate documented |
| Uberaccept final proof | yes | acceptance.md | pass | none |
| Policy-adherence / OpenClaw architecture check | yes | acceptance.md | pass | none |
| Skills invoked summary | yes | ledger.md | pass | none |
| Uberskillevolver learning decision | yes | learning.md | pass | none |

## Fresh-agent replay
- Replay mode: dry-run
- Replay prompt / fixture: tests/fixtures/valid/uber_run_receipt.md
- Fresh-agent or reviewer identity: validator fixture
- Result: pass
- Missing affordances: none
- Follow-up: none

## Behavior verdict
- Did the run use the intended Uber skills? yes
- Did the skills change behavior versus generic planning? yes
- Did the run avoid fat-harness / deterministic-monolith drift? yes
- Did the run produce enough evidence for `uberskillevolver`? yes
- Verdict rationale: receipt names invoked skills, artifacts, gates, replay, and learning handoff.

## Uberskillevolver handoff
- Learning record path: learning.md
- Candidate lessons: L1 run receipt is useful
- Promote now: validator fixture
- Defer: automated telemetry
- No-change rationale: no heavy orchestration
- Safe to commit? yes
