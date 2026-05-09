# Tiering and Rubric Guidance

## Prefer lower tiers unless risk justifies machinery

Use the rigorous workflow to reduce risk, not to maximize ceremony.

Escalate tiers for concrete reasons:

- unclear architecture or agentic-system behavior
- multiple repos or shared files
- production/runtime/launchd/cron/gateway/config risk
- prompts, skills, tool contracts, evals, context, memory, source authority, identity, subagents, or adoption-state changes
- concurrency, idempotency, security, privacy, migration, deletion, or external-write risk
- UI/user-visible behavior requiring browser verification
- long-running work where context drift is likely

De-escalate when:

- change is isolated and easy to review
- no judgment/model behavior changes
- no external side effects
- ordinary tests directly prove the outcome
- subagent coordination would cost more than it saves

## Rubric rules

A rubric is useful only if each row has observable evidence.

Avoid generic rows like “good quality.” Prefer:

- “Focused regression test covers duplicate retry race”
- “Browser check verifies form submit success and no console errors”
- “Real-world eval cases include prior false-positive incident and near miss”
- “`rg` reference sweep shows deleted helper has no dynamic callers”

Remove irrelevant rows. If no UI changed, do not require a UI score; state “not applicable” once.

## Scoring

- 0 = blocker; do not launch/accept
- 1 = weak or unresolved; revise unless the user explicitly accepts it
- 2 = acceptable with named residual risk
- 3 = strong evidence

For final completion, critical dimensions should be 3. Any non-3 score needs a named residual gap and explicit acceptance.

## Review lanes versus agents

Prefer review lanes over always spawning agents. A lane is a perspective with a return contract; a subagent is only needed when isolation, parallelism, or context separation is worth the cost.

Use separate agents for planning lanes when:

- the work is Tier 3,
- the lane can inspect independently without blocking the main path,
- the lane has a distinct context or expertise need,
- the result can materially change the plan before implementation.

Do not use separate agents when:

- the task is small,
- the main agent can run the checklist quickly,
- findings would be generic,
- coordination cost exceeds expected risk reduction.

## Agent Advocate trigger

Activate the Agent Advocate lane when work involves multi-agent design, agent errors, prompts, tools, memory, context, source authority, handoffs, retries, or recovery. This lane pays for itself when it prevents symptom patches and code bloat. It is optional for conventional deterministic code with no agent behavior.
