---
name: uber-skill-creator
description: Portable guide for creating, updating, migrating, deprecating, and evaluating Uber-style SKILL.md skills for Codex, Claude, and compatible coding agents. Use when users want to create a new general skill, update an existing skill, audit an existing skill or skill pack with a read-only quality report, migrate or purge legacy local skill-creator or skill-creator-pro aliases, add scripts/references/assets, run eval-driven skill iteration, compare with-skill vs without-skill behavior, generate an HTML review report, or tune a skill description for better triggering. For OpenClaw/Gaia/Type0/Soho-specific skills, prefer openclaw-agentic-skill-creator.
model: claude-opus-4-8
effort: max
metadata:
  short-description: Create or update an Uber skill
---

# Uber Skill Creator

Portable guide for creating effective `SKILL.md` packages for Codex, Claude, and compatible coding agents. This repo-local package is the canonical creator for `agentic-uber-skills`: runtime-neutral, eval-driven, and concise.

## Relationship to this pack

- Use `uber-skill-creator` to create, update, migrate, deprecate, install, validate, audit, and evaluate portable SKILL.md skills.
- Use `uberskillevolver` after substantial or surprising runs to capture lessons and decide which evidence-backed changes should be promoted into a skill.
- Treat local `skill-creator` or `skill-creator-pro` installs as legacy aliases. Redirect portable work here; redirect OpenClaw/Gaia/Type0/Soho-specific work to `openclaw-agentic-skill-creator`.
- Keep only a small deprecation shim for old aliases until removal is explicitly approved. Do not keep overlapping creator descriptions active.

## Choose the target profile first

| Target profile | Use when | Destination | Required extras |
|---|---|---|---|
| Portable Codex/Claude-compatible skill | Should work across coding agents with local SKILL.md folders | `$CODEX_HOME/skills/<skill>`, `~/.codex/skills/<skill>`, `~/.claude/skills/<skill>`, or runtime root | Strong trigger `description`, `agents/openai.yaml` when supported, `quick_validate.py`, lint/tests when present |
| Uber-family skill | Part of `agentic-uber-skills` | source repo plus installed Codex copy when needed | pack routing rules, pack contract tests, local lint/tests, Codex validation, `uberskillevolver` after real runs |
| OpenClaw/Gaia/Type0/Soho-specific skill | Depends on OpenClaw runtime, tenant policy, live source lanes, agent affordance, or local workspace conventions | use `openclaw-agentic-skill-creator` instead | preserve high agent affordance; name source/tool/context expectations; avoid hidden gates; verify with live-safe OpenClaw proof or record the gap |

## Core principles

- **Concise is Key.** The context window is a public good. Assume the agent is capable; add only non-obvious procedural/domain knowledge that earns its tokens.
- **Use progressive disclosure.** `SKILL.md` is the active control plane; scripts, references, and assets stay cold until needed. For detailed workflow/anatomy examples, read `references/skill-creation-workflow.md`.
- **Set degrees of freedom deliberately.** Use text instructions for judgment-heavy work, pseudocode/scripts for preferred patterns, and narrow scripts for fragile repeatable operations.
- **Protect validation integrity.** Subagents can forward-test behavior, but pass raw artifacts and realistic requests, not your diagnosis or expected answer.
- **Compress safely.** For existing skills or large plan artifacts, use `references/lossless-skill-compression-profile.md` and `scripts/estimate_lossless_compression.py`; preserve trigger phrases, validator labels, and safety gates unless tests intentionally change.

## Skill creation workflow

1. **Classify target profile.** Portable, Uber-family, or OpenClaw/Gaia/Type0/Soho-specific.
2. **Run the non-skill check.** Prefer a direct answer, note/doc, or small script when discoverable agent execution is not the real need.
3. **Collect concrete examples.** Ask only material trigger/non-trigger/resource questions. Stop once usage is clear.
4. **Plan reusable contents.** Choose `scripts/`, `references/`, and/or `assets/` only when they reduce repeated work, improve reliability, or keep active context small.
5. **Pick the maturity tier.** Use `Scaffold`, `Production`, `Library`, or `Governed`; each higher tier must earn its gates.
6. **Draft the production contract when needed.** For production/library/governed skills, read `references/production-skill-contract.md` and capture the owned job, trigger/non-trigger cases, resources, evals, risk boundary, owner/review cadence, and targets before adding adapters or release claims.
7. **Initialize when new.** Prefer `scripts/init_skill.py <skill-name> --path <output-directory> [--resources scripts,references,assets] [--examples]`; skip only for existing skills.
8. **Edit active instructions.** Write imperative guidance for another agent. Keep trigger information in frontmatter `description`; keep body focused on procedure and resource use.
9. **Validate.** Run `scripts/quick_validate.py <path/to/skill-folder>` plus package lint/tests when present.
10. **Fresh-install check when install/onboarding changed.** In a disposable environment, install from the documented instructions using no carried dependencies, credentials, or manual repairs. If a hidden assumption appears, fix the smallest setup/doc gap, discard the environment, and retry.
11. **Run the eval-driven extension** for reusable, high-impact, broadly installed, or behavior-changing skills.
12. **Install/sync/migrate.** Sync canonical source to runtime skill roots only after source validation passes.

