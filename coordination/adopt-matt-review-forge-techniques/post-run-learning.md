# Post-Run Learning Record

## Run metadata
- Skill(s): ubergoal, uberassess, uberplan, uberaccept, uberskillevolver
- Date/time: 2026-06-20T10:43:33-07:00
- Project/repo: /Users/rob/repos/agentic-uber-skills
- Run slug: adopt-matt-review-forge-techniques
- Tier / risk level: Tier 2 skill-contract and eval change
- Outcome: success
- Owner/session: Codex / goal 019ee589-8862-7491-af8d-29262435ea47

## Evidence links
- Scope artifact: coordination/adopt-matt-review-forge-techniques/scope.md
- Candidate diff: coordination/adopt-matt-review-forge-techniques/receipts/candidate.diff
- Claude prompt/output: coordination/adopt-matt-review-forge-techniques/receipts/claude-adversary-prompt.md and coordination/adopt-matt-review-forge-techniques/receipts/claude-adversary-output.md
- Test logs: coordination/adopt-matt-review-forge-techniques/receipts/uberplan-tests.log, coordination/adopt-matt-review-forge-techniques/receipts/uberaccept-tests.log, coordination/adopt-matt-review-forge-techniques/receipts/root-tests.log
- Lint/validator logs: coordination/adopt-matt-review-forge-techniques/receipts/pack-lint.log, coordination/adopt-matt-review-forge-techniques/receipts/quick-validate-uberplan.log, coordination/adopt-matt-review-forge-techniques/receipts/quick-validate-uberaccept.log, coordination/adopt-matt-review-forge-techniques/receipts/git-diff-check.log

## What worked
- The prior uberassess packet prevented wholesale import of external skills and kept the patch inside existing uberplan and uberaccept surfaces.
- Claude adversarial review found a real gap: the first acceptance validator version required section presence but not completed spec/standards fields.
- Validator-backed acceptance was worth the extra cost because the section now requires specific fields and table rows.

## What failed or surprised us
- The initial scope artifact was accidentally created in the previous Gaia cwd before being moved to this repo; the accidental file was removed and unrelated Gaia dirty files were not touched.
- Claude could not verify test execution from the first candidate bundle because logs were not yet saved under receipts.
- The first spec-vs-standards gate was weaker than intended until the validator was deepened.

## Agent Advocate / human counterfactual
- Did an agent make an avoidable error? yes, the first validator patch was too presence-only.
- Would a competent human with normal context/tools have made it? a careful reviewer might catch it, and Claude did.
- Missing context/tool feedback/source authority/memory/approval boundary: missing field-level validation for a newly required final acceptance section.
- Upstream invariant that would prevent recurrence: new acceptance-report sections that claim to block completion need field-level validator checks when the failure class is mechanical enough to test.

## Complexity and speed economics
- Complexity added: two uberplan sections, one uberaccept section, one acceptance validator requirement, three eval seeds, and fixture/test coverage.
- Complexity deleted or avoided: no new skills, no parallel review workflow, no hidden semantic judge.
- Did benefit clearly exceed total cost by a wide margin? yes, because the changes target recurring planning/acceptance failure shapes and are test-backed.
- Hidden downstream costs discovered: newly required acceptance sections are backward-incompatible for old draft reports; this is acceptable for templates/fixtures but should be noted for users validating old reports.

## Subagent / lane ROI
- Useful lanes/agents: Claude adversarial review; it produced one accepted validator-hardening challenge.
- Redundant/noisy lanes/agents: no additional subagents were needed.
- Parallelism that saved time: local lint/tests ran in parallel where independent.
- Coordination overhead: limited to one scope artifact, one review prompt, one output, and saved command logs.

## Runtime topology lesson
- Runtime topology in effect: standard single Codex root session plus one external Claude review lane; no spawned Codex campaign.
- Did plan depth differ from spawned-agent depth?: plan depth was one goal with no child plan tree; spawned-agent depth was zero for Codex subagents.
- Did the run need depth/thread escalation?: no depth/thread escalation was needed.
- Approval and ledger evidence for escalation: not applicable; no escalation.
- Restore-to-default evidence: not applicable; no runtime topology was changed, so restore was unnecessary.
- Lesson for future campaigns: keep one Claude challenge round for narrow skill edits unless it surfaces unresolved material risk.

## Red/green / false-green lesson check

- Did a green command fail to prove the real user-visible, black-box, integration, eval, or target-system risk? no; after Claude challenge, executed logs were saved as reproducible receipts.
- Would a red/green proof-ledger field, negative fixture, or Black-box Tester / Quality-Eval Auditor checklist item prevent recurrence? yes, the new acceptance validator test for missing spec-fidelity verdict prevents the presence-only false green.
- Is standalone `ubereval` extraction justified by repeated evidence, or is `no change` / existing-skill patch better? no standalone extraction; existing skill patch and eval seeds were enough.

## Lesson candidates

