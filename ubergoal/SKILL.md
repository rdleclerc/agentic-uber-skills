---
name: ubergoal
description: Use when Codex needs to turn substantial coding or agentic-system work into a lean plan, evidence rubric, optional Codex goal, and final acceptance proof. Trigger for long plans, cross-repo or architecture-sensitive changes, multi-agent systems, agentic-system behavior, prompts/skills/workflows/tools/context/memory, production/runtime risk, major refactors, UI flows needing browser verification, repeated agent errors, symptom patches, user requests for “100% confidence,” rigorous multi-agent coding, the former rigorous-multiagent-coding workflow, auditors, acceptance rubrics, root-cause analysis, or launching a plan as a Codex goal.
---

# Ubergoal

## Core rule

Use the lightest tier that makes the work safe. Do not turn every task into a bureaucracy.

Prefer the smallest deterministic guardrail that prevents a known or plausible failure class. Do not add agents, schemas, eval harnesses, or review layers unless their benefit beats the coordination and maintenance cost.

The workflow is:

1. Classify risk and choose Tier 0/1/2/3.
2. Build the smallest useful plan contract and risk-mapped acceptance rubric.
3. Run the planning review board lanes justified by the tier: Architecture Steward plus optional Agent Advocate, loophole, simplifier, codebase, platform, and quality/eval lenses.
4. Reconcile review-board findings into a revised plan.
5. Run an adversarial confidence gate.
6. Only when the user explicitly says to launch as a Codex goal, create a compact goal objective with evidence, stop conditions, and length validation before calling `create_goal`.
7. Execute with the minimum needed agents/audits for the tier.
8. Keep a goal ledger for long work.
9. Run final adversarial acceptance before `update_goal(status="complete")`.

“100% confident” means **100% confident within the stated scope after trying to disprove the plan/work and finding no material unresolved blocker**.

## Tier selection

| Tier | Use for | Machinery |
|---|---|---|
| Tier 0 Normal coding | Small isolated changes | No Codex goal, no subagents, concise plan/tests |
| Tier 1 Solo goal | Long but contained work | Plan contract, lean rubric, final acceptance gate; create a Codex goal only after explicit launch instruction |
| Tier 2 Audited goal | Medium/high-risk work | Architecture Steward plus 1-2 planning review lanes if useful, Agent Advocate when agent behavior/errors are involved, quality evidence ledger; create a Codex goal only after explicit launch instruction |
| Tier 3 Full multi-agent goal | Cross-repo, agentic-system, production/runtime, major refactor/deletion, prompt/skill/eval, concurrency/security, or complex UI work | Overseer/integrator, planning review board, disjoint worker write sets, architecture steward, Agent Advocate for multi-agent/agent-error work, quality/eval auditor, code-health auditor, UI verifier if relevant; create a Codex goal only after explicit launch instruction |

If uncertain between tiers, choose the lower tier unless a concrete risk requires the higher tier.

## Cost/complexity gate

Before escalating tier, spawning agents, adding validators, adding eval infrastructure, or creating new governance artifacts, answer:

- What failure does this prevent?
- Has that failure happened, or is it high-risk enough to justify the cost?
- Is there a smaller check, template line, focused test, or acceptance criterion that prevents it?
- What ongoing maintenance burden does the new machinery create?

If the benefit is not clear, keep the simpler plan and name the deferred machinery as a future option rather than implementing it now.

## When not to use

Do not use the full workflow for tiny deterministic edits where a short plan, focused patch, and direct test are enough. Do not create a Codex goal just because this skill is active. Do not spawn subagents unless the user explicitly authorizes subagents, delegation, or parallel agents in the current turn.

## Output contract

For planning, return the selected tier, activated/skipped review lanes, risk-to-evidence map, acceptance rubric, confidence verdict, and explicit launch recommendation. For execution, maintain a goal ledger only after explicit goal launch or when the user asks for a durable plan artifact. For acceptance, name every missing unit, integration, eval, browser, security/privacy, concurrency/idempotency, architecture, Agent Advocate, and dead-code layer rather than saying generic “checks passed.”

## Planning review board

For Tier 2/3, use review **lanes** before launch. A lane can be run by the main agent or by a separate subagent when the user explicitly authorized subagents/parallel work. Do not spawn agents merely to imitate an org chart.

Recommended lanes:

