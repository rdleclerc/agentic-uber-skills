---
name: uberplan
description: Do not auto-trigger from task similarity. Use only when explicitly named by the user or routed by ubergoal. Plans substantial coding, refactoring, UI, prompt/skill/workflow, or agentic-system work as a long-running goal plan with thread highlights, a durable .md file, operational outcome/Definition of Done contract, recursive pseudocode for hierarchical plan trees, proof ladders, review lanes, topology seams, and confidence gates.
---

# Uberplan

## Core rule

Create the smallest **long-running goal** plan that makes the work safe. Planning has cost: add lanes, subagents, templates, evals, or harness only when **benefit >> cost**.

`uberplan` owns planning only. It does not execute patches or accept completion; route final proof to `uberaccept` and post-run lessons to `uberskillevolver`. Do not collapse substantial work into a default 20-minute slice unless the user explicitly asks for a slice.

If a Coding Agent Work Contract already captures objective, scope, orientation, evidence, stop conditions, and gaps, use or extend it. Do not create duplicate bureaucracy.

## Basic Spine First gate

For product/rewrite/agentic-system work, first name the minimum user-visible product spine, the canonical command/live-safe check that proves it, and current result: `pass`, `fail`, or `not available`. If it is not green, plan only to create/fix that spine or explicitly scope a non-readiness spike. Do not add architecture, agents, routers, monitors, or eval frameworks until the spine is green or the user accepts the spike.

For Type0, the default spine is: real feed/tip/wire input → normalized signal → admission decision → lane/story assignment → story processing → fact-check/publish/reject guard → traceable result.

## Operational outcome contract

Tier 1+ plans must include a **Definition of Done / Operational Outcome Contract** naming intended outcome, what counts as implemented/operational, evidence, non-implementation examples, and terminal state.

Allowed terminal states:

- `operational` — implemented, wired into the intended real/target system, tested/evaled, and supported by live or target-system proof unless the plan explicitly scoped a local proof artifact as final outcome.
- `blocked` — exact blocker, evidence, next unblock action, and owner/prerequisite recorded.
- `re_scoped_with_approval` — user approved the smaller target before completion; original outcome remains visible as deferred/not done.

Readiness gates, safe adoption spines, registries, plans, eval fixtures, local proofs, or shadow-only proofs are not implementation unless the contract explicitly names that artifact as final outcome.

## Recursive / hierarchical execution pseudocode

For multi-plan goals, subplans, plan-making plans, or “execute all plans,” include **Recursive / Hierarchical Execution Pseudocode**. It must show child iteration, recursion, proof before parent return, child terminal-state recording, and rejection of superficial completion. Parent/shared proof cannot substitute for child operational completion.

For large plan trees, use `references/plan-tree-artifact-layout.md`: root `index.md`, child plan files, `status-ledger.md`, receipts, and final acceptance. Bound recursion; create child plans only when they reduce risk or separate operational outcomes.

For production/runtime implementation goals, especially long unattended goals, include an upfront approval packet and safe-predecessor decomposition before external/unsafe/irreversible stop points. A blocked child with runnable safe next actions is `active_blocked` and remains active work; only `hard_blocked_after_safe_action_exhaustion` can count toward parent completion, and only with evidence that safe autonomous predecessor work is exhausted.

For Tier 3 agentic/runtime/production-replacement or other expensive-proof work, load `templates/tier3-expensive-proof-plan-tree.md` and run `scripts/validate_plan_contract.py`. A single flat plan must not launch burn-in/final proof unless the plan records an explicit flat-plan exception, approval, and validator-bypass reason.

## Agent execution proof ladder

For OpenClaw or agentic-system plans, the **Agent execution proof ladder** is strategy, not a final wish:

1. Prove a Codex subagent with the intended skills/tools/source/context can execute the activity.
2. If it fails, improve skill/tool/context affordances before adding orchestration.
3. Prove the same activity through OpenClaw or target runtime.
4. Do not call ready until two target-runtime parity proofs pass or the missing proof is a blocker/spike.

## Delivery format

Return thread highlights plus a durable `.md` plan path. Before showing either, run an over-orchestration deletion review for accidental slices, expectation mismatch, unnecessary agents/templates/files, duplicate artifacts, deterministic harness creep, regex/router semantic authority, and places where better skills/tools/context/source authority beat more process.

## Output contract

Use `templates/plan-contract.md` for the durable plan. It must cover, as applicable:

