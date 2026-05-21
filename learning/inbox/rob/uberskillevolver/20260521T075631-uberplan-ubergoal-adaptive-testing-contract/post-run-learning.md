# Post-Run Learning Record

## Run metadata
- Skill(s): ubergoal, uberplan, deep-rca, uberaccept, uber-skill-creator, uberskillevolver
- Date/time: 20260521T075631
- Project/repo: /Users/rob/repos/agentic-uber-skills
- Run slug: uberplan-ubergoal-adaptive-testing-contract
- Tier / risk level: Tier 2/3 skill and multi-agent workflow contract update
- Outcome: success
- Owner/session: Codex GUI session with Rob

## Evidence links
List concrete evidence: plan files, diffs, commits, logs, tests, evals, traces, screenshots, PRs, or session notes. Prefer links/paths/summaries over raw private traces.

- `uberplan/SKILL.md`: changed `uberplan` from short-slice planning toward long-running goal planning, thread highlights, `.md` plan file, proof ladder, over-orchestration review, and testing adaptation.
- `uberplan/templates/plan-contract.md`: added Goal execution posture, Agent execution proof ladder, Pre-presentation over-orchestration review, and Testing adaptation gate.
- `uberplan/scripts/validate_plan_contract.py`: now validates long-running goal posture, proof ladder, over-orchestration review, and repeated-test-failure adaptation.
- `ubergoal/SKILL.md`: added execution lifecycle step to stop repeated clear test failures, run `deep-rca`, revise via `uberplan`, and resume under the same goal.
- `deep-rca/SKILL.md`: added repeated test failure trigger at or before five clear failures.
- `uberaccept/SKILL.md`: blocks completion when repeated clear failures exceeded five attempts without RCA, plan revision, and resumed-goal evidence.
- `ubergoal/templates/goal-ledger.md` and `ubergoal/templates/uber-run-receipt.md`: added testing adaptation gate/receipt fields.
- Eval seeds updated in `uberplan/evals/golden_skill_invocations.json`, `ubergoal/evals/golden_skill_invocations.json`, and `deep-rca/evals/golden_skill_invocations.json`.
- Validation passed: `python3 -B -m unittest discover -s uberplan/tests -v`, `python3 -B -m unittest discover -s ubergoal/tests -v`, `python3 -B -m unittest discover -s deep-rca/tests -v`, `python3 scripts/lint_pack_contract.py`, `python3 -m unittest discover -s tests -v`, `quick_validate.py` for `ubergoal`, `uberplan`, and `deep-rca`, installed-copy lints, and `git diff --check`.

## What worked
- The user caught two real skill-contract gaps quickly: `uberplan` was drifting toward short slices, and repeated test failures needed an adaptive RCA/replan loop rather than brute-force retrying.
- The existing pack structure paid for itself: `uberplan` owned the planning contract and validator, `ubergoal` owned lifecycle adaptation, `deep-rca` owned the RCA trigger, and `uberaccept` owned final blocker enforcement.
- Validator and eval surfaces made the lessons durable without adding a new skill or hidden orchestration layer.

## What failed or surprised us
- I initially used `uber-skill-creator` guidance but did not run `uberskillevolver` at final closeout for a skill-behavior change. Rob had to ask directly.
- The first implementation fixed the skill behavior but skipped the explicit learning artifact/promotion gate the pack already requires for Tier 2/3 skill and workflow updates.
- The correction showed that the run receipt and final response need to make `uberskillevolver` usage harder to forget after substantial skill changes.

## Agent Advocate / human counterfactual
- Did an agent make an avoidable error? Yes. I implemented durable skill changes without immediately creating the post-run learning record.
- Would a competent human with normal context/tools have made it? A careful maintainer probably would have opened the learning loop because the change touched multiple skill contracts and evals.
- Missing context/tool feedback/source authority/memory/approval boundary: The final-closeout habit checked tests and installed skill state, but did not force a learning-loop check when skill files changed.
- Upstream invariant that would prevent recurrence: Any Tier 2/3 skill, prompt, workflow, multi-agent protocol, or agentic-system change should close with an explicit `uberskillevolver` decision: used, skipped with reason, or blocked.

