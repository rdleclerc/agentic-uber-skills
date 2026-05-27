---
name: ubergoal
description: "Use when an agent needs the goal-owning lifecycle wrapper for substantial coding or agentic-system work: create or bind a Codex/platform goal by default when available, classify risk, route to uberplan for rigorous planning, run Tier 2+ specialist review-board agents when available, coordinate execution at the right tier, route to uberaccept for final proof, and route to uberskillevolver for post-run learning. Trigger for explicit goal/objective work, long plans, goal ledgers, multi-agent coding sessions, agentic-system changes, rigorous-multiagent-coding, the former monolithic ubergoal workflow, 100% confident strategy checks, final completion orchestration, or deciding which Uber subskill to use."
---

# Ubergoal

## Core rule

`ubergoal` is the **thin lifecycle wrapper**, goal owner, and bounded review-board coordinator for the Uber skill family. In runtimes with a platform goal object, explicit `ubergoal` use means create or bind that goal first, then route to focused subskills and specialist agents instead of carrying all planning and acceptance machinery itself.

Use the lightest tier that makes the work safe. Add process only when benefit is **clearly much greater than** total downstream cost.

## Routing table

| Need | Use |
|---|---|
| Rigorous planning, review-board lanes, codebase exploration, confidence gate | `$uberplan` |
| Execution coordination | main coding agent; Tier 2+ uses bounded specialist review-board agents/lenses when available |
| Final acceptance, policy-adherence, architecture drift, dead-code/test/eval proof, surprises | `$uberaccept` |
| Complexity/modularity/dead-code campaign | `$ubersimplify` |
| Source/research/internal-artifact assessment before adoption | `$uberassess` |
| Post-run learning for skills/prompts/workflows/agentic systems | `$uberskillevolver` |
| Repeated or material unexpected test failures | stop, run `$uberrca`, revise via `$uberplan`, append/merge child scope change, continue under same goal |
| Refactor campaign / HOT-file audit | load `references/refactor-campaign-profile.md` |
| `ubercampaign`, product campaign, multi-feature/feature-list/plan-tree campaign, “assess then plan then execute all items” | load `references/campaign-profile.md` |
| Tier 3 agentic/runtime/production-replacement expensive proof, burn-in, soak, canary expansion, or final proof | route to `$uberplan` with `templates/tier3-expensive-proof-plan-tree.md` and validator before launch |

Deferred until real usage proves benefit >> cost: `ubercode`, `ubergit`, `ubereval`, `uberui`, and standalone specialist-lane skills.

## Coding-agent work contract

For Tier 1+ coding, prompt, skill, workflow, or agentic-system implementation, use the Coding Agent Work Contract unless the task is tiny and deterministic:

- Guide: `/Users/claw1/agentic-architecture-guide/docs/coding-agent-work-contract.md`
- Template: `/Users/claw1/agentic-architecture-guide/.agentic/coding_agent_work_contract_template.md`

Tier 0 can use an inline note. Tier 1 uses the work contract unless risk requires `uberplan`. Tier 2/3 may extend it inside `uberplan`, but must avoid a duplicate objective/scope/evidence bureaucracy.

## Lifecycle

1. **Classify tier.** Choose the lowest safe Tier 0/1/2/3.
2. **Frame enough to make the goal non-vague.** Before creating a platform goal, do the minimum clarification needed to name the outcome, rough scope, non-goals, likely tier, and what “done” could mean. Preserve the operator original instruction, verbatim or by exact artifact path, before compressing it into a goal objective. For Tier 1+ or reviewer-involved work, record operator-original scope, agent-interpreted scope, proposed narrowed scope, explicit deferrals/non-goals, and approval evidence for any narrowing. This is not full planning and must not become implementation.
3. **Create or bind the goal before robust planning/execution.** If no goal exists and the user explicitly invoked `ubergoal`, call `create_goal` once the compact objective is specific enough. The goal may explicitly be “produce a robust plan, then execute it after the acceptance gate”; this preserves `ubergoal`’s purpose of preventing shallow plans while avoiding vague goal launch.
4. **Plan.** Start Tier 1+ with a **user expectation / surprise assessment**. Use inline note, work contract, or `$uberplan` by tier/risk. Agentic-system plans bias toward thin deterministic harnesses around capable agents. Do not execute until the plan or work contract names verification and stop conditions.
5. **Review and execute.** Main agent owns integration. Explicit `ubergoal` authorizes bounded Tier 2+ specialist review-board agents/lenses unless the user says no/lightweight. Workers mutate files only with disjoint write scopes.
6. **Adapt on test failure.** Stop before or at **five consecutive failures** of the same command/family, or immediately for material unexpected test failures. Capture evidence, run `$uberrca`, revise with `$uberplan`, append/merge scope expansion/correction/blocker, update ledger/receipt, continue under same goal.
7. **Ledger/receipt.** For long work, maintain `templates/goal-ledger.md` and the **Uber run receipt** in `templates/uber-run-receipt.md`, including the **Skills invoked summary**.
8. **Assess/simplify/accept/learn.** Route source due diligence to `$uberassess`; complexity campaigns to `$ubersimplify`; final proof to `$uberaccept`; Tier 2/3 skill/prompt/workflow/agentic lessons to `$uberskillevolver`.

