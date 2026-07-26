# Post-run learning record

## Run metadata

- Skills: UberPlan, UberGoal, UberAccept, UberSkillCreator, Uberskillevolver
- Date: 2026-07-25
- Repo: `/Users/rob/repos/worktrees/uberplan-transfer-v1`
- Tier: 2, prompt/skill/eval behavior
- Outcome: behavioral candidates selected and current-hash Claude gate passed;
  final promotion remains subject to UberAccept and operator-controlled Git/install actions

## Evidence links

- `evals/uberplan-v3/results/current-promotion.json`
- `evals/uberplan-v3/results/transfer-selected.md`
- `evals/ubergoal-v1/results/current-promotion.json`
- `evals/ubergoal-v1/results/champion-comparison.md`
- `evals/uberaccept-v1/results/current-promotion.json`
- `tests/test_uberplan_v3_eval_boundary.py`
- `tests/test_ubergoal_v1_eval_boundary.py`
- `tests/test_uberaccept_v1_eval_boundary.py`
- `uberaccept/tests/test_validators.py`
- `coordination/uber-skills-56-eval-iteration/independent-review.md`
- `coordination/uber-skills-56-eval-iteration/claude-rereview-2026-07-26.md`
- `coordination/uber-skills-56-eval-iteration/failure-intake.md`

## What worked

- Champion/challenger behavior, hidden rubrics, holdouts, and forward cases
  prevented a smaller but shallower UberPlan iteration from winning.
- Typed lifecycle states caught distinctions that generic reject/block language
  hid: local repair, replan, operator decision, unavailable gate, and
  authoritative rejection.
- One independent exact-diff review found evidence-package and validator seams
  that shape tests missed.

## What failed or surprised us

- The first saved eval tests checked fixture shape but not retained behavioral
  receipts. Green tests therefore overstated promotion evidence.
- UberAccept's old durable validator defaulted missing status to `accepted` even
  after the skill prompt prohibited that fallback.
- Two initially frozen rubric expectations conflated reverting unapproved scope
  with operator decision, and missing authority with infrastructure failure.
  Original rubrics and first-run receipts are now retained beside corrections.
- A fresh agent read the champion path once despite an explicit worktree path;
  the invalid receipt was rejected and rerun.

## Agent Advocate / human counterfactual

- Avoidable errors: initial shape-only receipt checks and one wrong-checkout
  agent run overstated or invalidated evidence.
- A competent human given the exact worktree, hidden rubric, and promotion
  receipt contract would likely have rejected both.
- Missing feedback/source authority: the first test version did not require
  exact current-skill hashes and complete declared-group coverage.
- Upstream invariant: every promotion receipt binds the exact skill hash and all
  manifest groups; an output from any other checkout is invalid.

## Complexity and speed economics

- Added: three reusable behavioral suites, compact promotion receipts, typed
  validator states, and focused boundary tests.
- Avoided: review-board orchestration, a new eval service, a new acceptance
  harness, universal reports for contained work, and pack-wide validator rewrite.
- Deleted/simplified: UberGoal is below its 800-word budget; UberAccept is about
  half the champion instruction size while preserving activated riders.

## Subagent / lane ROI

- Useful: fresh-context case agents and blind judges with exact raw receipts.
- Useful: one final exact-diff reviewer after behavioral promotion.
- Redundant: repeated generic reviewers or default boards; they were not added.
- Lesson: aggregate summaries are diagnostic, not proof. Preserve the raw
  decision fields needed by the frozen rubric.

## Runtime topology lesson

- Runtime topology in effect: one root goal owner with bounded fresh-context
  case/review agents; no service, scheduler, hidden judge, or recursive harness.
- Plan depth: one authoritative bounded plan; no child plan tree was activated.
- Spawned-agent depth: one level in the retained evaluation work; deeper history
  is not needed to support the promotion claim.
- Depth/thread escalation: not used for implementation authority; independent
  lanes were activated only for frozen cases and exact-diff review.
- Restore evidence: no runtime topology or agent-depth configuration was
  mutated, so restore-to-default is not applicable.
