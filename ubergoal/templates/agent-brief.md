# Agent Brief

## Role

Implementation worker / Architecture Steward / Agent Advocate / quality-eval auditor / code-health auditor / UI verifier.

## Context

Summarize only what this agent needs. Do not leak desired conclusions to auditors.

## Scope

- Read scope:
- Write set, if any:
- Allowed tools:
- Forbidden tools:
- Memory scope:
- Context policy:
- Forbidden files/actions:
- Side-effect constraints:
- Expected eval/verification:
- Handoff owner / integrator:

## Task


## Return contract

Return:

- files changed or inspected
- findings tied to file paths, commands, or evidence
- tests/evals/audits run
- unresolved risks
- recommended next action

## Stop conditions

Stop if blocked, if scope would be exceeded, or if external/destructive action would be required.

## Architecture Steward special instructions

If this brief is for the Architecture Steward, participate in planning before launch and again at final acceptance. Load only relevant architecture guide sections. Challenge both under-engineering and over-engineering. Return blocker/non-blocker findings tied to evidence, and recommend whether launch/acceptance should proceed.

## Agent Advocate special instructions

If this brief is for the Agent Advocate, reconstruct what the agent saw and why the mistake was locally plausible. Inspect traces, prompts, context, memory retrieval, tool descriptions, tool outputs/errors, source authority, state/admission, handoffs, feedback, retries, and stop conditions. Block fixes that only patch the visible symptom without an upstream invariant and recurrence test/eval.
