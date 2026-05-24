# Post-Run Learning Record

## Run metadata
- Skill(s): ubergoal
- Date/time: 20260509T090000
- Project/repo: /tmp/example
- Run slug: example-run
- Tier / risk level: Tier 2
- Outcome: success
- Owner/session: test

## Evidence links
- Plan: /tmp/example/plan.md
- Tests: `python3 -m unittest` PASS

## What worked
- The complexity gate prevented a new unnecessary template.

## What failed or surprised us
- The first plan missed a validator case.

## Agent Advocate / human counterfactual
- A competent human would likely have noticed the missing fixture from the test naming pattern.
- Missing context/tool feedback/source authority/memory/approval boundary: test fixture map.
- Upstream invariant that would prevent recurrence: validator tests must include positive and negative fixtures.

## Complexity and speed economics
- Complexity added: one fixture.
- Complexity deleted or avoided: no new daemon.
- Did benefit clearly exceed total cost by a wide margin? yes.
- Hidden downstream costs discovered: fixture upkeep.

## Subagent / lane ROI
- Useful lanes/agents: inline simplifier.
- Redundant/noisy lanes/agents: none.
- Parallelism that saved time: none.
- Coordination overhead: low.


## Runtime topology lesson
- Runtime topology in effect: standard local policy `max_threads=6`, `max_depth=2`; no deep-campaign mode used.
- Did plan depth differ from spawned-agent depth?: yes; plan depth can be represented in files without increasing spawned-agent depth.
- Did the run need depth/thread escalation?: no; depth/thread escalation was not needed.
- Approval and ledger evidence for escalation: not applicable; no escalation.
- Restore-to-default evidence: restore not needed because the run stayed at default 6/2.
- Lesson for future campaigns: keep plan depth and spawned-agent depth distinct; ask before depth-3 escalation.

## Lesson candidates
| ID | Lesson | Evidence | Decision: promote/defer/delete/no-change | Reason |
|---|---|---|---|---|
| L1 | Add validator fixture discipline | test failure | promote | repeated risk |

## Completion-claim regression check

- Did any parent goal claim child plans complete from a shared safe proof spine, readiness gate, registry, local proof, or shadow-only proof? no; no shared safe proof spine or child-plan completion claim was in scope.
- If yes, child plans affected: none.
- Operational Outcome Contract gap: none for this run; future runs should compare claimed state to the contract.
- Eval/template/validator candidate: no-change for this run; promote only when evidence shows claim blur.
- If giant-plan shallow execution contributed, should `uberplan` Plan Tree Artifact Layout be promoted? no; giant-plan shallow execution did not occur in this fixture.
- Anti-bloat verdict for any durable fix: no new harness; keep this as a lightweight learning check unless failures recur.

## Promotion decision
- Promote now: L1 as validator fixture guidance.
- Defer: none.
- Delete/simplify: none.
- No change: no new agent.
- Human review required before skill edit? yes

## Privacy and redaction
- Sensitive material excluded/redacted: none.
- Raw traces retained? no.
- Safe to commit? yes.

## Validation / follow-up
- New evals proposed: validator fixture missing case.
- Validators/tests proposed: yes.
- Skill/template changes proposed: small template line.
- Owner and deadline: test owner today.