## Complexity and speed economics
- Complexity added: one sanitized learning packet, new eval seeds, validator checks, and small template fields across existing skills.
- Complexity deleted or avoided: no new `ubercode`/testing-orchestration skill, no hidden retry telemetry, no new standalone test-loop controller.
- Did benefit clearly exceed total cost by a wide margin? Yes. The rules prevent two high-cost failure modes: wrong-sized `uberplan` outputs and agents burning cycles on systematic test failures.
- Hidden downstream costs discovered: More required sections can slow plan writing; this is controlled by keeping them short, validator-backed, and scoped to Tier 1+ or agentic/Tier 2+ work.

## Subagent / lane ROI
- Useful lanes/agents: Main-thread skill editing plus validator/eval checks were sufficient; no live subagent was needed for this contained repository change.
- Redundant/noisy lanes/agents: A broad review board would have been too much ceremony for this cleanup.
- Parallelism that saved time: Parallel reads and test commands saved wall-clock time without creating coordination overhead.
- Coordination overhead: Low; changes stayed in existing skill packages and existing test/eval surfaces.

## Lesson candidates
For each candidate, link to or summarize a `lesson-candidate.md` record.

| ID | Lesson | Evidence | Decision: promote/defer/delete/no-change | Reason |
|---|---|---|---|---|
| L1 | `uberplan` must produce long-running goal plans, not default short `uberslice` plans. | `uberplan/SKILL.md`, `plan-contract.md`, validator tests, golden evals. | promote | Repeated user correction and high risk of future planning drift justify small durable contract changes. |
| L2 | Agentic workflow plans should prove Codex subagent capability before OpenClaw/target-runtime parity, then require two parity proofs before readiness. | `Agent execution proof ladder` section and validator coverage. | promote | This turns a proven strategy into an explicit proof ladder without adding a new orchestrator. |
| L3 | After clear repeated test failures, stop by five attempts, run RCA, revise via `uberplan`, and continue under `ubergoal`. | `ubergoal` lifecycle, `Testing adaptation gate`, `deep-rca` trigger, `uberaccept` completion blocker, receipt gate. | promote | Prevents systematic error loops and aligns testing with adaptive goal execution. |
| L4 | Skill-behavior changes need an explicit `uberskillevolver` closeout decision. | This record exists only because Rob asked whether `uberskillevolver` was used. | promote | The miss was process-level and easy to catch with a lightweight receipt/learning expectation. |
| L5 | Fresh-agent behavioral proof for these exact skill changes is still not automated. | Current evidence is validators/evals, not a fresh-agent replay. | defer | Worth testing later, but building a full harness now would add more machinery than this run needs. |

## Promotion decision
- Promote now: L1, L2, L3, and L4 were promoted into existing skill instructions, templates, validators, eval seeds, receipt gates, and this learning packet.
- Defer: L5 fresh-agent behavioral replay harness; keep as future evidence work unless the drift recurs.
- Delete/simplify: No new skill created; no standalone execution/test-loop orchestrator added.
- No change: No raw telemetry or hidden self-modification system.
- Human review required before skill edit? no, because Rob explicitly authorized the skill revisions in this session; human review is still required before commit/push.

## Privacy and redaction
- Sensitive material excluded/redacted: yes; record contains repo paths, file names, commands, and distilled session lessons only.
- Raw traces retained? no/path: no raw private transcript or logs included.
- Safe to commit? yes: sanitized learning packet under `learning/inbox/rob/...`.

## Validation / follow-up
- New evals proposed: Already added golden evals for long-running `uberplan`, Codex-to-OpenClaw proof ladder, over-orchestration self-review, repeated test failure RCA/replan, and `deep-rca` repeated test failure trigger.
- Validators/tests proposed: Already added plan validator checks and run receipt gate for testing adaptation.
- Skill/template changes proposed: Already applied in `ubergoal`, `uberplan`, `deep-rca`, `uberaccept`, README/ROADMAP/AGENTS, templates, and adapter metadata.
- Owner and deadline: Codex completed the record in this session; remaining follow-up is optional fresh-agent replay before commit/push if Rob wants higher confidence.
