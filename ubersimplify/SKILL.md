---
name: ubersimplify
description: Do not auto-trigger from task similarity. Use only when explicitly named by the user or routed by ubergoal. Audits or carefully patches codebase complexity, dead code, duplicated policy, poor modularity, silent fallbacks, brittle hidden behavior, or agentic-system bloat with proof gates.
---

# Ubersimplify

## Core rule

Complexity must justify itself, but deletion must earn proof. Be aggressive against accidental complexity and dead code; be conservative about hidden production history, dynamic references, weak tests, and agent affordances.

Default to **Audit mode**. Patch mode is conservative/experimental until repeated real-project dogfooding proves it prevents more debt than it creates. It is allowed only after explicit authorization, strong local evidence, rollback proof, and acceptance gates are satisfied.

## Modes

| Mode | Use for | Edits allowed? |
|---|---|---|
| Audit | map complexity, modularity, dead code, tests, risks | no |
| Plan | rank candidates and define proof requirements | no |
| Patch | small reversible simplification batches | yes, only with explicit authorization and strong evidence; medium evidence must first be upgraded with characterization tests |

## Output contract

For persistent simplification campaigns, create or update a timestamped trail with the items below. If the user explicitly asks for a read-only/no-artifacts audit, do **not** write files; produce the same sections inline and propose a trail path for later.

1. scope, target slice, mode, and non-goals
2. baseline tests/evals/static checks before changes
3. complexity inventory with burden-of-proof notes
4. modularity/boundary audit
5. dead-code/dynamic-reference audit
6. test-confidence classification
7. ranked candidates: delete, merge, inline, centralize, fail-fast, defer, or no-change
8. patch log and rollback plan if edits occur
9. final simplification report with evidence and residual risks
10. `uberskillevolver` learning recommendation for notable lessons

Use `scripts/new_simplify_run.py` to create the trail when artifacts are authorized.

## Required gates

Before deleting or refactoring, apply `references/gates.md`: Basic Spine First veto, burden-of-proof, Chesterton, Modularity gate, Fail-fast gate, evidence, dead-code safeguard, rollback, and Agent Advocate / human-counterfactual gate. Do not patch when any gate lacks evidence.

## Modularity stance

Good modularity reduces concepts, duplicate truths, ambiguous ownership, and hidden invariants. Use `references/modularity-principles.md` for centralization vs split examples and `uber-skill-creator`'s lossless compression profile for skill/plan compression.

## Test-confidence policy

Use `references/test-confidence.md`. Strong evidence can support accepted patch/delete work; medium evidence needs characterization tests first; weak or unknown evidence stays Audit/Plan only. Passing weak tests is not proof.

## Parallel simplification

When subagents are explicitly authorized, split by codebase slice or responsibility and require each simplifier to leave key files, suspected complexity, proof needed, and no-change/defer rationale in the trail. Avoid overlapping file ownership unless the lenses are distinct.

## Relationship to Uber family

- Use `ubergoal` when the user asks for a broader lifecycle decision; if simplification was invoked directly, stay in this skill unless planning/acceptance/learning handoff is needed.
- Use `uberplan` for broad project planning before major simplification.
- Use `ubersimplify` for complexity/modularity/dead-code audit and safe simplification trails.
- Use `uberaccept` before accepting simplification patches.
- Use `uberskillevolver` after notable runs to promote lessons into evals, validators, templates, or deletions.

## Helpful resources

- `templates/simplify-plan.md` — scope/mode/non-goals.
- `templates/complexity-inventory.md` — complexity burden map.
- `templates/modularity-audit.md` — boundaries, contracts, fail-fast opportunities.
- `templates/dead-code-audit.md` — unused/dynamic/external reference checks.
- `templates/test-confidence.md` — proof strength classification.
- `templates/simplification-candidates.md` — candidate ranking table.
- `templates/patch-log.md` — reversible patch sequence.
- `templates/final-simplification-report.md` — acceptance-ready final report.
- `references/gates.md` — required gates before deletion or refactor.
- `references/dead-code-safeguards.md` — false-positive traps.
- `references/modularity-principles.md` — good vs bad modularity.
- `references/test-confidence.md` — evidence levels.
- `references/agentic-simplification.md` — agent-specific complexity and affordances.
- `scripts/new_simplify_run.py` — create a timestamped trail.
- `scripts/validate_simplify_report.py` — validate final report evidence.
- `scripts/lint_skill_package.py` — package hygiene.
