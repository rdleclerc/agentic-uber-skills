# Plan Contract

## Objective
Improve a multi-agent handoff prompt so workers stop overwriting each other and return evidence-backed findings.

## Scope
In scope: one skill prompt, one agent brief template, validator fixture updates. Out of scope: live runtime changes, commits, pushes, or production writes.

## Tier decision
- Tier: 2
- Why this tier is sufficient: agent behavior changes are meaningful but contained to one skill package.
- Why this tier is not overkill: Architecture Steward plus Agent Advocate catch symptom-patch and guide-drift risks without launching a full implementation swarm.
- Concrete risks that justify this tier: multi-agent ownership ambiguity, prompt/tool mismatch, and insufficient acceptance evidence.

## Cost/complexity check
- Failure class this plan prevents: agents editing shared files without ownership and accepting symptom patches.
- Smaller alternative considered: a one-line prompt warning only.
- Added machinery and why it is worth it: one Agent Advocate pass and validator fixture because the failure previously recurred.
- Benefit >> cost argument: the added validator fixture is small and prevents recurring shared-file overwrite failures with low maintenance cost.
- Hidden downstream costs considered: extra template length, validator upkeep, and more planning overhead.
- Machinery deferred because cost exceeds current benefit: fresh-agent automated eval harness remains future work.

## Clarifying questions gate
- Material ambiguities: none; the failure class is already known.
- Questions asked / answers received: user explicitly wanted better multi-agent safety.
- Recommendations when user says "use judgment": choose the smallest guardrail that blocks shared-file edits without ownership.
- Gate verdict: proceed to architecture? yes

## Codebase exploration / pheromone trail
- Exploration mode: main-agent because scope is one local skill package.
- Slices explored: skill prompt, templates, validators, tests.
- Key files returned and read by overseer: SKILL.md, templates/agent-brief.md, scripts/validate_plan_contract.py, tests/test_validators.py.
- Pheromone trail location: not applicable; findings embedded in this plan.
- Unknowns/follow-up angles: fresh-agent behavioral replay remains future work.

## Architecture options
| Option | Summary | Benefits | Costs/risks | Recommendation |
|---|---|---|---|---|
| Minimal | add prompt warning only | tiny change | weak enforcement | reject |
| Clean | full fresh-agent eval harness | strong proof | too much machinery now | defer |
| Pragmatic | add Agent Advocate fields and validator fixture | blocks known failure cheaply | small validator upkeep | choose |
| First-principles alternative | remove parallel writes entirely | eliminates class | too restrictive for useful work | not chosen |

## Affected surfaces

| Surface | Files/areas | Risk | Owner |
|---|---|---|---|
| skill prompt | SKILL.md and templates/agent-brief.md | medium | overseer |
| validators | scripts/validate_plan_contract.py | medium | overseer |

## Repository topology / package seam

- Intended package/module destination: existing uberplan skill package; validator code stays in `uberplan/scripts/`, validator tests stay in `uberplan/tests/`, fixtures stay in `uberplan/tests/fixtures/`.
- Why this does not belong at the root/convenience layer: root-level helper scripts would bypass skill package lint and make the behavior invisible to the packaged skill.
- Public import/API seam: command-line validator `scripts/validate_plan_contract.py` and the skill/template contracts it validates.
- Private/internal files: unit fixtures under `tests/fixtures/` and package-local test helpers.
- Repo-local topology/dependency guard to run or add: `scripts/lint_skill_package.py`, `python3 -m unittest discover -s tests`, and fixture-backed validator commands.
- If no guard exists, why that is acceptable for this task: not applicable; existing package lint and validator tests are the executable guard.

## Architecture classification
Skill, multi-agent/subagent system, cross-agent coordination layer, guardrail/human-review layer, eval/observability layer.