- goal posture, checkpoints, `.md` path, thread highlights, tier, objective, scope, assumptions, non-goals
- **User expectation / surprise assessment** and final handoff proof against material mismatch
- **Scope Fidelity Ledger**: operator original instruction, verbatim or exact artifact path; agent-interpreted scope; proposed narrowed scope; explicit deferrals/non-goals; approval evidence for narrowing; and diff between original and proposed scope
- **Gall's Law / Basic Spine First adversary** for agentic-system, harness, coordination-layer, or architecture-changing plans: smallest end-to-end working spine, not micro-feature slices or top-down architecture; evals that prove the spine works and stay green while it evolves
- Definition of Done / Operational Outcome Contract, allowed terminal state, and non-implementation examples
- Recursive / Hierarchical Execution Pseudocode plus Plan Tree Artifact Layout for child/subplans
- Unattended production/runtime approval and safe-predecessor plan when production/runtime work could hit external/unsafe/irreversible steps
- Tier 3 expensive-proof plan-tree preflight for agentic/runtime/production-replacement, burn-in, soak, canary expansion, or final-proof work
- checkable PRD checklist, task map, stable IDs, owners, dependencies, done conditions, Mermaid graph, and parallelization/write-scope policy
- testing adaptation gate: stop before or at **five consecutive clear failures** of the same command/failure family, or immediately for material unexpected failures; run RCA; if scope changes, create a focused **child/sub-`uberplan` appendix**, merge/append it as **RCA-driven scope expansion**, correction, or blocker, then continue only after new hypothesis/evidence gate is named
- affected repos/files, protected-file constraints, codebase exploration trails, architecture options, and repository topology/package-seam plan for new/moved/reorganized code
- code-health/dead-code tool plan for Tier 2/3 work, refactors, deletions, new modules, and package moves; tool findings are candidates, not deletion authority
- deterministic harness responsibilities vs adaptive model policy; for agentic systems, thin harness / fat agent rubric and source-convention check
- source authority, side effects, approval, rollback, adoption-state policy, risk-to-evidence map, acceptance rubric, and decision/surprise register
- pre-presentation over-orchestration review, plan acceptance gate, and **confidence gate** verdict after trying to falsify the plan

## Tier selection

| Tier | Use for | Planning machinery |
|---|---|---|
| Tier 0 | Small isolated deterministic edits | concise plan/test note |
| Tier 1 | Long but contained work | plan contract + loophole/simplifier check |
| Tier 2 | Medium/high-risk work | Architecture Steward plus most relevant extra lane |
| Tier 3 | Cross-repo, agentic-system, runtime/prod, major refactor/deletion, prompt/skill/eval, concurrency/security, complex UI | full review board, evidence rubric, optional subagents only when authorized |

Choose the lower tier unless a concrete risk requires escalation.

## Planning review lanes

Choose lanes by risk, not ceremony: Architecture Steward; **Agent Advocate / Agent Failure RCA** with **human counterfactual**; Loophole Hunter / Red Team; **First-Principles** Simplifier / Complexity Auditor; Codebase Scout; OpenClaw / Platform Steward; Quality/Eval Strategist; Cost/Risk Governor. Use `templates/planning-review-board.md` only when synthesis must be durable.

## Parallel exploration and execution planning

Map the critical path before parallel work. If subagents are authorized, split exploration into non-overlapping slices and require trails: key files, invariants, commands/tests, unknowns, false leads, next angles. Even without subagents, identify parallelizable work, serial blockers, disjoint write scopes, and batching/max-concurrency policy. Do not spawn duplicate agents over the same context.

## Runtime thread caps

Treat subagent/session limits as hard platform policy. In Codex, read configured/reportable `[agents]` limits when available. Standard campaign preset is `max_threads=6`, `max_depth=2` for L0 root → L1 workstream → L2 worker/reviewer. If a plan needs L0→L1→L2→L3, require an explicit deep-campaign prompt before temporary `max_threads=8`, `max_depth=3`; `10/3` requires separate approval. Record approval, restore target, queued/skipped/cap-hit lanes, and never count failed/unavailable/queued lanes as evidence.

## Repository topology and code health

For new, moved, or meaningfully reorganized code, propose target file tree before implementation, name package/module destination, separate public seams from private implementation, state tests/evals location, and name the repo-local topology/dependency gate. Avoid root dumps, helper piles, mixed-concern folders, and orphan generated artifacts.

For Tier 2/3, refactors, deletions, new modules, or package moves, name repo-local checks first, then language tools such as `vulture`, `ruff`, `pyright`/`mypy`, `pytest`, `knip`, `ts-prune`, `depcheck`, `eslint`, `tsc`, `git grep`, topology tests, import-boundary checks, generated-artifact audits, and dynamic-reference review. Deletion still needs Chesterton/dynamic-reference/rollback proof.

## Agentic system planning bias

Prefer thin harness / fat agent. Harness owns schemas, tool contracts, state, permissions, budgets, source authority, replay, traces, and evals. Agents own ambiguous intent, context selection, tool choice, decomposition, recovery, synthesis, and judgment. Reject deterministic monolith drift: giant routers, regex/keyword semantic authority, broad blob files, hidden state bags, and tools that absorb agent policy.

## First-principles simplification

Before hardening the plan, ask what requirement, artifact, abstraction, process, or agent can be deleted; whether the outcome can be achieved by removing a moving part; whether benefit clearly exceeds implementation, maintenance, debugging, context, coordination, eval, latency, rollback, and operator-attention cost; and what direct experiment could disprove an expensive assumption. Use `templates/first-principles-simplifier-report.md` when durable.

## Agent Advocate / failure RCA

