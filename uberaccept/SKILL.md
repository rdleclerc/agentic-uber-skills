---
name: uberaccept
description: Do not auto-trigger from task similarity. Use only when explicitly named by the user or routed by ubergoal. Performs adversarial final acceptance for substantial coding, refactoring, UI, prompt/skill/workflow, or agentic-system work before completion, merge, commit, push, or ship claims.
---

# Uberaccept

## Core rule

Try to prove the work is **not** ready. Accept only when material blockers are gone, evidence matches the risks, and added complexity still has benefit **clearly much greater than** total cost.

`uberaccept` owns final proof in the Uber skill family. It does not write the initial plan; use `uberplan` for planning and `uberskillevolver` for post-run learning.


## Architecture stepback acceptance blocker

If the completed work claims to fix a system-scale concurrency, queue/worker, gateway, orchestration, workflow durability, backpressure, repeated-timeout, or symptom-patching failure, final acceptance must look for an `$uberarchitect` Architecture Stepback Packet or equivalent. Soft-reject completion when the evidence only proves local timeout/context/config patches and never answers the system class, normal industry architecture, current mismatch, smallest transition path, and proof gate.

## Basic Spine First acceptance blocker

For product/rewrite/agentic-system work, check the `uberplan` Gall's Law / Basic Spine First gate and `../references/claude-adversary.md`; locally polished micro-feature success that did not advance the basic working spine is a soft rejection signal, and a complex top-down harness without planned spine proof is not acceptable unless the user scoped that artifact/non-readiness spike as final.

## Red/green and black-box proof audit

For any plan, review, or acceptance claim, same-agent review can be recorded as a lens but must not count as independent evidence. Final acceptance must record reviewer identity/model/runtime, author identity/model/runtime, `independent_review: true/false`, round number, and whether material edits made earlier review stale.

For code, prompt, skill, workflow, UI, or agent-behavior changes, final acceptance must inspect a **red/green proof ledger**: baseline result before the change, expected red/failing fixture when applicable, first green proof, black-box or user-visible check, false-green risks, and skipped evidence layers. Unit tests or package validators alone do not prove operational readiness when the plan required integration, browser, eval, live-safe replay, or target-system evidence.

If the ledger is missing, stale, or maps green checks to the wrong risk, score the relevant evidence layer 0/1 and do not recommend completion unless the user explicitly accepts the residual gap. Do not create a standalone `ubertesting` skill as a shortcut for this final audit; route recurring lessons to `uberskillevolver` and keep future `ubereval` extraction behind the roadmap promotion gate.

## Loop acceptance lens
For recurring, scheduled, watch-and-fix, queue-driven, or unattended loops, read `../references/loop-engineering.md` and require per-iteration receipts, independent verification instead of maker-only self-review, correct-stop proof, durable replay, budget/time/retry kill-switches, idempotency, duplicate suppression, and human gates.

## Claim-language and operational outcome audit

Final acceptance must prevent claim blur. Check every use of: `implemented`, `operational`, `live`, `adopted`, `tested`, `ready`, `wired`, `proof-only`, `blocked`, and `shadow-only`.

If a report claims `implemented`, `operational`, `live`, or `adopted`, require evidence that the work reached the plan's Operational Outcome Contract: real/target-system wiring, appropriate tests/evals, and live or target-runtime proof unless the plan explicitly scoped a local artifact as the final outcome.

Reject completion when the evidence is only a readiness gate, safe adoption spine, registry, plan, eval fixture, local safe proof, shadow-only proof, or shared parent proof spine unless the plan explicitly named that as the final outcome; inspect `../references/operational-states.md` for child terminal states, active/hard blockers, safe-work exhaustion review, parent completion rules, and runtime topology including `max_threads`/`max_depth`.

If `uberplan` used a Plan Tree Artifact Layout, final acceptance must inspect the root index, status ledger, child receipts, and final acceptance receipt; a single parent summary is not sufficient proof.

For Tier 3 agentic/runtime/production-replacement expensive proofs, final acceptance must inspect the expensive-proof plan validator result, risk/failure inventory, observability/telemetry preflight, phase-boundary/contract-fuzz preflight, burn-in vs final-proof separation, stop/replan evidence, and child/status ledger. Reject flat-plan readiness unless the report names a recorded approval and validator-bypass reason.