## Planning review board
- Lanes activated: Architecture Steward, Agent Advocate, Loophole Hunter, Quality/Eval Strategist.
- Lanes skipped, and why: OpenClaw Platform Steward skipped because no OpenClaw runtime or Type0 files are touched.
- Findings reconciled into this plan: added disjoint write-set rule, Agent Advocate human counterfactual, and validator fixtures.
- Board verdict: allow confidence gate? yes

## First-Principles Simplifier / Complexity Auditor
- Simplifier mode: main-agent pass.
- Requirements challenged or deleted: deleted the idea of a full fresh-agent eval harness for local-use readiness.
- Parts/processes/agents/schemas/files removed: no extra audit agents, no new CI, no broad schema system.
- First-principles alternative considered: forbid parallel writes entirely, rejected because disjoint write sets preserve speed safely.
- Benefit >> cost verdict: yes; one small validator fixture has clear benefit >> maintenance cost.
- Simplifier verdict: proceed? yes

## Agent Advocate / Agent Failure RCA
Required because this changes multi-agent behavior.

- Advocate mode: main-agent pass.
- Agent-eye reconstruction source: prior Type0 failures, prompt text, agent brief template, validator outputs.
- Human counterfactual: a competent human would ask who owns each file before editing and would notice missing evidence requirements.
- Human-parity gap fixed: explicit write-set, context policy, return contract, and recurrence fixture.
- Agent-eye reconstruction source detail: prompts and tool-output examples show agents lacked clear ownership and completion feedback.
- Root failed invariant, if known: no worker may edit shared files without a disjoint write set and evidence return contract.
- Symptom-patch risk: low after invariant and validator fixture are added.
- Advocate verdict: proceed? yes

## Architecture Steward lane
Required because this is a skill and multi-agent coordination change.

- Steward mode: main-agent pass.
- Guide sections to load, and why: subagents, cross-agent operating model, evals, and skills because they directly govern this change.
- Planning-stage steward findings: deterministic validator must enforce ownership/evidence shape; model policy may choose decomposition inside that harness.
- Blocker authority: launch cannot proceed until material steward blockers are resolved.

## Deterministic harness vs adaptive policy

| Deterministic harness owns | Model/adaptive policy owns |
|---|---|
| validator schema, explicit write sets, return contract, side-effect gates, evidence rows | task decomposition, context selection, tool choice inside allowed tools, synthesis |

## Agent Boundary Contract
Required because model-produced task decomposition can become delegated work and shared-file edits.

- Boundary surfaces: subagent task input, worker write set, returned evidence, and integrator acceptance.
- Shape contract: worker briefs must name role, allowed read scope, disjoint write set, return contract, and stop condition.
- Authority contract: integrator owns final acceptance; workers cannot broaden scope, change shared ownership, or claim completion without evidence.
- Isolation contract: no overlapping write sets; no shared mutable work queue; parent context is summarized into a bounded task brief rather than dumped wholesale.
- Failure semantics: missing owner/write set/evidence is a blocking validation failure, not a warning.
- Observability/replay evidence: validator fixture and golden eval seed record the recurrence proof; session logs preserve command outputs.
- Sentinel probes checked: parent-context dump, shared mutable write state, missing trace/evidence propagation, and swallowed worker failure.
- Boundary verdict: proceed? yes

## Regex / keyword semantic gate
Required because this plan changes agentic validators and prompt policy.

- Pattern uses introduced/touched: validator regexes for markdown headings, field labels, table rows, and placeholder detection.
- Classification for each use: mechanical syntax for owned markdown contract parsing; no candidate signal or semantic authority over natural language.
- Semantic authority over natural language present? no
- If yes, explicit exception approval and why model policy is not sufficient: not applicable because no semantic-authority regex/keyword use is present.
- Raw input preserved for model/review? yes, plans and reports remain intact; validators only accept or reject contract shape.
- Eval/replay/negative cases: valid and invalid validator fixtures cover missing required sections, hollow fields, and boundary contract omissions.
- Observability and rollback: validator errors name missing fields; rollback is normal file revert.
- Gate verdict: proceed? yes