| Lane | Use when | Blocking authority | Output |
|---|---|---|---|
| Architecture Steward | Tier 2/3 or agentic-system behavior | Blocks on material architecture, guide, harness/policy, source authority, durable execution, or eval gaps | `architecture-steward-report.md` |
| Agent Advocate / Agent Failure RCA | Multi-agent systems, repeated agent errors, prompt/tool/context/memory changes, or any plan meant to fix an agent behavior | Blocks symptom patches until the plan explains why the agent made the error and what invariant/tool/context/eval prevents recurrence | `agent-failure-rca.md` |
| Loophole Hunter / Red Team | Any high-risk or “100% confidence” plan | Blocks on exploitable loopholes, hidden assumptions, unsafe side effects, missing tests, race/idempotency gaps | `planning-review-board.md` section |
| Simplifier / Elegance Reviewer | Plan feels complex, broad, expensive, or fragile | Blocks only when simpler path avoids material risk/cost | smaller-plan proposal and removed-scope list |
| Codebase Scout / Cartographer | Existing repo is unfamiliar or likely has patterns/tests to reuse | Blocks on plan ignorance of existing extension points, protected files, active claims, or test harness | codebase map with files/tests/patterns |
| OpenClaw / Platform Steward | Work touches OpenClaw, Type0, runtime, gateway, launchd, orchestration, sessions, skills, or machine ops | Blocks on local policy violations, protected-file risk, missing OpenClaw docs/context, live/runtime side effects | platform constraints and required preflight |
| Quality/Eval Strategist | Tests/evals/audits are nontrivial or judgment/model behavior changes | Blocks on weak risk-to-evidence mapping or missing real-world eval strategy | quality/eval matrix |
| Cost/Risk Governor | Tier 2/3 could be overkill or budget/cost risk exists | Blocks on unnecessary multi-agent scope, unbounded loops, missing stop conditions | tier/cost recommendation |

Default activation:

- Tier 0: no board. Main agent may do a brief self-check.
- Tier 1: main agent runs Loophole + Simplifier lenses inline.
- Tier 2: Architecture Steward plus the single most relevant extra lane; choose Agent Advocate when the issue is agent behavior or multi-agent design.
- Tier 3: Architecture Steward, Agent Advocate for multi-agent/agent-error work, Loophole Hunter, Simplifier, Codebase Scout, Quality/Eval Strategist, plus OpenClaw/Platform Steward when locally relevant.

The overseer/integrator must reconcile findings into one plan. Review lanes advise or block; they do not own the final plan.

## Agent Advocate / Agent Failure RCA

For multi-agent systems or any fix to an agent mistake, add an **Agent Advocate** lane before planning hardens. The advocate asks what the agent actually experienced, why the action looked reasonable from inside the harness, and which upstream invariant was missing. It must also run a **human counterfactual**: would a competent human in the same role, with normal context and tools, have made this error? If not, identify the missing context, capability, tool affordance, feedback, source clarity, or authority boundary that would let the agent operate at human-or-better level. This prevents downstream symptom patches and code bloat.

The advocate should inspect or request traces, prompts, loaded context, tool descriptions, tool outputs/errors, state, memory retrieval, source conflicts, handoffs, feedback, retry loops, stop conditions, and the likely human baseline. It should classify the root cause as one or more of:

- missing, stale, excessive, or conflicting context
- unclear task/admission policy
- bad tool affordance or vague tool description
- misleading, lossy, or unstructured tool output
- conflicting source authority or identity resolution
- missing memory/context retrieval or bad compaction
- weak feedback loop, observation, or recovery path
- subagent handoff/ownership ambiguity
- prompt/tool/state mismatch
- missing deterministic guard, eval, or replay
- human-parity gap: a human would have had context, feedback, affordance, or authority the agent lacked
- bad incentives, stop condition, budget/backpressure, or escalation policy

The advocate blocks launch when the plan fixes only the visible symptom without naming the upstream failed invariant and the evidence that would catch recurrence. Use `templates/agent-failure-rca.md`.

## Architecture Steward

For Tier 2/3, and for any task that touches agentic-system behavior, create an explicit **Architecture Steward** lane. This may be a separate subagent only when the user has authorized subagents/parallel work; otherwise the main agent must run the steward pass itself.

The Architecture Steward participates before the confidence gate and again at final acceptance. It is not merely a late auditor. It should:

- load only the relevant local/agentic architecture guide sections, not the whole guide by default
- classify the component and name the architectural layer being changed
- enforce deterministic harness vs adaptive policy separation
- challenge unnecessary complexity, over-tiering, and subagent/audit cost
- check source authority, context, memory, tool, durable execution, adoption-state, eval, budget/backpressure, and human-approval boundaries when relevant
- block launch if the plan lacks enforceable tests/evidence for the claimed architecture
- block acceptance if implementation drifted from the plan or if evidence is missing

The steward may direct revisions and participate in planning, but it must not claim implementation ownership or edit shared files unless explicitly assigned a disjoint write set. Its output must be evidence-backed: concrete blocker/non-blocker findings tied to plan sections, files, commands, tests, or eval gaps.

Use `templates/architecture-steward-report.md` for the planning and final passes.

## Planning contract