## Acceptance-criteria verification

When a task used a micro-intent, work contract, PRD, ticket, or `uberplan` with acceptance criteria, final acceptance must verify each criterion explicitly:

- list every acceptance criterion
- mark `pass`, `fail`, or `partial`
- cite file paths, commands, artifacts, or a clear not-applicable reason
- block completion on any `fail`
- allow `partial` only with named residual risk and explicit user-accepted scope or follow-up owner

This is not a replacement for the Operational Outcome Contract. Acceptance criteria prove the stated intent was checked; the Operational Outcome Contract proves the final state being claimed. For AI-generated code, also check whether spec/intent review caught design and scope issues before code, and whether code review still covered repo conventions, naming, module seams, integration details, and maintainability.

For branches, PRs, or implemented work that originated from an issue, PRD, work contract, or explicit user request, keep two review axes separate:

- **Spec fidelity** — did the diff implement what the originating spec, PRD, issue, or operator instruction asked for, and did it avoid unapproved scope creep?
- **Repo standards** — did the diff follow documented project standards, naming, module seams, tests, and maintainability expectations?

Do not merge these into one generic review verdict. A change can satisfy the spec while violating standards, or follow standards while implementing the wrong behavior; either axis can block acceptance. If no spec source exists, state that explicitly and do not let standards-only review stand in for product correctness.

Final reports should include a compact requirement-to-evidence table. Valid statuses are `proved`, `weak`, `missing`, or `contradicted`. Treat `weak`, `missing`, and `contradicted` as explicit residual risk; completion is allowed only when the plan/user accepts that status or the row is fixed. Do not let one green command stand in for every requirement when it only proves a narrower layer.

## Scope fidelity verdict gate

Before any `SHIP`, completion, ready, or goal-complete language, final acceptance must include `## Scope fidelity verdict`. It must quote/link `coordination/<task-slug>/scope.md`, check the operator original instruction, agent-interpreted scope, proposed narrowed scope, explicit deferrals/non-goals, and approval evidence, answer whether implemented scope satisfies original scope, and block unapproved narrowing.

## Output contract

Produce a final acceptance report that names every relevant layer explicitly:

1. implementation summary and files changed
2. rubric scores with evidence and residual gaps
3. commands/artifacts proving unit, regression, integration, UI/browser, eval, security/privacy, concurrency/idempotency, architecture, repository-topology/dependency boundaries, dead-code, rollback, and observability layers as applicable
4. Acceptance-criteria verification: criterion-by-criterion pass/fail/partial evidence
5. Loop acceptance lens when recurring/watch-and-fix/scheduled/unattended work is claimed: per-iteration receipts, independent verification, correct-stop proof, durable state replay, no-progress/budget controls, idempotent side effects, and human gates
6. Requirement-to-evidence ledger: each material requirement marked proved/weak/missing/contradicted with evidence
7. Claim-state ledger: claim language, Operational Outcome Contract evidence, and child terminal states for multi-child goals
8. Production implementation blocker gate: active blockers vs hard blockers, runnable safe next actions, safe-predecessor exhaustion, and parent completion rule
9. Safe-work exhaustion adversarial review: blocked children inspected for plausible safe next actions before parent completion
10. Tier 3 expensive-proof acceptance when the work involved burn-in, soak, canary expansion, replacement proof, or final proof
11. planning-board reconciliation
12. user expectation / surprise delta: what the user likely expected, what was actually implemented, what changed, what may surprise them, and whether any mismatch needs explicit approval
13. scope fidelity verdict: quote/link `coordination/<task-slug>/scope.md`, compare original scope to implemented scope, cite approved narrowing, and block unapproved narrowing
14. Agent Advocate final check for agentic work or agent failures
15. Architecture Steward final check
16. first-principles simplification and cost/complexity verdict, including any Basic Spine First veto
17. adversarial acceptance check
18. post-run learning decision for skill/workflow/agentic-system changes
19. confidence verdict and completion recommendation

