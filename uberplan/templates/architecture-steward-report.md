# Architecture Steward Report

## Pass type

Planning pass / final acceptance pass.

## Guide-loading scope

List only the guide sections/docs loaded and why. Do not load the entire guide by default.

| Guide/source | Why loaded | Relevant decision |
|---|---|---|
|  |  |  |

## Component classification

Name the architectural layer(s): deterministic workflow, augmented LLM, agent loop, multi-agent/subagent system, tool/tool registry, skill, memory subsystem, source lane, identity layer, context engine, durable execution, guardrail/human review, cross-agent coordination, attention policy, adoption-state change, eval/observability layer.

## Harness vs policy review

| Deterministic harness responsibility | Model/adaptive policy responsibility | Issue? |
|---|---|---|
|  |  |  |

## Required architecture dimensions

Complete each relevant row or explicitly mark it not applicable with a reason.

| Dimension | Steward question | Finding | Evidence | Blocker? |
|---|---|---|---|---|
| Source authority | Are truth, retrieval, recall, synthesis, sidecar, candidate, and outbound artifact roles separated? |  |  |  |
| Context assembly | Is needed context available, scoped, fresh, and not overloaded? Are source handles preserved? |  |  |  |
| Memory behavior | Are memory reads/writes scoped, contradicted/retired safely, and traceable? |  |  |  |
| Tool boundaries | Are tool names, descriptions, schemas, permissions, outputs, and failure modes model-safe? |  |  |  |
| Repository topology | Do new/moved code files land in named packages with an executable topology/dependency guard instead of prose-only hierarchy? |  |  |  |
| Durable execution | Are checkpoints, replay safety, idempotency keys, stop conditions, and trace IDs defined where needed? |  |  |  |
| Eval/observability | Are real fixtures, negative cases, traces, and acceptance evidence sufficient? |  |  |  |
| Adoption/rollback | Are adoption state, rollback, and promotion rules explicit? |  |  |  |
| Subagent ownership | Are write sets, allowed tools, memory/context scope, return contracts, and integrator ownership clear? |  |  |  |
| Human approvals | Are external writes, destructive actions, and policy ambiguities gated correctly? |  |  |  |
| Budget/backpressure/fallback | Are token/time/cost limits, retry/backpressure behavior, and provider fallback policy explicit? |  |  |  |

## Complexity and tier challenge

- Is the selected tier too light?
- Is the selected tier too heavy/costly?
- Are subagents/audits justified by concrete risk?
- What can be simplified without losing safety?

## Architecture findings

| Severity | Finding | Evidence | Required change |
|---|---|---|---|
| blocker/non-blocker |  | plan section/file/test/eval |  |

## Gate recommendation

```text
Architecture Steward verdict:
- Allow launch/acceptance? yes/no
- Material blockers:
- Non-blocking residual risks:
- Required plan/code/evidence changes:
```
