# Agentic Uber Skills Roadmap

This roadmap keeps the skill pack evolving without turning it into bureaucracy. The rule is always: add durable machinery only when benefit is **clearly much greater than** total downstream cost.

## Current architecture

- `ubergoal` — thin lifecycle wrapper: classify, route, optional goal launch, ledger, acceptance, learning.
- `uberplan` — rigorous planning: plan contract, review lanes, exploration trails, Agent Advocate RCA, first-principles simplifier, confidence gate.
- `uberaccept` — adversarial final proof: evidence audit, architecture drift, Agent Advocate final check, completion recommendation.
- `uberskillevolver` — post-run learning loop: learning records, lesson candidates, promotion batches, anti-bloat gate.
- `deep-rca` — class-level root cause analysis before patches.

## Near-term priorities

1. **Fresh-agent behavioral evals**
   - Verify a fresh agent routes `ubergoal → uberplan → uberaccept → uberskillevolver` correctly.
   - Turn golden eval seeds into an executable or semi-automated harness.
   - Test de-escalation: tiny tasks should not trigger the full machine.

2. **Cross-machine learning loop**
   - Keep raw learning records local/private by default.
   - Share only sanitized learning packets through Git.
   - Periodically review shared packets and promote repeated/high-severity lessons into evals, validators, templates, or deletions.

3. **Real-project dogfooding**
   - Use the pack on several non-trivial coding/agentic-system tasks.
   - Record where it made work faster, where it slowed work down, and where it prevented tech debt.
   - Prefer removing or simplifying instructions that do not pay for themselves.

4. **Second-pass architecture review**
   - Re-review boundaries between `ubergoal`, `uberplan`, `uberaccept`, and `uberskillevolver`.
   - Check whether any duplicated wording should move to a shared reference or be deleted.
   - Confirm that the Agent Advocate and First-Principles Simplifier lanes are strong enough without becoming ceremony.

## Deferred modules

Do not build these until real usage proves benefit >> cost:

- `ubercode` — execution-wave orchestration.
- `ubergit` / `ubership` — commit, PR, release, and GitHub-management workflows.
- `ubereval` — dedicated eval design/execution workflow.
- `uberui` — UI/browser verification workflow.
- standalone specialist skills for Codebase Scout, Architecture Steward, Agent Advocate, Loophole Hunter, First-Principles Simplifier, Quality/Eval Strategist.

Default: keep specialist roles as lanes/templates inside `uberplan` and `uberaccept` until repeated use proves a standalone skill would reduce context/cost or prevent failures.

## Promotion criteria for new subskills

A deferred module may become a skill only when at least one is true:

- The same lane is used repeatedly across real projects and consumes enough context to justify extraction.
- A failure recurs because the lane was too hidden or too weak inside an existing skill.
- A deterministic script/validator/eval harness needs its own focused package.
- Splitting it makes the common path smaller and faster, not just more organized.

Every new subskill needs:

- a named failure class it prevents
- benefit >> cost argument
- example invocation/eval seed
- package lint/test coverage
- clear relationship to `ubergoal`
- deletion/retirement trigger

## Cross-machine learning policy

Use Git to combine learnings, but do not commit raw traces by default.

- Raw records: local/private, e.g. `~/.agentic-uber-learnings/<machine-id>/...`.
- Shared packets: sanitized, small, safe-to-commit Markdown under `learning/inbox/<machine-id>/...`.
- Promotion: periodic human-reviewed batches move repeated/high-value lessons into skill diffs, evals, validators, templates, or deletions.
- Archive: after promotion/rejection, move packets to `learning/processed/` or leave them referenced by the promotion batch.

No silent self-modification: shared learnings are evidence, not authority.