Use `templates/final-acceptance.md` and validate with `scripts/validate_acceptance_report.py` when producing durable artifacts.
Acceptance reports must include the mandatory failure-intake field; use the grammar in `evals/failures/README.md`.
`acceptance_status` values are `accepted`, `rejected`, and `blocked_with_failure_intake`; blocked reports must file or update a failure case with `failure_case_id:` or `case_updated:`.

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
- **Architecture Steward**: check implementation drift from plan, architecture-guide constraints, repository topology/package seams, source authority, harness/policy split, durable execution, adoption/rollback, budgets, and human approvals when relevant.
- **Agent Advocate**: for multi-agent/agent-error work, confirm the upstream reason the agent erred is fixed and answer the human counterfactual.
- **Black-box Tester / Quality-Eval audit**: map tests/evals/audits to risks and user-visible behavior, not to a generic checklist; call out false-green evidence explicitly.

## Completion rules

Only recommend completion when:

- no material blocker remains
- required evidence is present or explicitly accepted as a residual gap by the user
- red/green proof ledger and black-box/user-visible evidence match the plan's risk map where applicable; unit-green-only or validator-green-only claims are not enough for broader operational claims
- any claim of implemented/operational/live/adopted is backed by the plan's Operational Outcome Contract, not merely proof-only or shadow-only evidence
- repeated clear failures of the same test command/failure family did not exceed five attempts without an RCA, `uberplan` revision, and resumed `ubergoal` evidence
- expected-vs-actual user surprise was checked, and any material mismatch is either fixed or explicitly flagged for user approval
- scope fidelity was checked against the operator-original instruction, and any narrowed scope is either operator-approved, marked deferred/not done, or blocks completion
- product/rewrite/agentic-system spine proof is green, or the scope is explicitly limited to a spine-check fix/non-readiness spike accepted by the user
- any repo-local topology/dependency gate relevant to changed code files was run, or its absence is named as a blocker/gap
- score 0/1 rows are absent
- score 2 rows have named residual risks or clear not-applicable evidence
- rollback/adoption and external side effects are understood
- every touched repo is clean, locally committed with only claimed files, reverted, stashed with a descriptive name, or explicitly user-approved as uncommitted
- the final response/report includes `git status --short --branch` for every touched repo
- the final confidence verdict is yes within a stated scope

When running in Codex, call `update_goal(status="complete")` only when the objective is achieved and no required work remains, or the user explicitly accepts named residual gaps.

## Post-run learning

For Tier 2/3 skill, prompt, workflow, multi-agent protocol, or agentic-system changes, invoke or recommend `uberskillevolver` before final handoff. Capture what should become evals, validators, templates, deletions, or no change. Never allow silent self-modification.

## Optional Claude adversary

Contract: `../references/claude-adversary.md` (opt-in only on explicit request; reconciliation + frame-independence rules there).

For `uberaccept`, ask exactly:

1. **Receipt reproducibility.** Causal layer: evidence. Are receipts reproducible by deterministic tool output, or are they model summaries? Evidence: command/log/diff path. Minimum impact: rerun or downgrade evidence.
2. **Scope/diff match.** Causal layer: modularity/seams. Does the diff match stated scope? Name any out-of-scope change. Evidence: git diff/status. Minimum impact: revert, split, or explicitly re-scope.
3. **Inherited assumption.** Causal layer: future-agent collision. What assumption does the next task inherit that could be wrong? Evidence: named downstream dependency. Minimum impact: document/test/rollback or block acceptance.

Then answer the separate final gate: **Ship: yes/no, one sentence.** This ship gate is not one of the three Claude questions.

## Helpful resources

- `templates/final-acceptance.md` — full acceptance report.
- `templates/architecture-steward-report.md` — final architecture check.
- `templates/first-principles-simplifier-report.md` — simplification/cost report.
- `templates/agent-failure-rca.md` — agent RCA/human counterfactual.
- `references/agentic-architecture-checklist.md` — architecture checklist.
- `../references/loop-engineering.md` — loop-mode acceptance lens and anti-bloat trigger.
- `scripts/validate_acceptance_report.py` — final report sanity checks.
- `scripts/validate_architecture_steward_report.py` — architecture report checks.
