# Eval-Driven Skill Creation

Use this reference when a skill is reusable, high-impact, likely to be installed broadly, or likely to change agent behavior in ways that `quick_validate.py` cannot prove.

## Provenance

This workflow is portable across Codex, Claude, and SKILL.md-compatible agent runtimes. It adapts public skill-creation methodology from OpenAI's Codex skill-creator, Anthropic's public skill-creator workflow, and community skill-evaluation patterns. Do not copy proprietary or runtime-specific commands from another agent platform into skills. Translate useful methods into neutral SKILL.md terms and cite provenance in a `NOTICE.md` or reference note when material.

## Workflow

1. Capture intent examples.
   - Write 3-7 prompts that should trigger the skill.
   - Write 3-7 near-miss prompts that should not trigger it.
   - Include at least one realistic messy user prompt.

2. Draft eval prompts before hardening the skill.
   - Use prompts that resemble real user asks, not sterile unit-test names.
   - Include expected behavior, required artifacts, forbidden shortcuts, and acceptance evidence.
   - Save them under `evals/` when the skill owns them, or in the surrounding repo's eval fixture path when the repo owns them.

3. Compare with-skill vs without-skill when feasible.
   - With-skill: run a fresh agent or fresh context that can load the candidate skill.
   - Without-skill: run the same task without the skill, or record why a baseline is unsafe, too expensive, or not supported in the current runtime.
   - Keep raw prompts, outputs, relevant diffs, commands, and timing notes.

4. Review qualitatively before revising.
   - Look for missing trigger cases, over-triggering, hidden platform assumptions, bloated context, missing scripts, brittle examples, and untested output formats.
   - Record what changed because of evidence, not preference.

5. Use champion/challenger discipline for behavior tuning.
   - Preserve the current skill/prompt/configuration as the champion.
   - Tune challengers on the working set only.
   - Promote only if untouched holdouts improve by the preset margin and must-pass checks stay green.
   - Keep the champion when evidence is tied, stale, or ambiguous.

6. Fresh-install check when install or onboarding behavior changed.
   - Use a disposable environment and only the documented install/onboarding path.
   - Do not copy personal credentials, cached dependencies, or manual repairs into the test.
   - If a hidden setup assumption appears, fix the smallest doc/setup gap, discard the environment, and retry.

7. Generate a compact HTML review report.
   - Use `scripts/generate_eval_report.py` with a small JSON report.
   - The report is a review surface, not source authority. Keep the JSON or Markdown notes as the durable record.

8. Tune the description.
   - Put all trigger information in frontmatter `description`, not a "When to use" body section.
   - Use held-out trigger and non-trigger examples so the description does not overfit to the first eval set.
   - Prefer concrete contexts and file types over broad claims.

## Report JSON Shape

```json
{
  "skill_name": "example-skill",
  "iteration": "iteration-1",
  "summary": "What changed and why.",
  "cases": [
    {
      "id": "eval-1",
      "prompt": "Realistic user request",
      "expected": "Required behavior",
      "with_skill": "Observed result with skill",
      "without_skill": "Observed baseline or reason skipped",
      "verdict": "pass",
      "notes": "Evidence-backed notes"
    }
  ],
  "description_tuning": {
    "old": "old description",
    "new": "new description",
    "held_out_examples": ["near miss", "real trigger"]
  }
}
```

`verdict` should be `pass`, `partial`, `fail`, or `blocked`.
