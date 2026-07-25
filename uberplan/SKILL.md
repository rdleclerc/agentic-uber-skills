---
name: uberplan
description: Do not auto-trigger from task similarity. Use only when explicitly named by the user or routed by ubergoal. Produces the smallest source-grounded implementation plan that completely addresses the evidenced problem, with proportional proof and evidence-gated escalation.
---

# Uberplan

## Purpose

Measure three times, cut once. Use planning effort to understand the real problem, current ownership, change boundary, and failure proof before proposing work. The result is the smallest **complete** plan supported by the evidence, not the smallest-looking patch and not the largest process that the task category permits.

`uberplan` plans; it does not implement or accept completion. Route a substantial long-running goal through the owning workflow and final proof through `uberaccept`.

## The planning loop

Follow this order.

### 1. Understand the requested outcome

Run a short **Task Understanding Review**:

- What is the real problem the operator wants solved?
- Which requirements are clear?
- What is ambiguous, underspecified, or most likely to misunderstand?
- What is the execution plan, what is explicitly out of scope, and what evidence will prove this worked?

This is a misunderstanding-prevention step, not an output checklist.

**Decision-changing ambiguity gate:** resolve uncertainty from repository evidence when possible. Ask the operator only when the answer would materially change behavior, ownership, side effects, acceptance, write scope, or architecture. If a required authority is unavailable, return a bounded evidence-acquisition step; do not fill the gap with a guessed design.

### 2. Read the decisive sources

Before selecting a solution, read:

1. the governing instruction, contract, issue, or incident;
2. the current owner of the behavior or state;
3. the direct caller, consumer, or integration boundary affected;
4. the focused test, trace, or observable proof.

Read source bodies, not only filenames, summaries, or search snippets. Start with this minimum evidence set, then widen only when it leaves a decision-changing conflict or gap. Do not inventory the repository first. Archived proposals, old plans, broad history, and unrelated architecture are not evidence unless active sources conflict or provenance is the decision.

Stop source reading when all four questions have evidence-backed answers:

- What behavior is wrong or missing?
- Which current component owns it—or, for explicitly new behavior, which active
  contract defines the owner to create?
- What is the minimum complete change surface?
- What focused evidence would fail before the change and pass after it?

If one remains unknown, enter **terminal evidence-gap mode** and stop planning. Output only the decision that is blocked, the missing authority or evidence, one bounded acquisition or non-mutating falsification step, and the exact evidence that would unblock planning. Do not outline downstream implementation, tests, rollout, files, or conditional task maps while the owner or causal boundary is guessed.

The expected absence of a component in an explicitly new feature is not by
itself an evidence gap. When an active contract establishes that component's
responsibilities and boundaries, plan the smallest new owner and keep concrete
integration bindings as named evidence gates. Stop only when the missing
evidence could materially change ownership, the safety contract, or the change
surface—not merely because those bounded integrations have not been selected.

### 3. Choose the smallest complete change

Apply the Lazy Senior Dev ladder:

1. Can the requirement be narrowed, deleted, or satisfied by current behavior?
2. Does an existing owner, helper, dependency, platform primitive, skill, or
   tool already cover it?
3. Can the change remain one line, one function, or one file?
4. What additional layer is strictly necessary to prevent the evidenced
   failure or produce an honest terminal state?

Do not confuse implementation minimality with causal incompleteness. If one incident proves two independent failed contracts, the plan must repair both. Conversely, a severe consequence strengthens validation and rollout proof; it does not by itself justify new services, abstractions, agents, or artifacts.

Prefer one linear path and one independently valuable checkpoint. Branches are allowed only when a named unresolved fact genuinely changes the implementation; record the fact and its decision gate instead of scheduling both branches.

### 4. Attach proportional proof

Every plan names checkable acceptance criteria and the closest proof that would catch the failure:

- the pre-change failure or baseline;
- the focused unit, contract, integration, or black-box check;
- trust-boundary, data-loss, security, source-authority, or irreversible-action cases when implicated;
- exact-diff review for contained changes;
- runtime or user-visible readback only when runtime behavior is in scope.

For behavior changes, keep a compact **Red/green proof ledger**: baseline, expected red, first green, black-box or user-visible proof when applicable, false-green risk, and skipped layers with reasons. Test count is not proof quality. Do not create a harness, eval framework, canary program, or review board unless a named failure mode cannot be tested safely with existing means.

### 5. Delete planning theater and return

Before presenting the plan, run an over-orchestration deletion review: remove every slice, file, abstraction, reviewer, template, and operator step that does not change the decision or mitigate a named risk. Mark useful-but-untriggered work as evidence-contingent rather than scheduling it.

Compare the final plan with the **operator original instruction**: agent-interpreted scope, proposed narrowed scope, explicit deferrals/non-goals, and approval evidence for any material narrowing. Include a compact **User expectation / surprise assessment** and report **Scope fidelity: pass/fail/uncertain**. Do not let a polished plan hide an unapproved scope reduction.

## Output shape

Default to a concise inline plan:

1. decision and why;
2. decisive evidence and any remaining gap;
3. smallest linear implementation steps;
4. acceptance/proof;
5. explicit non-goals and escalation triggers.

Use these ceilings unless the operator requests more detail or a material requirement would otherwise be hidden: about 200 words for terminal evidence-gap mode, 350 for a contained plan, and 750 for a genuine cross-boundary plan. Reuse evidence already read; do not reopen sources solely to collect line numbers, repeat citations, or reformat the answer.

For a contained change, this may be a **Micro-intent / spec-first fast path**: 2-3 sentences of scope / intent, acceptance criteria, out-of-scope note, and a verification command or evidence note. A spec review catches missing requirements; code review catches implementation defects.

