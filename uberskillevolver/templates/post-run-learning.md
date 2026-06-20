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

## Recent-feedback sweep, if applicable
- Lookback window:
- User-reported fixes collected:
- Deduplicated failure patterns:
- Current-state verification:
- In-scope surfaces audited:
- Confirmed matches fixed or converted to evals/validators:
- Remaining blockers / no-change rationale:

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

## Red/green / false-green lesson check

- Did a green command fail to prove the real user-visible, black-box, integration, eval, or target-system risk?
- Would a red/green proof-ledger field, negative fixture, or Black-box Tester / Quality-Eval Auditor checklist item prevent recurrence?
- Is standalone `ubereval` extraction justified by repeated evidence, or is `no change` / existing-skill patch better?

## Lesson candidates
For each candidate, link to or summarize a `lesson-candidate.md` record.

| ID | Lesson | Evidence | Decision: promote/defer/delete/no-change | Reason |
|---|---|---|---|---|
| L1 |  |  |  |  |

## Scope-fidelity regression check

- Did the agent narrow, reframe, or defer the Operator original instruction?
- Did any second reviewer see only the agent's summary instead of the Operator original instruction, verbatim or exact artifact path?
- Did the reviewer answer whether the proposed scope satisfied the original instruction?
- Approval evidence for narrowing/deferrals:
- Scope fidelity verdict that should have been required:
- Eval/template/validator candidate:
- Anti-bloat verdict for any durable fix:

## Frame-adhesion / anti-roleplay regression check

- Did the reviewer accept the role Codex invited it to play without naming or challenging that role?
- Did the reviewer use Codex's terminology without a plain-language restatement tied to the Operator original instruction?
- Were three concrete reject conditions stated before approval language?
- Was a highly one-sided `Accepted`/`No material impact` ledger treated as proof rather than a rubber-stamp warning?
- Was model review treated as reduced-noise rather than zero-noise, with human spot-checks or observable success criteria still named?
- Smallest durable fix candidate: skill text / template field / eval fixture / no change:

## Slop register decision

Use this only for repeated or severe AI-generated-code failure patterns; otherwise record `not needed` to avoid bloat.

- Slop-register entry needed? yes/no, why:
- Pattern class: plausible-wrong-logic / over-engineering / convention-blindness / hallucinated-or-deprecated-API / defensive-overreach / cargo-cult-pattern / other:
- Concrete evidence:
- Prevention feedback for prompts/skills/context:
- Candidate deterministic check or CI guard, if mechanical:
- Why this is not hidden semantic authority:
- Revert/delete condition:

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
- Champion/holdout result for prompt/skill/config tuning:
  - Current champion:
  - Working set:
  - Untouched holdouts:
  - Must-pass checks:
  - Promotion margin / budget:
  - Challenger result:
  - Promote challenger? yes/no, why:
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
