# Failure-Eval Database

Schema version: v2.

This folder is the pack-layer failure-to-eval catalog. Process-canonical cases live in `evals/failures/cases/`. Runtime-canonical cases live in `agfunder-gaia/evals/failures/`; this layer may index or point to them but must not carry incident detail.

## Schema v2

Each case file uses YAML frontmatter plus a short Markdown body.

Required frontmatter fields:

- `id`: stable kebab-case case id.
- `date_observed`: `YYYY-MM-DD`.
- `layer`: `process`, `runtime`, or `both`.
- `canonical_layer`: `process` or `runtime`.
- `title`: short human title.
- `what_happened`: sanitized one-paragraph description.
- `failure_class`: reusable failure class.
- `cost`: sanitized cost statement.
- `gate_that_missed_it`: the missing or weak gate.
- `eval_check`: validator, fixture, checklist, or live proof location.
- `eval_type`: `executable`, `fixture`, `checklist`, or `live`.
- `plan_items`: one or more plan item ids.
- `status`: `seed`, `eval_built`, or `enforced`.

Optional fields such as `canonical_repo` are allowed only to make pointer files explicit. Pointer files must name the canonical repo path.

## Sanitization Rules

- Do not include named individuals.
- Do not include credentials, token values, private keys, cookie values, or secret material.
- Do not include message contents; summarize behavior instead.
- Do not include machine-specific `/Users/<name>/...` paths in `what_happened` unless parameterized, for example `${UBER_SKILLS_ROOT:-~/repos/agentic-uber-skills}`.
- Use `op://...` references for secrets when a reference is needed; never echo the value.
- Runtime-layer copies may carry more operational detail, but Git-pushed pack-layer copies stay sanitized.

Secret-value detection is delegated to `scripts/lint_pack_contract.py --secret-scan`; `validate_failure_case.py` only enforces lightweight case-shape and path-sanitization heuristics.

## P4 Completeness Rule

Every terminal failure path must require failure intake before the artifact validates. Current chokepoints are Uber run receipts, final acceptance reports, RCA artifacts, and the Gaia alert-RCA loop.

Use exactly one non-empty intake field:

```text
failure_case_id: <id>
case_updated: <id>
not_applicable_with_reason: <text>
```

Use `not_applicable_with_reason: no failure observed` only for happy-path artifacts where no new or updated failure case is warranted.

## Validation

Validate all pack-layer process cases:

```bash
python3 scripts/validate_failure_case.py evals/failures/cases/
```
