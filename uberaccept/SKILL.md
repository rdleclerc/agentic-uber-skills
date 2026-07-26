---
name: uberaccept
description: Do not auto-trigger from task similarity. Use only when explicitly named by the user or routed by ubergoal. Performs proportional adversarial acceptance against the exact approved scope, candidate diff, and risk-mapped proof before completion or ship claims.
---

# Uberaccept

## Core rule

Try to prove the candidate is not ready. Accept only the exact claim whose
material requirements are proved. Expand proof with evidenced risk, not with a
universal checklist. Unit green, polished prose, or a validator cannot stand in
for required black-box, integration, runtime, or user-visible evidence.

`uberaccept` owns the terminal acceptance decision. It does not plan or repair
the work. Use `$uberplan` for changed implementation contracts, `$ubergoal` for
bounded execution, and `$uberskillevolver` for post-run learning.

## Authority and inputs

Read the operator request and exact approved plan or micro-intent, candidate
diff/touched files, evidence receipts, and relevant repository contract. Record
their path and revision or digest when available.

Scope fidelity compares the operator original instruction, agent-interpreted scope, proposed narrowed scope, explicit deferrals/non-goals, and approval evidence. Unapproved narrowing or expansion blocks acceptance.

- The plan defines intended scope; the diff defines actual implementation;
  evidence proves claims. None may silently redefine another.
- Use `UNKNOWN` or `not provided` for an absent input. Never reconstruct missing
  state from summaries, fixtures, source-adjacent data, or a green local test.
- Preserve an authoritative upstream terminal decision and its evidence id.
  Missing or unknown status is not `rejected`.
- Material edits make earlier diff review stale; same-agent review can be recorded as a lens but must not count as independent evidence.
- When independent review is required, record reviewer identity/model/runtime and `independent_review: true/false`.

## Decision contract

Return exactly one `acceptance_status`:

- `accepted` — every material requirement for the scoped claim is proved, or a
  named residual gap has exact operator approval.
- `fix_within_scope` — a bounded defect or missing proof is already authorized
  by the approved plan and can be corrected without changing scope or authority.
- `replan` — evidence changes the implementation contract, causal repair set,
  architecture, or proof strategy without requiring a new product decision.
- `user_decision` — proceeding requires approval for product scope, public
  behavior, ownership, dependency, irreversible tradeoff, acceptance, or an
  external action.
- `blocked_with_failure_intake` — a required gate cannot currently run or an
  external/environmental barrier prevents acceptance. Name safe next actions
  and file or update the failure case.
- `rejected` — preserve an authoritative terminal rejection, or reject a
  candidate whose evidenced contradiction cannot honestly be represented by
  one of the repair/replan/decision states above.

Do not convert missing, malformed, or unknown status into `rejected`. Do not
average a blocker away. Only `accepted` authorizes completion or ship language.

## Acceptance kernel

1. Echo the exact claim, tier, approved scope, and explicit non-goals.
2. Compare plan to diff on two axes: spec fidelity and repo/architecture fitness.
   Either can block acceptance.
3. Map each material requirement to exact diff and proof. Mark it `proved`,
   `weak`, `missing`, or `contradicted`.
4. Identify the concrete false-green risk for each activated risk: what could
   still fail despite the evidence shown?
5. Apply only the riders triggered by the plan, diff, claim, or repository
   contract. Check repository-mandatory gates even when the plan omitted them.
6. Return the typed decision, material blocker or residual, and smallest safe
   next action. Never edit the implementation during acceptance.

Require a meaningful red-before/green-after result when it is practical and
diagnostic. Do not manufacture a red phase, broad suite, extra reviewer, or
artifact merely to fill a field. Tests must map to a concrete failure mode.

### Acceptance-criteria verification

Check every material criterion; block completion on any `fail`. A partial or
residual result needs exact operator approval. Keep spec/intent fidelity
separate from code and repository standards.

## Risk-activated riders

Activate a rider only when its trigger is present; record trigger, required
proof, observed proof, false-green risk, and verdict.