Create a durable `.md` plan only when the operator requests it or execution is long-running, multi-owner, resumable, or needs a handoff. Do not create a coordination tree merely because `uberplan` is active. Use `templates/plan-tier1.md` only for a durable contained plan and `templates/plan-tier3.md` only after the Tier 3 evidence gate below passes. Do not read either template for an inline plan.

## Evidence-gated riders

These are protections, not keyword triggers. The presence of words such as retry, scheduled, queue, worker, production, destructive, prompt, skill, or agentic does not activate them. Load a rider only when current evidence establishes its condition.

### Tier selection

- **Tier 0/1:** one established owner and a contained change. Use a micro-intent or short linear plan. Consequence can strengthen proof without changing tier.
- **Tier 2:** multiple real ownership seams, a meaningful migration, or a material approval/security/runtime risk that cannot be closed locally. Add only the most relevant review lens.
- **Tier 3:** evidence proves a cross-repo or production replacement, irreversible migration, concurrency/durability redesign, broad agentic behavior change, or another change whose safe proof genuinely needs the full contract. Prompt/skill/eval work is not automatically Tier 3.

Choose the lower tier unless a concrete risk requires escalation.

### Architecture stepback

For Tier 2/3 work, route to `$uberarchitect` only when evidence shows that a local fix cannot close a cross-boundary concurrency, queue, worker, backpressure, durability, gateway, orchestration, scaling, or repeated-timeout contract. The required **Architecture stepback / measure-three-times review** names the system class, current mismatch, viable avenues, blockers, second-order implications, pitfalls, smallest transition, proof, and what not to build. This is **Architecture focus, not uberengineering**: use extra thinking time/tokens to see the architecture and the terrain before cutting, not to make the plan bigger. If the bigger-picture review only adds ceremony, delete it; the point is to avoid blindly closing on the first plausible route.

For new agentic behavior, a new harness, or a new coordination layer, require a Gall's Law / Basic Spine First review before implementation. Name the smallest working end-to-end spine and its current proof. This does not auto-invoke Claude by task similarity. Locally polished micro-feature progress is not a substitute for a basic working spine.

### Loop Engineering Contract

Read `../references/loop-engineering.md` only when the plan changes or creates the loop itself: trigger/cadence, discovery, isolation, durable state, verification, stop/no-progress rule, budgets, idempotency, human gates, attention policy, or learning path. For a new unattended loop, account for every Loop Contract field or mark it inapplicable with a reason; learning means human-reviewed promotion of recurring failures into focused evals or fixtures, never loop self-modification. A contained defect inside an existing scheduled, recurring, event-triggered, or queue-driven owner does not activate the rider.

### Operational and hierarchical work

Use a **Definition of Done / Operational Outcome Contract** when work changes runtime state, external side effects, deployment, or multi-owner completion. Load `../references/operational-states.md` only when terminal-state or parent/child semantics are actually in scope.

Use **Recursive / Hierarchical Execution Pseudocode** and `references/plan-tree-artifact-layout.md` only when independently completable child plans reduce risk. For Tier 3 replacement or expensive production proof, use `templates/tier3-expensive-proof-plan-tree.md` and `scripts/validate_plan_contract.py`; do not apply them to a flat contained change.

### Review and execution lanes

For Tier 2/3, choose the smallest independent lens that challenges the named risk. A same-agent pass is a useful internal lens but not independent evidence. Do not create a full review board by default.

If subagents are authorized, split exploration, implementation, verification, and detail work into non-overlapping slices with digest-only receipts. The Root orchestrator keeps scope/decomposition/integration/acceptance. No plan should spawn duplicate agents over the same context.

If repeated test attempts hit **five consecutive clear failures** in the same family, or one material unexpected failure changes the model of the problem, stop and run RCA. Use a focused **child/sub-`uberplan` appendix** only for **RCA-driven scope expansion**.

Rare riders stay evidence-gated: use an **Agent Advocate** and **human counterfactual** for proven agent-affordance failures; the **Agent execution proof ladder** for a real cross-runtime agentic change; and a **First-Principles** lens, premortem, or **confidence gate** only when its benefit >> cost. When evidence proves agentic behavior, a model-output boundary, or an external side effect is in scope, read `references/agentic-architecture-checklist.md` and apply only the relevant protections: component classification; adaptive-policy versus deterministic-harness ownership; typed tools, permissions, approvals, and idempotency; checkpoints and replay; source/memory/context authority; and positive/negative evals. At a model/tool boundary, state what the model may decide and what the deterministic harness must validate and execute. Runtime topology defaults such as `max_threads=6` and `max_depth=2` come from `../references/operational-states.md` only when that rider is active.

## Final value check

For Tier 0/1, perform this check directly. For Tier 2/3, use one fresh-context
reviewer when available:

- **Strictly necessary now:** omission leaves an explicit requirement or named
  failure unaddressed.
- **Evidence-contingent:** remove from initial work and record its trigger.
- **Cautious theater:** delete it.

The plan passes only if it is the smallest linear plan that preserves the complete operational outcome and its proof. Keep trust-boundary validation, data-loss protection, security, source authority, irreversible-action gates, and explicit operator requirements.

## Optional Claude adversary

Contract: `../references/claude-adversary.md` (opt-in only on explicit request; reconciliation + frame-independence rules there).

Ask exactly:

1. **Most likely execution failure.** What evidence predicts it, and what
   smallest plan change prevents it?
2. **Missing affordance.** Which required skill, tool, source, or context is
   absent or unproven?
3. **Overengineering / code-bloat failure.** Which proposed mechanism can be
   deleted, merged, or deferred?
4. **Linear 80/50 alternative.** Can a linear version deliver most of the value
   with half the surface?
