---
name: uberarchitect
description: "Do not auto-trigger from task similarity. Use only when explicitly named by the user or routed by ubergoal, uberassess, uberplan, or uberaccept for system-scale architecture questions: concurrency, scaling, queues, workers, long-running jobs, gateways, orchestration, workflow durability, backpressure, repeated timeouts, or agents stuck in micro-patches. Forces a senior-architect stepback before local code fixes."
---

# Uberarchitect

## Core rule

`uberarchitect` is the architecture stepback gate. It prevents agents from debugging the current implementation so narrowly that they miss the standard system shape.

Use it to answer: **what kind of system is this, how is this class of problem normally solved, and is the current implementation fighting that pattern?**

It does not implement. It produces an architecture recommendation and proof plan. If implementation is approved, hand off to `$ubergoal`/`$uberplan`.

## When to use

Use only when explicitly named or routed by an Uber skill for material system-design risk, especially:

- concurrency, scaling, admission, backpressure, rate limits, queues, workers, leases, or priority;
- long-running jobs, stuck gateways, blocked pipelines, repeated timeouts, or throughput collapse;
- multi-agent orchestration, workflow durability, durable execution, task dispatch, or result events;
- repeated coding-agent attempts that patch symptoms but miss the system pattern.

Do not use for tiny deterministic edits, local refactors with no architecture question, or ordinary debugging where the component class and architecture are already settled.

## Procedure

1. **Stop local patching.** Say plainly that this is an architecture pass, not a code-fix pass.
2. **Restate the problem in human language.** Avoid jargon before the operator understands the failure.
3. **Classify the system.** Name the class: queue/worker system, actor system, durable workflow, event pipeline, agent loop, tool boundary, memory/source lane, context engine, guardrail, or other.
4. **Name the normal pattern.** Compare to common prior art and ordinary software architecture. For example: producer → durable queue → bounded worker pool → durable state/results → backpressure.
5. **Fresh-start design.** Ask what a senior architect would build if starting today, unconstrained by current files.
6. **Current mismatch.** Explain where the existing implementation fights the normal pattern.
7. **Demote symptom patches.** List local changes that may help but are not the root architecture.
8. **Smallest transition path.** Separate a stabilizer from the real architecture move.
9. **Scope revision gate.** If the fresh-start architecture materially differs from the current implementation plan, say `Scope revision required: yes` and do not approve the original local patch plan without revised scope.
10. **Proof gate.** Name the smallest experiment that would prove or falsify the architecture before a rewrite.
11. **Human counterfactual.** Ask whether a competent senior human with the same facts would likely have missed this. If not, name the missing agent affordance.

## Required output: Architecture Stepback Packet

For Tier 1+ use, produce these fields:

- **Plain-English diagnosis:** one paragraph a human operator can understand.
- **System class:** the architectural category and why.
- **Normal industry architecture:** the standard pattern and prior-art examples.
- **Fresh-start architecture:** what should exist if built cleanly today.
- **Current mismatch:** how the existing implementation diverges.
- **Symptom patches demoted:** patches that may be useful but must not be mistaken for the root solution.
- **Smallest transition path:** stabilizer first, target architecture second.
- **Scope revision required:** yes/no; if yes, state the revised implementation scope and halt the original local-patch plan until approved.
- **Proof gate:** experiment, metrics, and failure threshold.
- **Human counterfactual / agent affordance gap:** what a senior human would see and what the agent lacked.
- **Recommendation:** adopt/watch/reject plus implementation approval boundary.

Use `templates/architecture-stepback-packet.md` when a durable artifact is useful.

## Type0 example

Bad answer:

> Tune context injection, subprocess timeouts, and gateway settings first.

Better answer:

> Type0 is treating long-running reporter work like blocking gateway calls. The normal architecture is assignment queue plus bounded worker pool plus durable state/results plus backpressure. A short-term OpenClaw turn-slot limiter may stabilize the current system, but the real architecture is asynchronous assignment dispatch with workers returning results.

## Route-hook guidance for other Uber skills

- `$uberassess`: route here before adoption recommendations when a research question involves system-scale concurrency/orchestration or repeated local patches.
- `$uberplan`: route here before implementation planning when the system shape may be wrong.
- `$ubergoal`: route here for Tier 2+ agentic-system goals whose failure class is architectural.
- `$uberaccept`: reject completion if a system-scale failure was answered only with micro-patches and no architecture stepback.

## Anti-patterns

- Architecture theater: filling the packet with generic words while still recommending the same local patch.
- Pattern overreach: forcing queues/workers onto every problem.
- Big rewrite reflex: naming the ideal architecture without a smallest transition proof.
- Hidden deterministic decision tree: keyword-matching the user's problem into a fixed architecture.
- Jargon-first answer: speaking in labels before the operator understands the system failure.
