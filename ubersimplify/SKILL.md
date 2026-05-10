---
name: ubersimplify
description: Direct-use only when explicitly named or routed by ubergoal. Use when an agent needs to aggressively but safely reduce codebase complexity, over-abstraction, dead code, duplicated policy, poor modularity, silent fallbacks, brittle hidden behavior, or agentic-system bloat. Trigger for simplification campaigns, complexity audits, modularity audits, dead-code cleanup, first-principles deletion/refactoring, fail-fast boundary design, timestamped simplification trails, audit/plan/patch modes, or requests for Elon-style simplification with strong tests and rollback proof.
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

Before deleting or refactoring, pass these gates:

- **Burden-of-proof gate** — what cost does this complexity impose and what failure does it prevent?
- **Chesterton gate** — why was it probably added, and is that reason gone or handled elsewhere?
- **Modularity gate** — would better boundaries, single source of truth, or stronger contracts reduce conceptual complexity?
- **Fail-fast gate** — should a shared dependency/contract make violations loud instead of allowing silent drift?
- **Evidence gate** — tests/evals/static checks/characterization prove behavior is preserved or intentionally changed.
- **Dead-code safeguard** — dynamic imports, CLI entrypoints, framework routes, configs, migrations, prompts, tools, and external references are checked before deletion.
- **Rollback gate** — patch is small, reversible, and has a clear backout plan.
- **Agent Advocate / human-counterfactual gate** — for agentic-system complexity, ask whether a capable human with the same goal, context, and tools would have made the error; if not, fix missing context, bad tool feedback, conflicting source authority, or weak affordances before adding/removing compensating complexity.

## Modularity stance

Good modularity simplifies by reducing concepts, eliminating duplicate truths, clarifying ownership, and enforcing invariants. A central dependency can be better when it is narrow, well-tested, observable, and fails loudly.

Bad modularity is theater: wrapper chains, god modules, vague helpers, premature abstraction, or splitting cohesive code just to create files.

## Test-confidence policy

| Confidence | Allowed action |
|---|---|
| strong | patch/delete allowed with acceptance |
| medium | add characterization tests first, then patch only after the touched slice reaches strong-enough local confidence |
| weak | audit/plan only; never delete/refactor production behavior on weak evidence |
| unknown | no deletion; discover tests/references first |

Passing weak tests is not proof. If evidence is weak, create candidates and proof requirements rather than deleting. User risk acceptance may permit audit notes, reversible non-semantic cleanup, or an explicitly quarantined spike, but not deletion/refactoring of production behavior.

## Parallel simplification

When subagents are explicitly authorized, split by codebase slice or responsibility. Each simplifier must leave a trail section with key files, suspected complexity, proof needed, and no-change/defer rationale. Do not run multiple agents over the same files unless they use distinct lenses.

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
- `references/dead-code-safeguards.md` — false-positive traps.
- `references/modularity-principles.md` — good vs bad modularity.
- `references/test-confidence.md` — evidence levels.
- `references/agentic-simplification.md` — agent-specific complexity and affordances.
- `scripts/new_simplify_run.py` — create a timestamped trail.
- `scripts/validate_simplify_report.py` — validate final report evidence.
- `scripts/lint_skill_package.py` — package hygiene.
