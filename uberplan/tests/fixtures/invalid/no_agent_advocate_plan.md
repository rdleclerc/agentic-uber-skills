# Plan Contract

## Objective
Change a multi-agent handoff prompt.
## Scope
One skill only.
## Tier decision
- Tier: 2
- Why this tier is sufficient: contained.
- Why this tier is not overkill: agent behavior risk.
- Concrete risks that justify this tier: multi-agent behavior.
## Affected surfaces
| Surface | Files/areas | Risk | Owner |
|---|---|---|---|
| prompt | SKILL.md | medium | overseer |
## Architecture classification
Skill and multi-agent/subagent system.
## Planning review board
- Lanes activated: Architecture Steward.
- Lanes skipped, and why: Agent Advocate skipped.
- Findings reconciled into this plan: none.
- Board verdict: allow confidence gate? yes
## Architecture Steward lane
- Steward mode: main-agent pass.
- Guide sections to load, and why: subagents.
- Planning-stage steward findings: none.
- Blocker authority: launch cannot proceed until material steward blockers are resolved.
## Deterministic harness vs adaptive policy
Harness owns ownership; model owns synthesis.
## Side effects, approvals, and rollback
No external writes.
## Risk-to-evidence map
| Risk/failure mode | Required evidence | Command/artifact | Owner |
|---|---|---|---|
| prompt drift | regression | test | overseer |
## Acceptance rubric
| Dimension | Pass condition | Required evidence | Score |
|---|---|---|---|
| Scope clarity | explicit | plan | 3 |
| Planning review | board | verdict | 3 |
| Architecture | steward | report | 3 |
| Ownership | clear | brief | 3 |
| Unit/regression tests | pass | test | 3 |
## Pre-launch confidence gate
Confidence verdict:
- 100% confident within scope? yes
- Material blockers: none