Create or adapt `templates/plan-contract.md`. The plan must include:

- objective and user-visible outcome
- in scope, out of scope, and assumptions
- tier and why the tier is not overkill
- affected repos/files and protected-file constraints
- component classification for agentic work
- planning review board lanes activated, their scope, and blocker authority when relevant
- Agent Advocate / agent-failure RCA lane when agent behavior, multi-agent design, or symptom-patch risk exists
- Architecture Steward lane, guide-loading scope, and blocker authority when relevant
- deterministic harness responsibilities vs model-owned adaptive behavior
- source authority/truth boundaries where relevant
- side-effect, approval, rollback, and adoption-state policy
- subagent plan only if explicitly authorized and useful
- cost/complexity tradeoff and simpler alternatives considered
- tests/evals/audits mapped to risks
- final rubric with only relevant dimensions

For OpenClaw/Type0/agentic-system work, read the local coordination and architecture guides before editing, claim files, and honor protected-file rules.

## Confidence gate

Before launch, ask the model to falsify the plan. Use `templates/confidence-gate.md`.

Do not say “100% confident” if any material blocker remains. Instead, revise the plan and rerun the gate.

Required verdict format:

```text
Confidence verdict:
- 100% confident within scope? yes/no
- Scope:
- Material blockers:
- Non-blocking residual risks:
- Required revisions:
- Evidence required before completion:
```

## Codex goal launch

Only create a Codex goal after explicit user instruction such as “Launch this as a Codex goal.” Do not create a goal merely because a plan exists.

Use the full plan for reasoning, but keep the goal objective compact enough for Codex to carry through continuations. Include:

- destination and current starting point
- hardened objective and scope
- tier
- path or compact summary of the plan contract
- preserve/non-regression constraints
- verification gates and required evidence
- allowed subagent/audit shape, if useful
- done/stop conditions and user approval boundaries
- success metric

Do not set a goal token budget unless the user explicitly gives one.

Before returning or creating a `/goal` objective, validate the objective text with `scripts/validate_goal_objective.py` using `--target-chars 3400 --strict-target`. Hard limit is 3,999 objective characters after stripping a leading `/goal`; treat 3,800+ as failed draft and compress. Do not force the whole plan into the goal; put details in a plan artifact and point the goal at it.

## Subagents and parallel work

Use subagents only when the current user request explicitly authorizes subagents, delegation, or parallel agents. If authorized:

- keep the main agent as overseer/integrator
- assign disjoint write sets to implementation workers
- delegate bounded sidecar audits that can run in parallel
- do not delegate the immediate critical-path blocker
- require evidence-backed outputs, not generic approval

If write sets overlap, serialize the work instead of parallelizing.

## Execution ledger

For Tier 1+, keep a goal ledger using `templates/goal-ledger.md`. Update it after major steps with:

- current phase
- completed work
- open risks
- tests/evals/audits added or run
- architecture issues
- known gaps
- next checkpoint

## Final acceptance

Use `templates/final-acceptance.md`. Try to prove the implementation is not ready. Check:

- rubric scores
- code quality and dead code
- architecture conformance
- cost/complexity tradeoff still justified
- unit/regression/integration/UI/eval evidence as relevant
- external side effects and approvals
- rollback/adoption state
- known gaps

Only mark a Codex goal complete when the objective is actually achieved and no required work remains, or when the user explicitly accepts named residual gaps.

## Helpful resources

- `templates/plan-contract.md` — planning artifact.
- `templates/confidence-gate.md` — pre-launch falsification gate.
- `templates/goal-ledger.md` — long-running goal state.
- `templates/planning-review-board.md` — loophole/simplifier/codebase/platform/quality planning lenses.
- `templates/agent-failure-rca.md` — Agent Advocate root-cause analysis for agent mistakes and multi-agent systems.
- `templates/architecture-steward-report.md` — planning/final architecture enforcement.
- `templates/agent-brief.md` — bounded worker/auditor handoff.
- `templates/final-acceptance.md` — final acceptance gate.
- `references/codex-goal-objective.md` — compact Codex goal objective guidance.
- `references/tiering-and-rubric.md` — tier choice and rubric guidance.
- `references/agentic-architecture-checklist.md` — architecture review checklist.
- `scripts/validate_goal_objective.py` — Codex goal objective length check.
- `scripts/validate_plan_contract.py` — section/rubric sanity check.
- `scripts/validate_acceptance_report.py` — acceptance evidence sanity check.
- `scripts/validate_architecture_steward_report.py` — Architecture Steward report evidence check.
- `scripts/lint_skill_package.py` — package hygiene and metadata lint.
- `tests/test_validators.py` — validator regression tests with positive and negative fixtures.
- `evals/golden_skill_invocations.json` — behavior eval seeds for future fresh-agent tests.
