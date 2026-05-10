# Plan Contract

## Objective

State the concrete outcome and why it matters.

## Scope

### In scope

-

### Out of scope

-

### Assumptions

-

## Tier decision

- Tier: 0 / 1 / 2 / 3
- Why this tier is sufficient:
- Why this tier is not overkill:
- Concrete risks that justify this tier:

## Cost/complexity check

- Failure class this plan prevents:
- Smaller alternative considered:
- Added machinery and why it is worth it:
- Benefit >> cost argument:
- Hidden downstream costs considered:
- Machinery deferred because cost exceeds current benefit:

## Clarifying questions gate

Required when requirements, edge cases, integrations, approval boundaries, or success criteria are ambiguous. If not applicable, say why.

- Material ambiguities:
- Questions asked / answers received:
- Recommendations when user says "use judgment":
- Gate verdict: proceed to architecture? yes/no

## Codebase exploration / pheromone trail

Required when the codebase is complex, unfamiliar, or context-heavy enough that missing context is a material risk. Use `exploration-trail.md` when separate scouts are useful and authorized.

- Exploration mode: main-agent / parallel scouts / not applicable because:
- Slices explored:
- Key files returned and read by overseer:
- Pheromone trail location:
- Unknowns/follow-up angles:

## Architecture options

Required for non-obvious feature architecture. Keep concise; do not force this for small deterministic edits.

| Option | Summary | Benefits | Costs/risks | Recommendation |
|---|---|---|---|---|
| Minimal |  |  |  |  |
| Clean |  |  |  |  |
| Pragmatic |  |  |  |  |
| First-principles alternative | delete/substitute/reframe before optimizing |  |  |  |

## Affected surfaces

| Surface | Files/areas | Risk | Owner |
|---|---|---|---|
|  |  |  |  |

## Repository topology / package seam

Required for any new or moved code file. Keep this small and executable.

- Intended package/module destination:
- Why this does not belong at the root/convenience layer:
- Public import/API seam:
- Private/internal files:
- Repo-local topology/dependency guard to run or add:
- If no guard exists, why that is acceptable for this task:

## Architecture classification

Classify relevant components: deterministic workflow, augmented LLM call, agent loop, multi-agent/subagent system, tool/tool registry, skill, memory subsystem, source lane, identity layer, context engine, durable execution, guardrail/human review, cross-agent coordination, attention policy, adoption-state change, eval/observability layer.

## Planning review board

Activate only the lanes justified by tier and risk. For Tier 2/3, complete `planning-review-board.md` or embed its findings here.

- Lanes activated:
- Lanes skipped, and why:
- Findings reconciled into this plan:
- Board verdict: allow confidence gate? yes/no

## First-Principles Simplifier / Complexity Auditor

Required for Tier 2/3 and final acceptance. This lane should aggressively fight complexity and require benefit >> cost for additions.

- Simplifier mode: main-agent pass / separate strongest-reasoning subagent / not applicable because:
- Requirements challenged or deleted:
- Parts/processes/agents/schemas/files removed:
- First-principles alternative considered:
- Benefit >> cost verdict:
- Simplifier verdict: proceed? yes/no

## Agent Advocate / Agent Failure RCA

Required when the task changes multi-agent behavior or fixes an agent mistake. If not applicable, say why.

- Advocate mode: main-agent pass / separate subagent / not applicable because:
- Agent-eye reconstruction source: traces/prompts/context/tool outputs/logs/other:
- Root failed invariant, if known:
- Symptom-patch risk: low/medium/high:
- Advocate verdict: proceed? yes/no

## Architecture Steward lane

Required for Tier 2/3 and any agentic-system behavior. If subagents are not authorized, the main agent performs this pass.

- Steward mode: main-agent pass / separate subagent / not applicable because:
- Guide sections to load, and why:
- Planning-stage steward findings:
- Blocker authority: launch cannot proceed until material steward blockers are resolved.

## Deterministic harness vs adaptive policy

| Deterministic harness owns | Model/adaptive policy owns |
|---|---|
| schemas, permissions, idempotency, budgets, tests, traces, side-effect gates | ambiguous intent, context gathering, plan revision, synthesis, tool choice within harness |

## Source authority and truth boundaries

State authoritative sources, retrieval-only sources, synthesis artifacts, sidecars, and promotion rules. If not relevant, say why.

## Side effects, approvals, and rollback

- External writes/destructive actions:
- Required human approvals:
- Idempotency/undo strategy:
- Adoption state before:
- Adoption state after:
- Rollback plan:
- Checkpoint/replay policy:
- Trace IDs/artifact locations:
- Budget/backpressure/fallback policy:
- Max agents/audit rounds, if any:

## Multi-agent plan

Only fill this if the user explicitly authorized subagents/parallel work.

