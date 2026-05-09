# Agent Advocate / Agent Failure RCA

Use this before planning a fix for an agent or multi-agent-system failure. Do not patch yet unless it is a reversible mitigation.

## Incident or behavior being addressed

- Symptom:
- Affected agent/session/task IDs:
- User-visible impact:
- Current mitigation, if any:

## Agent-eye reconstruction

Reconstruct what the agent likely saw and why the mistaken action was locally plausible.

| Step | Agent goal/state | Context available | Tool/memory/source observations | Decision made | Why it looked reasonable |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## Human counterfactual

Ask whether a competent human in the same role, with normal context and tools, would likely have made this error. Do not compare the agent to an omniscient human; compare it to a human operator with the information/capabilities the system should reasonably provide.

- Would a competent human have made this error? yes/no/unclear
- If no, what did the human likely have that the agent lacked?
  - missing context:
  - missing tool/capability:
  - misleading or incomplete tool feedback:
  - unclear source authority or identity:
  - missing memory/history:
  - missing state/admission signal:
  - missing handoff/ownership clarity:
  - missing recovery/stop guidance:
- If yes or unclear, what policy, product, or domain ambiguity also needs to be resolved?
- Human-parity fix required before launch:

## Context/tool/source diagnosis

| Layer | Failure question | Finding | Evidence |
|---|---|---|---|
| Task/admission | Was the agent admitted to the right task/state? |  |  |
| Context assembly | Was key context missing, stale, excessive, buried, or conflicting? |  |  |
| Tool affordance | Did tool names/descriptions/schemas invite misuse? |  |  |
| Tool output | Was output misleading, lossy, unstructured, or missing next-step feedback? |  |  |
| Source authority | Were truth/retrieval/synthesis/sidecar boundaries clear? |  |  |
| Memory/retrieval | Did memory retrieval/compaction distort the situation? |  |  |
| Handoff/ownership | Did subagent or role boundaries confuse responsibility? |  |  |
| Feedback/recovery | Did the system show the error and recovery path? |  |  |
| Stop/budget/backpressure | Did incentives, caps, retries, or escalation policy push the wrong action? |  |  |
| Human parity | Would a competent human have avoided this with context/tools the agent lacked? |  |  |

## RCA ladder

- Symptom:
- Immediate failure:
- Enabling condition:
- Failed guard/invariant:
- Human counterfactual / parity gap:
- Upstream admission/context/tool failure:
- Recovery/detection gap:
- Class-level cause:
- Minimal durable fix at the lowest enforceable layer:

## Symptom-patch rejection test

Explain why a narrow downstream patch would be insufficient, or why the proposed fix is truly the lowest durable layer.

## Fix contract

| Root cause | Durable contract/invariant | Human-parity fix | Test/eval/replay that proves it |
|---|---|---|---|
|  |  |  |  |

## Advocate verdict

```text
Agent Advocate verdict:
- Plan may proceed? yes/no
- Root cause understood? yes/no
- Human counterfactual answered? yes/no
- Human-parity gap fixed or explicitly accepted? yes/no
- Symptom-patch risk: low/medium/high
- Material blockers:
- Required context/tool/source/eval changes:
- Evidence required before acceptance:
```