## Tier selection

| Tier | Use for | Wrapper behavior |
|---|---|---|
| Tier 0 | Small isolated deterministic edits | smallest goal if explicitly invoked in a goal-capable runtime; otherwise short plan/tests |
| Tier 1 | Long but contained work | create/bind goal, light `$uberplan` or work contract, optional ledger, `$uberaccept` |
| Tier 2 | Medium/high-risk work where solo coding may miss context, dirty state, or acceptance | create/bind goal, audited plan, 2-3 specialist review-board agents/lenses by default, evidence rubric, `$uberaccept`, optional learning |
| Tier 3 | Cross-repo, agentic-system, production/runtime, major refactor/deletion, prompt/skill/eval, concurrency/security, complex UI | full `$uberplan`, batched board/workers when useful, audits, `$uberaccept`, `$uberskillevolver` |

If uncertain, choose the lower tier unless concrete risk requires escalation.

## Implementation effort recommendation

| Effort | Use when | Avoid when |
|---|---|---|
| `medium` | Tier 0/1, localized deterministic patches, clear tests, low ambiguity | architecture reset, agentic-system change, unresolved RCA |
| `high` | Tier 1/2 with judgment, repo navigation, user-visible behavior, non-trivial tests/evals, uncertainty | tiny deterministic work |
| `xhigh` | Tier 3, cross-repo/runtime impact, prompt/skill/eval changes, major refactor/deletion, concurrency/security/privacy, repeated hidden-assumption failures | when a smaller `medium`/`high` slice preserves safety/progress |

Before recommending `xhigh`, run the deletion-first pass: can the task be split while preserving the spine?

## Goal ownership

`ubergoal` is a superset of the platform goal primitive. The platform goal is the durable execution spine; the wrapper adds tiering, routing, subskills, agents, acceptance, and learning.

When launching, keep the objective compact: destination, objective/scope, operator-original scope reference, non-goals, tier, plan path/summary, expectation/surprise risks, preserve constraints, verification gates, allowed subagent/audit shape, done/stop conditions, approval boundaries, operational outcome contract, per-child terminal states, and success metric. The platform goal is not the entire plan; it is the durable North Star that survives the robust `$uberplan` phase and later execution. Validate objective text with `scripts/validate_goal_objective.py --target-chars 3400 --strict-target`. Do not set a token budget unless the user explicitly gives one.

## Execution coordination

Treat subagent/session limits as hard policy. In Codex, prefer the configured/reportable `[agents]` limits. Standard campaign preset is `max_threads=6`, `max_depth=2`: L0 root orchestrator → L1 workstream orchestrator → L2 worker/reviewer. If a campaign appears to need L0→L1→L2→L3, prompt before temporary deep-campaign mode (`max_threads=8`, `max_depth=3`), record approval, and restore `6/2` afterward unless the user says to keep it. `10/3` needs separate explicit approval. Never silently raise thread/depth limits or confuse plan depth with spawned-agent depth.

Tier 2 is valuable because it changes the decision shape: the orchestrator receives independent specialist context, not just more solo thinking. For Tier 2, launch 2-3 bounded review lanes when supported. Default lanes: Codebase/State Scout, Architecture/Contract Steward, and Quality/Eval/Hygiene Auditor. Choose fewer only when risk is narrower.

Review-board agents inspect, challenge, and recommend; they do not mutate unless assigned disjoint worker scope. Keep write sets disjoint, do not delegate the immediate critical-path blocker, require evidence-backed outputs, serialize overlapping work, update `templates/goal-ledger.md`, and stop/replan after repeated or material unexpected failures. Ask before destructive/external side effects unless already approved.

## Operational parent/child execution