| Agent role | Purpose | Write set / read scope | Return contract | Stop condition |
|---|---|---|---|---|
| Overseer/integrator | Own plan, decomposition, integration, final acceptance | all claimed files | final synthesis and evidence | rubric satisfied or blocked |
| Architecture Steward | Participate in planning, enforce relevant agentic architecture guide, challenge over/under-complexity, block launch/acceptance on material architecture gaps | read plan/relevant files; no writes unless separately assigned | `architecture-steward-report.md` with blockers/non-blockers tied to evidence | no material architecture blockers |
| Agent Advocate / Agent Failure RCA | Reconstruct why an agent made or would make the error; prevent symptom patches | read traces/prompts/context/tool outputs/logs; no writes unless separately assigned | `agent-failure-rca.md` with failed invariant and recurrence evidence | root cause understood or plan blocked |
| Loophole Hunter / Red Team | Try to disprove the plan before implementation | read plan/relevant files | blocker/non-blocker loopholes tied to evidence | no material loopholes |
| Simplifier / Elegance Reviewer | Find smaller/simpler plan that sidesteps problems | read plan/relevant files | simplification proposal and tradeoffs | adopted or explicitly rejected |
| First-Principles Simplifier / Complexity Auditor | Aggressively delete, simplify, and require benefit >> cost for every addition | read plan/relevant files; no writes unless assigned | `first-principles-simplifier-report.md` | benefit >> cost or plan blocked |
| Codebase Scout / Cartographer | Bring codebase-specific patterns, tests, and constraints into plan | read codebase/tests/claims | codebase map and hazards | no material codebase ignorance |
| OpenClaw / Platform Steward | Bring OpenClaw/Type0/runtime/local-policy constraints when relevant | read local policy/docs only as needed | platform constraints and preflight needs | no policy/protected-file blockers |
| Quality/Eval Strategist | Ensure risk-to-evidence map and rubric are real | read plan/tests/evals | evidence matrix | no material evidence gaps |

## Risk-to-evidence map

| Risk/failure mode | Required evidence | Command/artifact | Owner |
|---|---|---|---|
|  | unit/regression/integration/UI/eval/audit/manual proof |  |  |

## Acceptance rubric

Score only relevant dimensions. Use 0 = blocker, 1 = weak/unresolved, 2 = acceptable with named residual risk, 3 = strong evidence.

| Dimension | Pass condition | Required evidence | Score |
|---|---|---|---|
| Scope clarity | In/out/non-scope and assumptions are explicit | plan contract |  |
| Planning review | Relevant agent-advocate/loophole/simplifier/codebase/platform/quality lanes ran or were explicitly skipped | Planning Review Board verdict |  |
| Cost/complexity | The plan uses the smallest guardrails that address named failure classes and benefit >> cost | Cost/complexity check |  |
| First-principles simplification | Requirements and added machinery were challenged; deletion/simplification was considered | Simplifier report |  |
| Codebase exploration | Key files/patterns/tests were explored when context risk was material | Exploration trail or explicit non-applicability |  |
| Agent RCA | Agent behavior fixes name why the agent erred and the failed invariant/tool/context/source/eval layer | Agent Advocate report or explicit non-applicability |  |
| Architecture | Relevant guide sections were applied; deterministic harness/adaptive policy split is respected where relevant | Architecture Steward report or explicit non-applicability |  |
| Repository topology | New/moved code files land in named packages and repo topology/dependency guard is run or added | topology test/dependency-map command or explicit accepted gap |  |
| Ownership | Write sets and integrator role are clear | claim/briefs |  |
| Code quality | Code is simple, maintainable, typed/idiomatic where applicable | review/tests |  |
| Dead code | References searched and deletions justified | rg/audit output |  |
| Unit/regression tests | Changed behavior has focused coverage | test command output |  |
| Integration tests | Cross-component behavior is verified where relevant | command/output or explicit non-applicability |  |
| UI/browser tests | User-visible UI flows verified where relevant | browser/e2e evidence or explicit non-applicability |  |
| Evals | Judgment/model behavior uses real-world fixtures where available | eval cases/results or explicit non-applicability |  |
| Safety | External/destructive side effects are approved and idempotent | approval/evidence |  |
| Observability | Logs/traces/artifacts are enough to debug failures | trace/log artifacts |  |
| Rollback | Revert/adoption-state plan exists | rollback note |  |
| Acceptance evidence | Commands, outputs, screenshots/traces/gaps recorded | final acceptance report |  |

## Pre-launch confidence gate

Complete this before launch.

```text
Confidence verdict:
- 100% confident within scope? yes/no
- Scope:
- Material blockers:
- Non-blocking residual risks:
- Required revisions:
- Evidence required before completion:
```