- **Black-box/UI/user-visible behavior:** exercise the actual boundary and, for
  UI, rendered interaction and relevant accessibility behavior.
- **Operational/live/adopted claim:** prove target wiring and authoritative
  target-system or user-visible readback. A registry, scaffold, shadow result,
  or local proof supports only that lower claim.
- **External action/security/privacy:** require exact target, authorization,
  boundary negatives, idempotency, rollback, execution receipt, and
  authoritative readback. Planning never grants execution authority.
- **Concurrency/retries/loops:** require race and duplicate-suppression proof,
  durable replay, correct stop, budgets/kill switches, per-iteration receipts,
  and independent verification as applicable; read
  `../references/loop-engineering.md`.
- **Agentic or multi-agent failure:** verify the minimum complete causal repair
  set, upstream contract, human counterfactual, and behavior eval. Do not accept
  one repaired layer when another material user-visible failure remains.
- **System-scale architecture:** require a `$uberarchitect` Architecture Stepback Packet for
  concurrency, queue/worker, gateway, orchestration, durability, backpressure,
  repeated-timeout, or symptom-patching claims. Local timeout/config patches do
  not prove the system class fixed.
- **Product/rewrite/agentic-system spine:** locally polished micro-feature success that did not advance the basic working spine is a soft rejection signal. Reject a complex top-down harness unless the approved scope explicitly makes a non-readiness spike the final outcome.
- **Tier 3/runtime/replacement:** retain the stated tier; require plan review,
  exact-diff review, independent adversarial review, security negatives,
  telemetry preflight, rollback rehearsal, authorized canary, authoritative
  runtime readback, and final acceptance as activated by the plan.
- **Multi-child or plan tree:** inspect authoritative child states and receipts.
  Parent completion requires every required child operational,
  re-scoped-with-approval, or hard-blocked after safe work is exhausted.
- **Repository topology/dependencies:** run the relevant boundary checks and
  distinguish unrelated known failures from candidate-caused failures.

### Loop acceptance lens

For an activated loop rider, use per-iteration receipts and independent
verification rather than maker-only self-review. Require durable replay,
correct-stop proof, idempotency, and budget/time/retry kill-switches.

## Output

Default to a compact decision receipt:

1. `acceptance_status`
2. exact claim and inputs read
3. material requirement-to-evidence findings
4. activated riders and false-green risks
5. blocker/residual and smallest safe next action
6. scoped confidence and completion recommendation

Produce a durable report only when requested or when Tier 3, multi-child,
long-running, resumable, or handoff work needs it. In that case use
`templates/final-acceptance.md`, complete the core and activated rider sections,
mark inactive template sections with one concise not-applicable reason, and
validate with `scripts/validate_acceptance_report.py`. Failure intake is
mandatory only for `blocked_with_failure_intake`, using the grammar in
`evals/failures/README.md`.

Report `git status --short --branch` for each touched repository when accepting
code work. A dirty state is acceptable only when it is exactly the reviewed
candidate or the operator explicitly approved it.

## Completion and learning

Call `update_goal(status="complete")` only after `accepted` and only when no
required work remains. All other statuses remain non-complete.

For Tier 2/3 skill, prompt, workflow, multi-agent protocol, or agentic-system
changes, route the observed lesson and eval evidence to `$uberskillevolver`.
Never silently self-modify the skill.

## Optional Claude adversary

Contract: `../references/claude-adversary.md` (opt-in only on explicit request; reconciliation + frame-independence rules there).

Ask:

1. **Receipt reproducibility.** Are receipts deterministic tool output or model summaries?
2. **Scope/diff match.** Does the exact diff match the approved scope?
3. **Inherited assumption.** What could the next task inherit incorrectly?

Then answer: **Ship: yes/no, one sentence.**

## Helpful resources

- `templates/final-acceptance.md`
- `templates/architecture-steward-report.md`
- `templates/first-principles-simplifier-report.md`
- `templates/agent-failure-rca.md`
- `references/agentic-architecture-checklist.md`
- `../references/operational-states.md`
- `../references/loop-engineering.md`
- `../references/claude-adversary.md`
