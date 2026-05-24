# Skill Creation Workflow Reference

Use this reference when creating, migrating, or deeply revising a portable SKILL.md package. Keep `SKILL.md` itself as the active control plane; this file carries tutorial detail.

## Skill anatomy

```
skill-name/
├── SKILL.md                 # required: YAML frontmatter + active instructions
├── agents/openai.yaml        # recommended UI/routing metadata
├── scripts/                  # deterministic helpers and validators
├── references/               # loaded only when needed
└── assets/                   # copied/used output resources, not context docs
```

`SKILL.md` frontmatter should include only allowed fields such as `name` and `description` unless the target runtime explicitly supports more. The description is the primary trigger surface, so put “when to use” details there, not in the body.

## Resource choices

- Use `scripts/` when the same code is repeatedly rewritten, deterministic reliability matters, or validation should run without loading prose into context.
- Use `references/` for schemas, policies, examples, long workflows, API docs, migration notes, and variant-specific details.
- Use `assets/` for files the agent copies or modifies as output: icons, templates, boilerplate projects, fonts, slide decks, document templates.
- Do not create package-local README/INSTALL/CHANGELOG clutter unless the runtime/package contract explicitly requires it.

## Progressive disclosure patterns

1. **High-level active guide + references:** `SKILL.md` gives the workflow and links to references for advanced cases.
2. **Domain/variant organization:** split references by domain or provider so agents load only the relevant file.
3. **Conditional detail:** active instructions say when to load deeper references, e.g. tracked changes, OOXML details, provider-specific deployment.

Avoid deep reference chains. Link reference files directly from `SKILL.md`. For reference files longer than about 100 lines, include a table of contents.

## Concrete-example discovery

Ask only questions that materially change the skill design. Good discovery prompts:

- What user requests should trigger this skill?
- What should not trigger it?
- What recurring code, schemas, files, or external tools are involved?
- Is this portable, Uber-family, or OpenClaw/Gaia/Type0/Soho-specific?
- Where should it be installed or sourced?

Translate examples into resources by asking what an agent would otherwise rediscover or rewrite every time.

## Initializing a skill

For a new portable skill, run:

```bash
scripts/init_skill.py <skill-name> --path <output-directory> [--resources scripts,references,assets] [--examples]
```

Common destinations:

```bash
scripts/init_skill.py my-skill --path "${CODEX_HOME:-$HOME/.codex}/skills"
scripts/init_skill.py my-skill --path "${CODEX_HOME:-$HOME/.codex}/skills" --resources scripts,references
scripts/init_skill.py my-skill --path ~/work/skills --resources scripts --examples
```

Generate or regenerate `agents/openai.yaml` by reading the skill and passing deterministic values:

```bash
scripts/generate_openai_yaml.py <path/to/skill-folder> --interface key=value
```

Use `references/openai_yaml.md` for field definitions. Only include optional metadata such as icon/brand color when explicitly provided or already present.

## Editing rules

- Write active instructions in imperative/infinitive form.
- Start with reusable resources, then make `SKILL.md` tell agents when/how to use them.
- Test new scripts by running them; representative tests are acceptable for families of similar helpers.
- Delete placeholder example files if `--examples` created them and they are not needed.
- Keep detailed examples in references/evals unless they are essential to trigger or safety behavior.

## Validation and iteration

Run:

```bash
scripts/quick_validate.py <path/to/skill-folder>
```

For package-quality review, run:

```bash
scripts/evaluate_skill_quality.py <skill-or-pack-path> --format markdown
scripts/evaluate_skill_quality.py <skill-or-pack-path> --format json --output skill-quality.json
```

Treat evaluator output as review evidence, not authority. Do not mutate skills in evaluation mode unless edits were explicitly approved.

Forward-test complex or high-impact skills with fresh agents when practical. Pass the raw skill path and a realistic user request; do not leak intended fixes, expected answers, or your prior diagnosis. If forward-testing succeeds only with leaked context, tighten the skill or test setup.

## Migration/deprecation pattern

1. Inventory old alias behavior.
2. Move durable portable guidance into `uber-skill-creator` or a focused reference.
3. Move OpenClaw/Gaia/Type0/Soho-specific guidance into `openclaw-agentic-skill-creator`.
4. Install/sync the canonical package.
5. Replace legacy aliases with small deprecation shims until removal is approved.
6. Record the promotion/deletion decision with `uberskillevolver`.