For agentic systems or fixes to agent mistakes, inspect what the agent experienced: traces, prompts, loaded context, tools/errors, state, memory, source conflicts, handoffs, retries, feedback, stop conditions, and authority. Ask the human counterfactual: would a competent human with normal context/tools have erred? If not, fix missing context, affordance, feedback, source authority, memory, handoff, approval boundary, or deterministic guard. Use `templates/agent-failure-rca.md`.

## Plan acceptance and confidence gates

Before implementation or launch, compare the plan against the operator-original instruction, not only the agent's summary. If the plan narrows scope, name the narrowing and require explicit operator approval or mark it as `re_scoped_with_approval`/deferred rather than done. Final plan review must include `Scope fidelity: pass/fail/uncertain`.

For plans that introduce new agentic behavior, new harness, new coordination layer, or meaningful architecture, require a Gall's Law / Basic Spine First review before implementation. This does not auto-invoke Claude by task similarity, but when Claude/second-review is in use the Gall's Law check is mandatory for these plans. Locally polished micro-feature progress is not a substitute for a basic working spine.

Before implementation or launch, try to reject the plan against OpenClaw/agentic architecture, thin-harness/fat-agent policy, topology, dead-code, source-authority, side effects, and evidence. Then run the scoped verdict from `templates/confidence-gate.md`; do not say “100% confident” while a material blocker remains.

## Optional Claude adversary

Use this only when the user explicitly asks for Claude review, e.g. `with Claude`, `Claude review`, `Claude debate`, or `Claude for 2 rounds`. Do not invoke Claude from task similarity or ordinary `uberplan` use. Codex remains plan owner and reconciler; Claude is an adversarial reviewer, not a co-author, final authority, or acceptance substitute. If available, read `../references/claude-adversary.md`; keep the essentials here because references may not auto-load.

Default to one Claude challenge round; run two or three only when requested or when material unresolved risk remains. Each Claude challenge must name a claim, causal layer, why it matters, falsifying/satisfying evidence, and minimum impact threshold. If more than one challenge is raised, the first two challenges must use distinct causal layers; a single-challenge round must say why only one challenge is material. Codex reconciliation must classify each challenge as `Accepted`, `Risk added`, `Rejected`, `Uncertain`, or `No material impact`; `No material impact` is non-evidence: it proves a review ran, not that the artifact is acceptable. Bind the ledger to the artifact version/section reviewed.

Before the skill-specific questions, include the Scope Fidelity Packet from `../references/claude-adversary.md` and require the reviewer to answer `Original-scope satisfaction`, `Narrowing approval`, and `Scope fidelity verdict` against the operator-original instruction. A reviewer must not assess only Codex's summary or proposed scope. Also require Claude to challenge whether Codex is sticking to the operator-approved plan and preserving modularity, thin harness / fat skills/tools, and agentic affordance unless the user explicitly overrides those defaults. For plan-phase review, require the Gall's Law / Basic Spine First adversary: think bigger about the ultimate goal and first principles, not bigger about architecture; identify the basic working spine, the thin/fat split, eval-driven evolution, what success is not, and the smallest next move.

Also include the Frame-independence / anti-roleplay check from `../references/claude-adversary.md`. The reviewer prompt must put the operator-original instruction first; if it is missing, Claude must stop and flag the review as invalid. Before any approval language, require Claude to state what role Codex is asking it to play and whether it accepts, modifies, or refuses that role; name what the operator's original instruction requires that Codex's summary might hide or narrow; and list three concrete reject conditions. Treat highly one-sided `Accepted`/`No material impact` ledgers as rubber-stamp warnings, not proof of quality. Model adversary review is reduced-noise, not zero-noise, and does not replace operator-defined observable success criteria, direct prompt/diff spot-checks, deterministic tests, evals, or receipts.

For `uberplan`, ask exactly:

1. **Most likely execution failure.** Causal layer: failure prediction. Name the single most likely execution failure and its mitigation, not just acknowledgment. Evidence: tie it to a prior failure/source constraint. Minimum impact: add a stop gate or remove the risky branch.
2. **Missing affordance.** Causal layer: agent affordance/tooling. What skill, tool, source, or context does this plan depend on that does not exist or is unproven? Evidence: identify the exact missing affordance. Minimum impact: add proof/fallback or remove dependency.
3. **Linear 80/50 alternative.** Causal layer: simplification. Is there a linear no-branch version that gets at least 80% of the value with at most 50% of the surface? Evidence: describe it. Minimum impact: replace the plan or justify complexity.

## Helpful resources

- `templates/plan-contract.md` — durable plan contract.
- `templates/tier3-expensive-proof-plan-tree.md` — required preflight for Tier 3 expensive-proof/replacement/runtime proofs.
- `templates/confidence-gate.md` — adversarial confidence gate.
- `templates/planning-review-board.md`, `templates/exploration-trail.md`, `templates/agent-failure-rca.md`, `templates/architecture-steward-report.md`, `templates/first-principles-simplifier-report.md`, `templates/agent-brief.md` — optional lane/worker artifacts.
- `references/tiering-and-rubric.md`, `references/agentic-architecture-checklist.md`, `references/plan-tree-artifact-layout.md` — tiering, architecture, and nested-plan layout.
- `scripts/validate_plan_contract.py` — deterministic plan sanity checks.