- Lesson: preserve raw receipts and exact checkout identity instead of adding
  another orchestration layer.

## Red/green and false-green lesson

Green lint/shape tests do not prove source reading, status truth, or transfer
quality. Every promoted skill now has retained behavioral receipts; UberAccept
also has focused validator tests for missing status and non-accepted states.
No standalone `ubereval` skill is justified.

## Lesson candidates

| ID | Lesson | Evidence | Decision | Reason |
|---|---|---|---|---|
| L1 | Missing/unknown status must never synthesize accepted or rejected | UberAccept working and forward receipts plus validator tests | promote | Prompt and durable validator now agree |
| L2 | Repair, replan, operator decision, unavailable gate, and rejection need distinct states | UberGoal and UberAccept working/holdout/forward receipts | promote | Cases changed decisions materially |
| L3 | Retain original rubric plus first blind receipt when correcting a benchmark | UberAccept original/corrected rubrics and first blind receipt | promote | Makes semantic correction auditable |
| L4 | Default review boards and universal reports improve ceremony, not decision quality | Selected skill hashes and exact-diff review | promote | One risk-specific lane and activated riders preserved quality |
| L5 | Add a new orchestration/eval service | Existing file-based suites and unittest boundaries | no change | Existing substrate is sufficient |

## Completion-claim regression check

- Shared safe proof spine: the green local suite and Sol review were treated as
  supporting evidence, not as permission to close the parent goal.
- Operational Outcome Contract: the repository's independent Claude gate
  passed at the current hash. The operator then authorized commit and local
  installation; merge, push, main adoption, and other live states remain
  distinct.
- No child or parent was called complete while a safe next action remained.
  Local checks were exhausted before the repeated external blocker verdict.
- Eval/template/validator candidate: the existing hash-and-coverage boundary
  tests and learning-record validator cover the observed false-green risks; no
  new template or harness is needed.
- Anti-bloat verdict: no additional completion machinery is justified.

## Promotion decision

- UberPlan: promote behaviorally; all working, holdout, forward, and transfer
  cases pass. Transfer output size remains a diagnostic, not a hard truth failure.
- UberGoal: promote behaviorally; the frozen `c8469eec` champion comparison
  shows the challenger preserves source/safety behavior while improving typed
  lifecycle truth and removing universal artifact/review ceremony.
- UberAccept: promote behaviorally; all working, holdout, and split forward
  gates pass, and the durable validator now fails closed.
- The current-hash Claude Opus gate passed. Implementation commit `75e323a`
  and local Codex/Claude installation are proved; do not claim merge, push,
  main adoption, or other live state.

## Slop register and loop checks

- Slop register: not needed; the failures are now direct eval/validator cases.
- Loop mode: not applicable.
- Scope fidelity: pass; no new architecture, service, or unrelated skill rewrite.

## Privacy and redaction

- Sensitive material excluded/redacted: yes; the record contains only local
  paths, hashes through linked receipts, decisions, and test outcomes.
- Raw traces retained: the selected UberPlan hash was freshly replayed across
  all 10 cases under
  `.uberlearn-local/uberplan-v3/2026-07-26/manifest.md`; its three raw artifacts
  are hash-recorded in the promotion receipt. This ignored store is local, not
  portable; future machines rerun the committed suite. Sanitized committed
  results remain under each suite's `results/`, with no credentials or private
  customer data retained.
- Safe to commit: yes. The operator explicitly authorized commit and install.
  Implementation commit `75e323a` was created, all ten pack skills were linked
  into both local Codex and Claude skill roots, strict install sync passed, and
  all 20 installed-package shape checks passed.

## Validation / follow-up

- New evals proposed: none; the saved working, holdout, forward, and transfer
  suites are the reusable cross-model asset.
- Validators/tests proposed: none beyond the implemented hash/coverage and
  fail-closed status checks.
- Skill/template changes proposed: no further change.
- Owner and deadline: the scoped run is complete through local installation;
  the operator separately controls any merge, push, main adoption, or broader
  deployment action.
