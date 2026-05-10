# Agentic Simplification

Agentic systems often accumulate complexity from symptom patches: extra prompts, fallback branches, tools, retries, queues, or memory paths.

Before deleting agent-facing complexity, ask:

- Did this complexity compensate for missing context, bad tool output, unclear source authority, weak feedback, or poor handoff?
- Would a competent human with normal context/tools need it?
- If not, can we fix the agent environment instead of preserving the workaround?
- Does simplification remove an affordance agents need to operate at human-or-better level?

Prefer fixes that improve context, tools, source authority, observability, deterministic guards, and handoffs over local symptom-patch deletion.


## Agent Advocate / human-counterfactual lens

For every agent-created failure that produced complexity, ask:

1. Would a capable human with the same mission, context, tools, and feedback have made this error?
2. If not, what was missing: context, source authority, tool feedback, observability, affordance, memory, or permission boundary?
3. Is the current complexity a symptom patch that compensates for the missing affordance?
4. Would simplifying by deleting the support harm agents more than humans because agents lack an implicit capability humans use?
5. Can the simpler fix be upstream: clearer context assembly, better tool results, stronger contracts, deterministic harnesses, or fail-fast errors?

Prefer fixing upstream affordances/source authority over accumulating retries, fallback branches, prompt patches, or hidden heuristics. Do not remove compensating support until the upstream affordance is proven by tests/evals or real-world replay.
