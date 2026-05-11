# Agentic Architecture Checklist

Use this when the task touches agentic-system behavior: agent loops, orchestration, tools, skills, prompts, memory, context, source authority, identity, subagents, provider fallback, cost controls, human attention, evals, or durable execution.

## Agent Advocate / failure RCA

For multi-agent systems and agent mistakes, add an Agent Advocate lane before choosing a fix. The advocate explains the failure from the agent's perspective: what context, tools, memory, sources, state, handoffs, feedback, and stop conditions made the wrong action plausible. It also asks the human counterfactual: would a competent human with normal context/tools have made the error? If not, fix the missing information/capability/feedback/authority that prevented human-parity agent behavior.

Never accept “the model made a bad judgment” as root cause until the plan identifies which deterministic harness, tool contract, context policy, source-authority boundary, memory behavior, eval, or feedback loop should have bounded that judgment.

## Architecture Steward role

For Tier 2/3 or any agentic-system change, make architecture enforcement an explicit lane. The Architecture Steward participates during planning, not just after implementation. It should load only relevant guide docs, challenge complexity/cost, classify the component, enforce the deterministic harness/adaptive policy split, and block launch or acceptance on material gaps.

The steward is not an all-purpose reviewer. Its job is architectural safety and coherence: source authority, context, memory, tools, durable execution, evals, identity, adoption state, human approvals, budget/backpressure, and subagent ownership when those layers are in scope.

## Classify the component

Name the component type: deterministic workflow, augmented LLM, agent loop, multi-agent/subagent system, tool, skill, memory subsystem, source lane, identity layer, context engine, durable execution, guardrail, cross-agent coordination, attention policy, adoption-state change, eval/observability layer.

## Split harness from policy

Deterministic harness should own schemas, permissions, idempotency, budgets, checkpoints, memory APIs, source authority, identity resolution, context assembly, tool execution, approvals, traces, and evals.

Model/adaptive policy should own ambiguous interpretation, context gathering, tool choice within allowed tools, memory retrieval choices, decomposition, plan revision, recovery, and synthesis.

## Agent Boundary Contract

For every boundary where model output becomes tool input, state, memory, context, delegated work, external action, or durable truth, require a contract for shape, authority, isolation, failure semantics, observability, and replay/eval evidence.

Use recurring failures as sentinel probes, not as the doctrine: wrong-shaped IDs, swallowed tool errors, missing ask path, shared mutable state, untrusted memory/context, unbounded loops, ungated privileged action, parent-history dumps to subagents, and missing trace propagation.

## Regex / keyword semantic gate

Regex and keyword matching are allowed for mechanical syntax: identifiers, timestamps, paths, protocol envelopes, command flags, and owned structured formats.

Regex and keyword matching must not be the authority for semantic judgment over natural language: intent, request-likeness, routing, memory meaning, source selection, priority, importance, or whether a model sees a message. If a regex/keyword result is useful, treat it as a candidate signal passed to model policy or human review with the raw input preserved.

Any proposed semantic-authority exception requires explicit approval, named eval/replay coverage, observability, and rollback. The default verdict is no.

## Source and truth boundaries

State what is raw evidence, authoritative truth, retrieval-only material, memory/recall, synthesis, candidate signal, sidecar output, and outbound artifact. Do not silently promote synthesis or sidecar output into truth.

## Durable execution

For long-running or side-effecting work, require checkpoints, replay-safe side effects, idempotency keys for external writes, stop conditions, trace IDs, and rollback/adoption-state plans.

## Evals

For LLM judgment or generated behavior, require real-world fixtures when possible, negative and near-miss cases, explicit rubrics, traceable results, and a known-gap statement if live-safe replay/eval was not run.

## Anti-patterns

- brittle keyword routing for semantic judgment
- regex as semantic authority over natural language
- silent paid/provider fallback
- vague tools like `run(query: string)` without contracts
- subagents with overlapping write sets and no integrator
- one successful demo treated as production adoption
- final “looks good” without evidence layers
