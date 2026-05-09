# Planning Review Board

Use this before launch for Tier 2/3, and inline for Tier 1 when useful. A lane can be performed by the main agent or a subagent when explicitly authorized.

## Board configuration

- Tier:
- Lanes activated:
- Lanes intentionally skipped, and why:
- Separate subagents used? yes/no; if yes, user authorization:

## Agent Advocate / Agent Failure RCA

Use for multi-agent systems, repeated agent errors, and fixes to agent behavior. Reconstruct what the agent saw and why the mistake was locally plausible. Run the human counterfactual: would a competent human with normal context/tools have made the same error? If not, name the human-parity gap. Do not accept symptom patches without an upstream invariant, tool/context/source/memory/human-parity fix, and a recurrence test/eval.

| Severity | Agent-perspective finding | Human counterfactual / parity gap | Failed invariant or layer | Required fix/evidence |
|---|---|---|---|---|
| blocker/non-blocker |  |  |  |  |

## Loophole Hunter / Red Team

Find hidden assumptions, bypasses, unsafe side effects, missing tests, race/idempotency gaps, context-loss risks, and ways the plan could pass superficially while failing in reality.

| Severity | Loophole | Evidence | Required fix |
|---|---|---|---|
| blocker/non-blocker |  |  |  |

## First-Principles Simplifier / Complexity Auditor

Fight complexity aggressively. Remove machinery unless the benefit is clearly much greater than total cost across implementation, maintenance, debugging, onboarding, context burden, evals, coordination, latency, rollback, and failure surface. Challenge requirements before optimizing them.

| Complexity source | Delete/simplify/substitute alternative | Benefit >> cost? | Hidden downstream cost | Recommendation |
|---|---|---|---|---|
|  |  | yes/no |  |  |

## Codebase Scout / Cartographer

Map existing extension points, tests, conventions, protected files, active claims, and likely integration hazards. For complex codebases, split exploration into non-overlapping slices and leave a reusable pheromone trail.

| Slice | Key files/lines | Pattern/invariant found | Unknowns / follow-up angle |
|---|---|---|---|
|  |  |  |  |

## OpenClaw / Platform Steward

Use when work touches OpenClaw, Type0, runtime, gateway, launchd, orchestration, sessions, skills, machine ops, or protected files.

| Policy/source | Constraint | Plan impact |
|---|---|---|
|  |  |  |

## Quality/Eval Strategist

Map risks to evidence. Prefer real-world fixtures for judgment/model behavior.

| Risk | Evidence layer | Fixture/source | Command/artifact |
|---|---|---|---|
|  | unit/regression/integration/UI/eval/audit |  |  |

## Cost/Risk Governor

Challenge tier, number of agents, audit rounds, stop conditions, and token/time cost.

- Recommended tier:
- Max agents/audit rounds:
- Stop conditions:
- What to defer or remove:
- Benefit >> cost threshold satisfied? yes/no:

## Reconciled planning changes

List changes made to the plan because of this board.

| Finding source | Plan change | Status |
|---|---|---|
|  |  | resolved/deferred/accepted risk |

## Board verdict

```text
Planning review board verdict:
- Allow confidence gate? yes/no
- Material blockers:
- Non-blocking improvements:
- Simplifications adopted:
- Explicitly deferred suggestions:
```
