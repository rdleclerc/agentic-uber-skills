---
name: uberaccept
description: Do not auto-trigger from task similarity. Use only when explicitly named by the user or routed by ubergoal. Performs adversarial final acceptance for substantial coding, refactoring, UI, prompt/skill/workflow, or agentic-system work before completion, merge, commit, push, or ship claims.
---

# Uberaccept

## Core rule

Try to prove the work is **not** ready. Accept only when material blockers are gone, evidence matches the risks, and added complexity still has benefit **clearly much greater than** total cost.

`uberaccept` owns final proof in the Uber skill family. It does not write the initial plan; use `uberplan` for planning and `uberskillevolver` for post-run learning.

## Basic Spine First acceptance blocker

For product/rewrite/agentic-system work, final acceptance must name the minimum user-visible product spine, the canonical command or live-safe check that proves it, and the current result. If the result is `fail` or `not available`, do not recommend readiness for added architecture, abstractions, agents, contracts, routers, monitors, or eval frameworks. The only acceptable completion scope is a spine-check fix/creation or an explicitly user-accepted non-readiness spike. Core spine gaps are blockers, not residual risks.

For Type0, default spine: real feed/tip/wire input → normalized signal → admission decision → lane/story assignment → story processing → fact-check/publish/reject guard → traceable result.

## Red/green and black-box proof audit

For code, prompt, skill, workflow, UI, or agent-behavior changes, final acceptance must inspect a **red/green proof ledger**: baseline result before the change, expected red/failing fixture when applicable, first green proof, black-box or user-visible check, false-green risks, and skipped evidence layers. Unit tests or package validators alone do not prove operational readiness when the plan required integration, browser, eval, live-safe replay, or target-system evidence.

If the ledger is missing, stale, or maps green checks to the wrong risk, score the relevant evidence layer 0/1 and do not recommend completion unless the user explicitly accepts the residual gap. Do not create a standalone `ubertesting` skill as a shortcut for this final audit; route recurring lessons to `uberskillevolver` and keep future `ubereval` extraction behind the roadmap promotion gate.

## Claim-language and operational outcome audit

Final acceptance must prevent claim blur. Check every use of: `implemented`, `operational`, `live`, `adopted`, `tested`, `ready`, `wired`, `proof-only`, `blocked`, and `shadow-only`.

If a report claims `implemented`, `operational`, `live`, or `adopted`, require evidence that the work reached the plan's Operational Outcome Contract: real/target-system wiring, appropriate tests/evals, and live or target-runtime proof unless the plan explicitly scoped a local artifact as the final outcome.

Reject completion when the evidence is only a readiness gate, safe adoption spine, registry, plan, eval fixture, local safe proof, shadow-only proof, or shared parent proof spine, unless the plan explicitly named that as the final outcome. For multi-child goals, require a child-by-child terminal-state table before parent completion.

For production/runtime implementation goals, reject parent completion when any child is `active_blocked` or has runnable safe next actions. Only count a blocked child as terminal when it is `hard_blocked_after_safe_action_exhaustion`: safe autonomous predecessor work is exhausted, the remaining stop point is exact/external/unsafe/irreversible, and the next unblock owner/action is recorded.

Also run a **Safe-work exhaustion adversarial review** for production/runtime implementation goals: list every blocked child, enumerate plausible safe next actions the agent could still perform, and block completion if any safe action remains runnable. This review is the semantic oversight layer; deterministic validators only enforce that the review is visible and internally consistent.

If `uberplan` used a Plan Tree Artifact Layout, final acceptance must inspect the root index, status ledger, child receipts, and final acceptance receipt; a single parent summary is not sufficient proof.

For Codex campaign/subagent work, final acceptance must inspect runtime topology: configured/reported `max_threads`, `max_depth`, role shape, depth-3 approval evidence, restore target/proof, and child-agent depth policy. Reject “operational campaign” claims that silently raised thread/depth limits or omit the topology ledger.

For Tier 3 agentic/runtime/production-replacement expensive proofs, final acceptance must inspect the expensive-proof plan validator result, risk/failure inventory, observability/telemetry preflight, phase-boundary/contract-fuzz preflight, burn-in vs final-proof separation, stop/replan evidence, and child/status ledger. Reject flat-plan readiness unless the report names a recorded approval and validator-bypass reason.

## Output contract

Produce a final acceptance report that names every relevant layer explicitly:

1. implementation summary and files changed
2. rubric scores with evidence and residual gaps
3. commands/artifacts proving unit, regression, integration, UI/browser, eval, security/privacy, concurrency/idempotency, architecture, repository-topology/dependency boundaries, dead-code, rollback, and observability layers as applicable
4. Claim-state ledger: claim language, Operational Outcome Contract evidence, and child terminal states for multi-child goals
5. Production implementation blocker gate: active blockers vs hard blockers, runnable safe next actions, safe-predecessor exhaustion, and parent completion rule
5a. Safe-work exhaustion adversarial review: blocked children inspected for plausible safe next actions before parent completion
4a. Tier 3 expensive-proof acceptance when the work involved burn-in, soak, canary expansion, replacement proof, or final proof
5. planning-board reconciliation
5. user expectation / surprise delta: what the user likely expected, what was actually implemented, what changed, what may surprise them, and whether any mismatch needs explicit approval
6. Agent Advocate final check for agentic work or agent failures
7. Architecture Steward final check
8. first-principles simplification and cost/complexity verdict, including any Basic Spine First veto
9. adversarial acceptance check
10. post-run learning decision for skill/workflow/agentic-system changes
11. confidence verdict and completion recommendation

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

## Helpful resources

- `templates/final-acceptance.md` — full acceptance report.
- `templates/architecture-steward-report.md` — final architecture check.
- `templates/first-principles-simplifier-report.md` — simplification/cost report.
- `templates/agent-failure-rca.md` — agent RCA/human counterfactual.
- `references/agentic-architecture-checklist.md` — architecture checklist.
- `scripts/validate_acceptance_report.py` — final report sanity checks.
- `scripts/validate_architecture_steward_report.py` — architecture report checks.