| ID | Lesson | Evidence | Decision: promote/defer/delete/no-change | Reason |
|---|---|---|---|---|
| L1 | New required acceptance sections should get field-level validator coverage when they block completion | Claude C2 plus updated validate_acceptance_report.py and test_acceptance_requires_spec_fidelity_verdict_field | promote | Small mechanical validator prevents the exact failure class |
| L2 | Pre-PRD grilling and vertical issue slicing are useful inside uberplan, not as new skills | Matt/Review Forge assessment plus narrow diff | promote | Existing skill surfaces can absorb the behavior with less context bloat |
| L3 | Save executed command logs before asking acceptance to rely on test evidence | Claude C1 plus receipts/*.log | promote | Reproducible receipts are cheap and useful |

## Scope-fidelity regression check

- Did the agent narrow, reframe, or defer the Operator original instruction? yes, narrowed to the previously assessed narrow adoption into existing Uber skills.
- Did any second reviewer see only the agent's summary instead of the Operator original instruction, verbatim or exact artifact path? no, Claude prompt put the operator original instruction first and pointed to scope.md plus candidate.diff.
- Did the reviewer answer whether the proposed scope satisfied the original instruction? yes, Claude returned Scope Fidelity PASS with a residual note about the tmp assessment.
- Approval evidence for narrowing/deferrals: prior assessment recommended narrow adoption; user then instructed implementation.
- Scope fidelity verdict that should have been required: pass with residual that the scratch /tmp assessment is not committed.
- Eval/template/validator candidate: no additional scope-fidelity change needed.
- Anti-bloat verdict for any durable fix: no change beyond existing scope artifact and review prompt requirement.

## Frame-adhesion / anti-roleplay regression check

- Did the reviewer accept the role Codex invited it to play without naming or challenging that role? no, Claude accepted with modification and named conditional approval.
- Did the reviewer use Codex's terminology without a plain-language restatement tied to the Operator original instruction? no material issue; it tied review to the implementation/acceptance/commit/push loop.
- Were three concrete reject conditions stated before approval language? yes.
- Was a highly one-sided `Accepted`/`No material impact` ledger treated as proof rather than a rubber-stamp warning? no; Claude raised two challenges and one drove a code change.
- Was model review treated as reduced-noise rather than zero-noise, with human spot-checks or observable success criteria still named? yes; deterministic tests and receipts remained the proof.
- Smallest durable fix candidate: no change; the review workflow worked as intended.

## Slop register decision

Use this only for repeated or severe AI-generated-code failure patterns; otherwise record `not needed` to avoid bloat.

- Slop-register entry needed? no, this was a single caught validator-depth issue and it was fixed directly.
- Pattern class: other, presence-only validator for a new required section.
- Concrete evidence: Claude C2 and updated validator/test.
- Prevention feedback for prompts/skills/context: require field-level coverage for mechanical acceptance gates.
- Candidate deterministic check or CI guard, if mechanical: test_acceptance_requires_spec_fidelity_verdict_field.
- Why this is not hidden semantic authority: it checks explicit markdown fields and rows, not natural-language truth.
- Revert/delete condition: revert if the section creates widespread false positives without preventing spec/standards blur in real acceptance runs.

## Completion-claim regression check

- Did any parent goal claim child plans complete from a shared safe proof spine, readiness gate, registry, local proof, or shadow-only proof? no shared safe proof spine or child-plan completion claim was used.
- Did any production/runtime parent goal close while a blocked child still had runnable safe next actions, instead of remaining `active_blocked` until safe predecessor work was exhausted? no production/runtime parent goal was in scope.
- Did final acceptance include a Safe-work exhaustion adversarial review that enumerated plausible safe next actions for each blocked child? not applicable; no production/runtime blocked children.
- If yes, child plans affected: n/a.
- Operational Outcome Contract gap: none for local skill-package implementation.
- Eval/template/validator candidate: no additional completion-claim candidate; existing acceptance validator remains sufficient.
- If giant-plan shallow execution contributed, should `uberplan` Plan Tree Artifact Layout be promoted? no, this run did not use a plan tree and did not show giant-plan shallow execution.
- Anti-bloat verdict for any durable fix: no additional completion-claim machinery.

## Promotion decision
- Promote now: L1, L2, L3 through this patch's validators/templates/evals/receipts.
- Defer: no fresh-agent behavioral harness; existing eval seeds are enough for this narrow patch.
- Delete/simplify: no new skill or Review Forge artifact tree added.
- No change: no standalone ubereval/ubertesting extraction.
- Human review required before skill edit? yes, satisfied by user instruction and Claude adversarial review.

## Privacy and redaction
- Sensitive material excluded/redacted: yes; only public-source summaries, local diffs, and command logs included.
- Raw traces retained? yes, under coordination/adopt-matt-review-forge-techniques/receipts/.
- Safe to commit? yes.

## Validation / follow-up
- New evals proposed: already added to uberplan and uberaccept golden invocation files.
- Validators/tests proposed: already added to acceptance validator and package tests.
- Skill/template changes proposed: already implemented in uberplan and uberaccept.
- Owner and deadline: Codex in this run before commit/push.