For multiple plans or an `uberplan` plan tree, execute the root index/status-ledger/child-file layout and keep a child-by-child ledger. Each child records runtime topology, intended outcome, proof/blocker/re-scope evidence, remaining gap, and terminal state: `operational`, `blocked`, or `re_scoped_with_approval`. Recurse for subplans. Do not merge children into one shared proof layer; safe proof spines, registries, readiness gates, plans, local proofs, or shadow-only proofs do not complete children unless explicitly scoped as final outcome.

For production/runtime implementation goals, split blocked children into `active_blocked` and `hard_blocked_after_safe_action_exhaustion`. If a blocked child has runnable safe next actions, keep the parent active and continue safe autonomous predecessor work. Parent completion is allowed only when every required child is operational, user-rescoped with approval, or hard-blocked after safe-action exhaustion, with active blocked count = 0 and runnable safe next action count = 0.

For Tier 3 expensive-proof/replacement/runtime proof campaigns, do not proceed from one flat plan into burn-in or final proof. Require the `uberplan` expensive-proof preflight validator, child/status-ledger structure, and burn-in vs final-proof separation, or a recorded user-approved flat-plan bypass.

## Completion rule

Do not call `update_goal(status="complete")` until `$uberaccept` says the objective is achieved, no required work remains, policy-adherence has been checked against the plan and OpenClaw/agentic architecture, expected-vs-actual surprise has been checked, tradeoffs/surprises are reported, and every touched repo is committed, reverted, intentionally stashed, or explicitly approved as uncommitted.

For Tier 2/3, use specialist review-board agents/lenses for the final policy check when available; no solo self-certification. Final handoff must include `git status --short --branch`, Skills invoked summary, and a validated Uber run receipt when feasible. For “100% confident,” mean scoped confidence after trying to disprove the work and finding no material unresolved blocker.

## Optional Claude adversary

Use this only when the user explicitly asks for Claude review, e.g. `with Claude`, `Claude review`, `Claude debate`, or `Claude for 2 rounds`. Do not invoke Claude from task similarity or ordinary `ubergoal` use. Codex remains goal owner and reconciler; Claude is an adversarial reviewer, not a co-author, final authority, or acceptance substitute. If available, read `../references/claude-adversary.md`; keep the essentials here because references may not auto-load.

Default to one Claude challenge round; run two or three only when requested or when material unresolved risk remains. Each Claude challenge must name a claim, causal layer, why it matters, falsifying/satisfying evidence, and minimum impact threshold. If more than one challenge is raised, the first two challenges must use distinct causal layers; a single-challenge round must say why only one challenge is material. Codex reconciliation must classify each challenge as `Accepted`, `Risk added`, `Rejected`, `Uncertain`, or `No material impact`; `No material impact` is non-evidence: it proves a review ran, not that the artifact is acceptable. Bind the ledger to the artifact version/section reviewed.

Before the skill-specific questions, include the Scope Fidelity Packet from `../references/claude-adversary.md` and require the reviewer to answer `Original-scope satisfaction`, `Narrowing approval`, and `Scope fidelity verdict` against the operator-original instruction. A reviewer must not assess only Codex's summary or proposed scope. Also require Claude to challenge whether Codex is sticking to the operator-approved plan and preserving modularity, thin harness / fat skills/tools, and agentic affordance unless the user explicitly overrides those defaults.

For `ubergoal`, ask exactly:

1. **Load-bearing goal?** Causal layer: scope/ownership. Is this goal actually load-bearing, or a routing artifact? Evidence: name what execution decision changes because the goal exists. Minimum impact: delete/narrow the goal or name the decision it controls.
2. **Skip test.** Causal layer: deletion-first. What is lost if we skip the goal wrapper and execute directly? Evidence: list the lost safety/evidence boundary or admit none. Minimum impact: downgrade to ordinary task or add the missing boundary.
3. **Testable decomposition.** Causal layer: operational evidence. Does this decompose into three or fewer testable sub-outcomes? Evidence: name each sub-outcome and proof. Minimum impact: split/re-scope if not testable.

## Helpful resources

- `templates/goal-ledger.md` — compact long-running state.
- `templates/uber-run-receipt.md` — final skill/evidence receipt.
- `references/goal-objective.md` — compact objective guidance.
- `references/refactor-campaign-profile.md` — reusable refactor campaign profile.
- `references/campaign-profile.md` — `ubercampaign` multi-item assessment → plan-tree → execution profile.
- `scripts/validate_goal_objective.py`, `scripts/validate_uber_run_receipt.py` — deterministic checks.
