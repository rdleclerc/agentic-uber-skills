---
name: uberskillevolver
description: Use when an agent needs a lightweight side audit trail and human-reviewed learning loop for skills, prompts, workflows, multi-agent coding protocols, or agentic-system playbooks. Trigger after substantial Ubergoal Tier 2/3 runs, failed or surprising skill usage, repeated agent mistakes, requests for a self-evolving skill, post-run retrospectives, skill evolution ledgers, lesson promotion into evals/templates/validators, or preventing skill drift and prompt bloat.
---

# Uberskillevolver

## Core rule

Skills improve through **evidence, evals, validators, deletion, and human-reviewed diffs** — never through silent self-modification.

Use the smallest learning loop that captures real wins/mistakes and converts only high-value repeated lessons into durable skill changes. Treat accumulated lessons, memories, templates, and governance as complexity with maintenance cost. Promote a lesson only when the expected benefit is **clearly much greater than** the total downstream cost.

## When to use

Use this skill when:

- a Tier 2/3 `ubergoal` run changes a skill, prompt, workflow, agentic-system behavior, or multi-agent coding pattern
- a skill run fails, surprises us, or produces avoidable cost/complexity
- the user asks how a skill can learn, evolve, keep an audit trail, or improve from usage
- repeated agent errors suggest a prompt/tool/context/source-authority failure
- a proposed skill update needs a promotion gate: lesson → eval/template/validator/deletion → reviewed diff

Do **not** use this for tiny deterministic edits unless there was a notable failure or reusable lesson.

## Output contract

For a learning pass, produce:

1. learning-record path or inline record summary
2. candidate lessons with promote/defer/delete/no-change decisions
3. proposed durable changes, if any
4. required evals/validators before changing a skill
5. explicit anti-bloat verdict: why benefit >> cost, or why no change is better

## Storage policy

Default location for artifacts:

- Local/private raw records: `~/.agentic-uber-learnings/<machine-id>/<skill-name>/<YYYYMMDDTHHMMSS>-<run-slug>/`
- In a repo/workspace: `.uberlearn/<skill-name>/<YYYYMMDDTHHMMSS>-<run-slug>/` when local-only or gitignored.
- Cross-machine shared packets: `learning/inbox/<machine-id>/<YYYYMMDDTHHMMSS>-<run-slug>/post-run-learning.md` after sanitization.
- In OpenClaw sessions: `/Users/claw1/.openclaw/runtime/skill-evolution/<skill-name>/<YYYYMMDDTHHMMSS>-<run-slug>/`
- If the run already has a session archive, store there and link from the session log.

Do not store secrets, credentials, private customer data, full copyrighted source dumps, or unnecessary raw prompts/responses. Prefer links, file paths, hashes, excerpts, and summaries. Redact sensitive traces before persisting. For multi-machine use, commit only sanitized learning packets whose `Privacy and redaction` section says `Safe to commit? yes`.

## Learning loop

1. **Capture the run** using `templates/post-run-learning.md` or `scripts/new_learning_record.py`.
2. **Separate observations from lessons.** A surprising outcome is evidence, not yet a rule.
3. **Create lesson candidates** with `templates/lesson-candidate.md` only for actionable patterns.
4. **Run the promotion gate.** A candidate may become:
   - an eval seed or regression case
   - a validator/checklist item
   - a template change
   - a script/tool change
   - a deletion/simplification
   - documentation/reference routing
   - a deferred/no-change note
5. **Demand benefit >> cost.** One-off annoyances usually become notes, not permanent machinery.
6. **Patch only with authorization.** Apply skill changes only when the current task authorizes edits; otherwise produce a change plan.
7. **Validate.** Run quick validation, package lint, unit tests, and any behavior/eval checks relevant to the changed skill.
8. **Close the loop.** Record what changed, what was deliberately not changed, and what future run would falsify the decision.

## Promotion gate

Before changing a skill, answer:

- What concrete run evidence supports this lesson?
- Is it a repeated pattern or a severe one-off?
- What is the smallest durable change that prevents recurrence?
- Can we delete/simplify instead of adding instructions?
- Will this increase context load, checklist fatigue, coordination, false positives, or maintenance burden?
- What eval, validator, or example will catch regression?
- What would make us revert this change?

If evidence is weak or benefit is not clearly much greater than cost, defer or record `no change`.


## Cross-machine learning

When this skill pack is used on multiple machines, combine learnings through Git, not hidden memory. Keep raw records local/private. Share only sanitized packets in `learning/inbox/<machine-id>/...`, then periodically review the inbox and promote repeated/high-value lessons into skill changes, evals, validators, templates, or deletions.

Shared packets are evidence, not authority. They must still pass the promotion gate and human review. See `references/cross-machine-learning.md`.

## Agent Advocate lens

For agent mistakes, include the human counterfactual:

- Would a competent human with normal context/tools have made this mistake?
- If not, what context, affordance, feedback, source authority, memory, or approval boundary was missing?
- Did the plan patch symptoms instead of fixing the upstream invariant?

Promote fixes that improve the agent's operating environment: clearer source authority, better tool output, better context retrieval, stronger deterministic checks, or sharper handoffs.

## Relationship to Ubergoal

`ubergoal` manages planning/execution/acceptance for substantial work. `uberskillevolver` manages the **post-run learning loop** for improving skills and workflows after real usage.

For Tier 2/3 skill, prompt, workflow, or agentic-system runs, use `uberskillevolver` at final acceptance or after a notable failure to decide whether the experience should become a durable eval, validator, template change, or deletion.

## Helpful resources

- `templates/post-run-learning.md` — concise run retrospective and evidence ledger.
- `templates/lesson-candidate.md` — normalize one lesson before promotion.
- `templates/promotion-batch.md` — review a batch of candidates before editing a skill.
- `templates/skill-evolution-change-plan.md` — plan a specific skill update.
- `scripts/new_learning_record.py` — create a timestamped learning record from the template.
- `scripts/validate_learning_record.py` — validate required learning-record sections and evidence.
- `scripts/validate_promotion_batch.py` — validate promotion-batch review discipline.
- `scripts/lint_skill_package.py` — check this skill package for required files and policy hooks.
- `references/cross-machine-learning.md` — combine sanitized learning packets across machines.
