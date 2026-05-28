---
name: uberskillevolver
description: Do not auto-trigger from task similarity. Use only when explicitly named by the user or routed by ubergoal. Captures a lightweight, human-reviewed learning loop for skills, prompts, workflows, multi-agent coding protocols, or agentic-system playbooks after substantial or surprising runs.
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



## Regression lessons from scope-fidelity failures

Promote severe scope-drift failures when an agent narrows, reframes, or defers the operator's original instruction and a second reviewer approves the narrowed frame because it saw only the agent's summary. The smallest durable fix should be a Scope Fidelity Packet, template field, reviewer prompt requirement, or regression fixture that forces comparison against the operator original instruction, verbatim. Do not solve this with a hidden semantic judge, persistent debate harness, or broad reviewer bureaucracy.

A useful scope-fidelity learning record names: operator original instruction, agent-interpreted scope, proposed narrowed scope, explicit deferrals/non-goals, approval evidence, diff between original and proposed scope, reviewer scope-fidelity verdict, and what would have blocked the mistaken sign-off.

For frame-adhesion failures, promote the smallest rule that makes a reviewer stand outside Codex's roleplay before approval: operator original instruction first, invited role named, original-vs-summary gap named, three reject conditions stated, and a reduced-noise caveat that model review cannot replace direct human spot-checks or observable success criteria. Prefer skill text, template fields, or eval fixtures; do not add a hidden debate controller.

## Regression lessons from completion-claim failures

Promote severe completion-claim failures into evals, templates, validators, or examples when they can recur. In particular, treat this as a high-value regression class: a parent `ubergoal` claims all child plans complete because a shared safe proof spine, readiness gate, registry, local proof, or shadow-only proof passed, while one or more child plans have not reached their intended operational outcome.

Also promote production/runtime implementation goal failures where a parent closes because every child has a status, but one or more `blocked` children still have runnable safe next actions. The expected fix class is an active-vs-hard blocker invariant: `active_blocked` remains active work, while `hard_blocked_after_safe_action_exhaustion` requires safe predecessor exhaustion and an exact external/unsafe/irreversible blocker.

When the failure is semantic safe-work exhaustion rather than only missing fields, prefer a visible `uberaccept` adversarial review over a hidden deterministic judge: list blocked children, enumerate plausible safe next actions, and block completion if any remain runnable.

If the failure involved one giant plan file causing shallow inner-loop treatment, consider promoting `uberplan`'s Plan Tree Artifact Layout: root index, child files, status ledger, receipts, and final acceptance.

If the failure involved Tier 3 agentic/runtime/replacement expensive proof, burn-in, soak, canary expansion, or final-proof burn, promote a scoped preflight template/validator/eval when it can catch the next shallow flat-plan launch. Require risk/failure inventory, observability/telemetry, phase-boundary contract-fuzz, burn-in/final separation, stop/replan rules, and child/status ledger unless a human-approved bypass is recorded.

The smallest durable fix should usually be a plan/acceptance template field, mechanical validator, or negative fixture. Do not solve this by adding a hidden runtime controller or semantic judge inside the skill package.

## Runtime topology lessons

For campaign/subagent runs, record whether the configured depth/thread budget matched the work shape. Preserve the distinction between plan depth and spawned-agent depth. Promote a lesson only when evidence shows the default `max_threads=6`, `max_depth=2` or explicit deep-campaign `8/3` escalation caused or prevented a real failure. Never promote a silent thread/depth increase; durable changes must keep approval, ledger, and restore rules visible.

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