## Source authority and truth boundaries

Authoritative: skill files and validator outputs. Retrieval-only: prior incident narratives. Synthesis: planning board recommendations. No synthesis may become acceptance evidence without command/test output.

## Side effects, approvals, and rollback

- External writes/destructive actions: none.
- Required human approvals: required before goal launch, subagent spawning, commit, push, or external writes.
- Idempotency/undo strategy: normal file revert.
- Adoption state before: local draft skill.
- Adoption state after: local installed skill, not GitHub canonical.
- Rollback plan: restore previous skill folder from versioned copy or file diff.
- Checkpoint/replay policy: record plan and acceptance reports in session log.
- Trace IDs/artifact locations: session log plus test command output.
- Budget/backpressure/fallback policy: max one review pass unless blockers remain; no paid/provider fallback.
- Max agents/audit rounds, if any: two audit rounds without explicit user approval.

## Multi-agent plan

Only used if user explicitly authorizes subagents.

| Agent role | Purpose | Write set / read scope | Return contract | Stop condition |
|---|---|---|---|---|
| Overseer/integrator | Own synthesis and final acceptance | all claimed files | reconciled plan and evidence | rubric satisfied or blocked |
| Architecture Steward | Enforce guide and harness/policy split | read-only skill files | blocker/non-blocker findings | no material architecture blockers |
| Agent Advocate / Agent Failure RCA | Explain why an agent would err | read-only prompts/templates/traces | failed invariant and recurrence evidence | root cause understood |

## Risk-to-evidence map

| Risk/failure mode | Required evidence | Command/artifact | Owner |
|---|---|---|---|
| hollow plan passes | regression test | tests/test_validators.py invalid hollow fixture | overseer |
| symptom patch accepted | agent behavior eval fixture | evals/golden_skill_invocations.json | overseer |
| subagent conflict | template review | templates/agent-brief.md | architecture steward |

## Acceptance rubric

| Dimension | Pass condition | Required evidence | Score |
|---|---|---|---|
| Scope clarity | In/out/non-scope and assumptions are explicit | plan contract | 3 |
| Planning review | Relevant lanes ran or were explicitly skipped | board verdict | 3 |
| Cost/complexity | Smallest guardrail prevents named failure class | cost/complexity check | 3 |
| First-principles simplification | Full fresh-agent harness deferred; small validator chosen | simplifier section | 3 |
| Codebase exploration | Key skill files and validator tests were read by main agent | codebase exploration section | 3 |
| Agent RCA | Agent behavior fix names why the agent erred and failed invariant | Agent Advocate report | 3 |
| Agent boundary contract | Delegation boundary has shape, authority, isolation, failure, observability, and replay evidence | Agent Boundary Contract section | 3 |
| Regex / keyword semantics | Regex/keyword uses are mechanical markdown contract parsing only; no natural-language semantic authority | Regex / keyword semantic gate | 3 |
| Architecture | Guide sections applied and harness/policy split respected | Architecture Steward report | 3 |
| Repository topology | New validator/test files stay inside the existing skill package and package lint/validator tests run | package lint and validator commands | 3 |
| Ownership | Write sets and integrator role are clear | agent brief | 3 |
| Code quality | Validators are simple and maintainable | tests and review | 3 |
| Unit/regression tests | Positive and negative validator fixtures pass | unittest output | 3 |
| Evals | Golden behavioral cases exist for future forward tests | evals/golden_skill_invocations.json | 3 |

## Pre-launch confidence gate

```text
Confidence verdict:
- 100% confident within scope? yes
- Scope: local skill package hardening only; no live runtime, no GitHub save, no goal launch.
- Material blockers: none
- Non-blocking residual risks: fresh-agent behavioral eval not yet automated; golden cases are seed fixtures.
- Required revisions: none
- Evidence required before completion: package lint, validator tests, quick_validate, and acceptance report.
```
