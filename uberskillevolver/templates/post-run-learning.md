# Post-Run Learning Record

## Run metadata
- Skill(s):
- Date/time:
- Project/repo:
- Run slug:
- Tier / risk level:
- Outcome: success | partial | failed | aborted
- Owner/session:

## Evidence links
List concrete evidence: plan files, diffs, commits, logs, tests, evals, traces, screenshots, PRs, or session notes. Prefer links/paths/summaries over raw private traces.

-

## What worked
- What did the skill/process correctly prevent or speed up?
- Which template, lane, validator, or agent paid for itself?

## What failed or surprised us
- What did the plan miss?
- What was slower or noisier than expected?
- What assumption proved false?

## Agent Advocate / human counterfactual
- Did an agent make an avoidable error?
- Would a competent human with normal context/tools have made it?
- Missing context/tool feedback/source authority/memory/approval boundary:
- Upstream invariant that would prevent recurrence:

## Complexity and speed economics
- Complexity added:
- Complexity deleted or avoided:
- Did benefit clearly exceed total cost by a wide margin?
- Hidden downstream costs discovered:

## Subagent / lane ROI
- Useful lanes/agents:
- Redundant/noisy lanes/agents:
- Parallelism that saved time:
- Coordination overhead:

## Runtime topology lesson
- Runtime topology in effect:
- Did plan depth differ from spawned-agent depth?:
- Did the run need depth/thread escalation?:
- Approval and ledger evidence for escalation:
- Restore-to-default evidence:
- Lesson for future campaigns:

## Lesson candidates
For each candidate, link to or summarize a `lesson-candidate.md` record.

| ID | Lesson | Evidence | Decision: promote/defer/delete/no-change | Reason |
|---|---|---|---|---|
| L1 |  |  |  |  |

## Completion-claim regression check

- Did any parent goal claim child plans complete from a shared safe proof spine, readiness gate, registry, local proof, or shadow-only proof?
- Did any production/runtime parent goal close while a blocked child still had runnable safe next actions, instead of remaining `active_blocked` until safe predecessor work was exhausted?
- Did final acceptance include a Safe-work exhaustion adversarial review that enumerated plausible safe next actions for each blocked child?
- If yes, child plans affected:
- Operational Outcome Contract gap:
- Eval/template/validator candidate:
- If giant-plan shallow execution contributed, should `uberplan` Plan Tree Artifact Layout be promoted? yes/no, why:
- Anti-bloat verdict for any durable fix:

## Promotion decision
- Promote now:
- Defer:
- Delete/simplify:
- No change:
- Human review required before skill edit? yes/no

## Privacy and redaction
- Sensitive material excluded/redacted:
- Raw traces retained? yes/no/path:
- Safe to commit? yes/no:

## Validation / follow-up
- New evals proposed:
- Validators/tests proposed:
- Skill/template changes proposed:
- Owner and deadline:
