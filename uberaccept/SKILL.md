---
name: uberaccept
description: Use when Codex needs rigorous final acceptance for substantial coding, refactoring, UI, prompt/skill/workflow, or agentic-system work. Trigger before claiming completion, updating a Codex goal complete, merging, committing, or shipping; for acceptance rubrics, adversarial acceptance, evidence audits, dead-code checks, architecture drift checks, Agent Advocate final checks, first-principles simplification, test/eval completeness, rollback/adoption proof, and “are you 100% confident this is done?” checks. Usually invoked by ubergoal after implementation.
---

# Uberaccept

## Core rule

Try to prove the work is **not** ready. Accept only when material blockers are gone, evidence matches the risks, and added complexity still has benefit **clearly much greater than** total cost.

`uberaccept` owns final proof in the Uber skill family. It does not write the initial plan; use `uberplan` for planning and `uberskillevolver` for post-run learning.

## Output contract

Produce a final acceptance report that names every relevant layer explicitly:

1. implementation summary and files changed
2. rubric scores with evidence and residual gaps
3. commands/artifacts proving unit, regression, integration, UI/browser, eval, security/privacy, concurrency/idempotency, architecture, dead-code, rollback, and observability layers as applicable
4. planning-board reconciliation
5. Agent Advocate final check for agentic work or agent failures
6. Architecture Steward final check
7. first-principles simplification and cost/complexity verdict
8. adversarial acceptance check
9. post-run learning decision for skill/workflow/agentic-system changes
10. confidence verdict and completion recommendation

Use `templates/final-acceptance.md` and validate with `scripts/validate_acceptance_report.py` when producing durable artifacts.

## Acceptance scoring

Use 0–3 scores:

- **0** = blocker
- **1** = weak/unresolved
- **2** = acceptable only with named residual risk or explicit not-applicable evidence
- **3** = strong evidence

Do not hide missing evidence behind generic “checks passed.” If a layer is not relevant, state why it is not applicable.

## Required final lenses

- **Adversarial acceptance**: actively look for reasons the work is not ready.
- **First-Principles Simplifier**: ask what can be deleted or simplified now that the implementation exists; block complexity without benefit >> cost.
- **Architecture Steward**: check implementation drift from plan, architecture-guide constraints, source authority, harness/policy split, durable execution, adoption/rollback, budgets, and human approvals when relevant.
- **Agent Advocate**: for multi-agent/agent-error work, confirm the upstream reason the agent erred is fixed and answer the human counterfactual.
- **Quality/Eval audit**: map tests/evals/audits to risks, not to a generic checklist.

## Completion rules

Only recommend completion when:

- no material blocker remains
- required evidence is present or explicitly accepted as a residual gap by the user
- score 0/1 rows are absent
- score 2 rows have named residual risks or clear not-applicable evidence
- rollback/adoption and external side effects are understood
- the final confidence verdict is yes within a stated scope

For Codex goals, call `update_goal(status="complete")` only when the objective is achieved and no required work remains, or the user explicitly accepts named residual gaps.

## Post-run learning

For Tier 2/3 skill, prompt, workflow, multi-agent protocol, or agentic-system changes, invoke or recommend `uberskillevolver` before final handoff. Capture what should become evals, validators, templates, deletions, or no change. Never allow silent self-modification.

## Helpful resources

- `templates/final-acceptance.md` — full acceptance report.
- `templates/architecture-steward-report.md` — final architecture check.
- `templates/first-principles-simplifier-report.md` — simplification/cost report.
- `templates/agent-failure-rca.md` — agent RCA/human counterfactual.
- `references/agentic-architecture-checklist.md` — architecture checklist.
- `scripts/validate_acceptance_report.py` — final report sanity checks.
- `scripts/validate_architecture_steward_report.py` — architecture report checks.
