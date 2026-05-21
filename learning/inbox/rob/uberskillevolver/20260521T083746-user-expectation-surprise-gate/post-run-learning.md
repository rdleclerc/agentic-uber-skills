# Post-Run Learning Record

## Run metadata
- Skill(s): ubergoal, uberplan, uberaccept, uberskillevolver
- Date/time: 20260521T083746
- Project/repo: /Users/rob/repos/agentic-uber-skills
- Run slug: user-expectation-surprise-gate
- Tier / risk level: Tier 2 skill/workflow contract update
- Outcome: success
- Owner/session: Codex local session

## Evidence links
List concrete evidence: plan files, diffs, commits, logs, tests, evals, traces, screenshots, PRs, or session notes. Prefer links/paths/summaries over raw private traces.

- `uberplan/SKILL.md`, `uberplan/templates/plan-contract.md`, and `uberplan/scripts/validate_plan_contract.py` now require a user expectation / surprise assessment for Tier 1+ plans.
- `ubergoal/SKILL.md`, `ubergoal/templates/goal-ledger.md`, `ubergoal/templates/uber-run-receipt.md`, and `ubergoal/scripts/validate_uber_run_receipt.py` now track the gate through goal execution.
- `uberaccept/SKILL.md`, `uberaccept/templates/final-acceptance.md`, and `uberaccept/scripts/validate_acceptance_report.py` now require expected-vs-actual user surprise checks before completion.
- Golden eval seeds added in `uberplan/evals/golden_skill_invocations.json`, `ubergoal/evals/golden_skill_invocations.json`, and `uberaccept/evals/golden_skill_invocations.json`.

## What worked
- The user named the failure mode clearly: plans and implementations can surprise them when agents assume intent instead of modeling expected outcome, surprise risk, and ask/flag triggers.
- Treating the phrase as `User expectation / surprise assessment` kept it evidence-bound and testable instead of turning it into vague mind-reading.
- Validators and golden evals paid for themselves because this is a recurring planning/acceptance behavior that can silently drift if kept as prose only.

## What failed or surprised us
- No implementation failure occurred. One validator fixture needed a small rewrite because the new assessment text used "adding validator fixture coverage," which correctly triggered the topology detector in an existing-file-only test.
- The smallest durable change still touched three phase skills because the user wanted both upfront planning behavior and final "what did we actually do?" checks.
- Fresh-agent behavioral evals are still not automated; golden eval seeds and validators are the current regression surface.

## Agent Advocate / human counterfactual
- Did an agent make an avoidable error? The motivating error is anticipatory: an agent can plan or ship something technically valid while violating what the user thought would happen.
- Would a competent human with normal context/tools have made it? Less likely; a good human collaborator would usually say "I think you expect X; Y might surprise you" before taking a risky path.
- Missing context/tool feedback/source authority/memory/approval boundary: planning and acceptance contracts lacked an explicit place to state expected user outcome, surprise risk, ask/flag triggers, and expected-vs-actual delta.
- Upstream invariant that would prevent recurrence: Tier 1+ plans and final acceptance must compare explicit request plus known preferences against planned/actual implementation and flag material mismatches before proceeding or claiming completion.

## Complexity and speed economics
- Complexity added: one required plan section, one goal receipt gate, one acceptance section, validator checks, and golden eval cases.
- Complexity deleted or avoided: no new skill, no new agent lane, no hidden personality/mind-reading rubric, and no broad telemetry system.
- Did benefit clearly exceed total cost by a wide margin? yes; this is a high-value operator-trust invariant and the implementation is small and checkable.
- Hidden downstream costs discovered: agents may overfill the section with generic prose unless validators and examples keep it grounded in evidence, assumptions, ask/flag triggers, and final handoff delta.

## Subagent / lane ROI
- Useful lanes/agents: main-agent skill-creator and uberskillevolver loops were enough.
- Redundant/noisy lanes/agents: no subagents were needed for this contained contract update.
- Parallelism that saved time: parallel file reads shortened orientation; implementation stayed serial to avoid overlapping edits.
- Coordination overhead: low.

## Lesson candidates
For each candidate, link to or summarize a `lesson-candidate.md` record.

| ID | Lesson | Evidence | Decision: promote/defer/delete/no-change | Reason |
|---|---|---|---|---|
| L1 | Add an evidence-bound user expectation / surprise assessment before material plans and a user surprise delta before acceptance. | User request plus patched `uberplan`, `ubergoal`, and `uberaccept` validators/templates/evals. | promote | Prevents a recurring trust failure with small checkable machinery. |
| L2 | Keep theory-of-mind wording grounded in request/preferences/evidence rather than claiming mind-reading. | Section labels and validator terms require expectation, evidence, surprise, assumption, ask/flag, and handoff. | promote | Reduces surprise without adding speculative personality bureaucracy. |
| L3 | Existing topology detectors can catch surprising language in fixtures; update test fixtures to preserve scenario semantics after adding new sections. | `test_existing_file_plan_can_mark_topology_not_applicable` initially failed until the fixture rewrite removed "adding validator fixture coverage." | no-change | The detector behaved correctly; no validator weakening needed. |

## Promotion decision
- Promote now: user expectation / surprise assessment in `uberplan` and `ubergoal`; expected-vs-actual surprise delta in `uberaccept`; receipt/validator/eval coverage.
- Defer: automated fresh-agent behavioral eval harness for these golden cases.
- Delete/simplify: no new `ubertom` or extra review lane; keep the behavior inside existing planning/goal/acceptance contracts.
- No change: topology detector remains strict.
- Human review required before skill edit? no; the current user explicitly authorized iteration on these skills.

## Privacy and redaction
- Sensitive material excluded/redacted: no secrets, customer data, or private raw traces included.
- Raw traces retained? no; only repo file paths and summarized command results are referenced.
- Safe to commit? yes

## Validation / follow-up
- New evals proposed: golden cases for user expectation/surprise in `uberplan`, `ubergoal`, and `uberaccept`.
- Validators/tests proposed: plan-contract section validation, run-receipt gate validation, acceptance-delta section validation, and missing-section tests.
- Skill/template changes proposed: already applied in local repo; pack validation still required before final handoff.
- Owner and deadline: Codex in current session; complete before final response.