Read `references/skill-creation-workflow.md` for command examples, anatomy, resource-selection details, and forward-testing prompts.

## Agents metadata

Create or update `agents/openai.yaml` for runtimes that expose skill chips/lists. Read `references/openai_yaml.md`, generate deterministic `display_name`, `short_description`, and `default_prompt`, and regenerate when SKILL.md changes materially.

## Evaluation Mode

Use Evaluation Mode when asked whether a skill or skill pack is production-grade, should be tightened, split, deleted, promoted, or tuned.

Run the read-only evaluator before recommending broad rewrites:

```bash
scripts/evaluate_skill_quality.py <skill-or-pack-path> --format markdown
scripts/evaluate_skill_quality.py <skill-or-pack-path> --format json --output skill-quality.json
```

The read-only evaluator checks trigger clarity, concision, progressive disclosure, verification evidence, side-effect policy, eval coverage, package shape, anti-shortcut guidance, and overlap. Treat the output as review evidence, not authority; do not mutate skills unless edits were explicitly approved.

## Eval-driven extension

Read `references/eval_driven_skill_creation.md` when the skill is reusable, high-impact, likely to be installed broadly, or likely to change agent behavior beyond simple validation. The extension adds intent examples, trigger/non-trigger prompts, realistic evals, with-skill vs without-skill comparison when feasible, qualitative review notes, an HTML review report via `scripts/generate_eval_report.py`, and trigger-description tuning with held-out examples.

For prompt, policy, or skill-behavior tuning, keep a champion and challenge it deliberately: save the current version, working set, untouched holdouts, must-pass checks, budget, and promotion margin before editing. Promote a challenger only when it wins on fresh holdouts without weakening a must-pass check; keep the champion on uncertainty.

Keep this portable. Do not paste platform-specific slash commands, subprocess assumptions, or proprietary runtime conventions into a general skill; translate useful methods into neutral SKILL.md terms and record provenance in notice/reference notes.

### Refactor failure-patched prose

When a skill has accumulated long corrective paragraphs after failures, rewrite
them before adding more prose. Prefer `Trigger / Do / Fallback / Invalid`:

- **Trigger:** observable condition that activates the rule.
- **Do:** required action, output field, trace, or receipt.
- **Fallback:** only acceptable blocked/degraded path.
- **Invalid:** missing evidence, vague blockers, or lower-affordance shortcuts.

Keep the invariant and required evidence. Delete human-debugging history. Move
rationale to a reference/session log unless one short "why" line materially
changes behavior. Preserve source-authority/receipt requirements and keep an eval
or example proving the compressed wording still prevents the failure.

## Legacy alias migration

Use this path when the user mentions `skill-creator` or `skill-creator-pro`, asks whether either is deprecated, or wants to purge old creator skills.

1. Inventory old alias behavior and preserve only still-useful guidance.
2. Move durable portable guidance here or into a focused reference; move OpenClaw-specific guidance to `openclaw-agentic-skill-creator`.
3. Install/sync the canonical creator package.
4. Replace the old alias with a small deprecation shim; do not leave the old broad trigger active.
5. Validate the canonical skill and shim with `quick_validate.py`.
6. Use `uberskillevolver` to record migrated, deleted, protected, and deferred lessons.

## Forward-testing

Forward-test substantial skill revisions when practical. Fresh agents should receive the skill path and a realistic user-style task, for example: `Use $skill-x at /path/to/skill-x to solve problem y`. Do not ask them to review the skill, and do not leak expected answers. Review outputs, diffs, logs, and artifacts; if success depends on leaked context, tighten the skill or test setup before trusting it.
