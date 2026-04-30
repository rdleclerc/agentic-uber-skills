---
name: deep-rca
description: Force deep, class-level root cause analysis before patches. Use when asked why/how an incident happened, to do RCA/postmortem/debugging, to investigate stuck loops, production/workflow/agentic-system failures, repeated bugs, suspicious edge cases, or when the user challenges whether a patch addresses the underlying issue rather than a proximate cause.
---

# Deep RCA

Do not stop at the first plausible cause. Do not stop when you can see a fix. Stop when you can name the absent invariant whose enforcement would make the entire failure class impossible.

## Non-negotiable rule

Before proposing a durable patch, answer:

> What upstream policy, state, or admission invariant was missing or unenforced such that this failure was **possible**, **repeatable**, and **not caught earlier**?

If you cannot answer that, say: **"RCA incomplete — still proximate. Do not patch yet except safe mitigation."**

Safe mitigations are reversible operational actions that stop current damage without claiming to fix the class.

## The self-challenge loop — run this yourself, before surfacing

After every candidate root cause, challenge it:

**"This answer is still proximate because ___."**

If you can fill in that blank, you are not done. Keep going.

Common ways to fill the blank (all mean keep going):

- "...it describes what happened, not what allowed it"
- "...a human still had to intervene to notice or stop it"
- "...the same failure could recur via a different trigger"
- "...the fix is a special case, not a policy"
- "...I'm naming a component behavior, not an absent rule"

An answer passes the self-challenge test when: you try to fill in the blank and genuinely cannot. The answer names something **absent** (a rule, policy, state constraint, monitor) whose presence would have made the class impossible — not just this instance harder.

## The convergence test — how to know you're at root

You're at root cause when you can write:

> "If [single gate / policy rule / state constraint] had been enforced, this entire class of failure would have been **impossible** — not just this instance."

If you need multiple unrelated gates, you're describing symptoms of a deeper missing invariant. Keep going.

## The depth floor — how to know you've gone too far

You've overshot when:

- The fix requires redesigning the entire system from scratch
- The cause is "the language/framework/platform doesn't prevent X"
- Enforcing the invariant would require simultaneous changes across more than ~3 independent systems
- The answer is effectively "we shouldn't have built it this way"

When you hit the depth floor: **back up 1–2 rungs on the ladder** and present that level as the practical root cause. Note that deeper causes exist but are outside practical fix scope.

The right depth is: the deepest rung where the answer still names something you can actually enforce.

## RCA ladder

Build in order. Evidence must come from logs, state, code, or tool output — not inference.

1. **Symptom** — What was observed?
2. **Immediate failure** — What command, prompt, state transition, model output, or process failed?
3. **Enabling condition** — Why was that failure allowed to happen or repeat?
4. **Failed guard/invariant** — What rule should have stopped it?
5. **Upstream admission failure** — Why did the work enter the wrong path before the visible failure?
6. **Recovery/detection gap** — Why did monitors/reconcilers/UI/agents fail to surface or resolve it automatically?
7. **Class-level cause** — What general design pattern makes this likely to recur?

At each rung: run the self-challenge loop before moving up. Stop when you pass it. Apply the depth floor test before presenting.

## Proximate-cause red flags

Treat these as incomplete until traced deeper:

- "The prompt told the agent to do it." → Why did policy allow that action?
- "The tool returned an error." → Why was the job left dispatchable after the error?
- "A flag said needs_review." → Was the flag binding in dispatch/admission/state?
- "The model made a bad judgment." → What deterministic guard or eval should bound that judgment?
- "It timed out." → Why did timeout recovery not transition, retry safely, or log a blocker?
- "The UI showed the wrong stage." → What state model conflates terminal/display/operational states?
- "We hit the cap." → What terminal path should own capped/exhausted work?

## Patch selection — after RCA is complete

Map the fix to the lowest enforceable layer. Prefer in order:

1. **State machine / transition contract** — impossible states become unrepresentable
2. **Central admission policy** — dispatchers ask one gate for allowed next actions
3. **Typed tool enforcement** — CLI/API refuses illegal actions, performs terminal transitions
4. **Autonomous resolver path** — agents resolve exhausted work with allowed terminal actions
5. **Prompt alignment** — prompts display only actions the state/tool layer allows
6. **UI/observability** — show the true blocker and invariant breach

Avoid: special cases, prompt scolding, longer timeouts, manual cleanup, one-instance patches — unless explicitly labeled temporary mitigation.

## Autonomous agentic systems

For autonomous agent workflows, do not default to human escalation for ordinary editorial or operational judgment. Exhaustion means: exit the normal loop and enter an autonomous resolution path owned by the responsible role. If the incident reveals a system bug, log it as a side effect, then still make the decision and move on.

Human attention is for infrastructure impossibility or genuine policy ambiguity — not ordinary operational taste.

## Required output shape

- **Current status / mitigation** — if live damage exists
- **Evidence trail** — concrete timestamps, IDs, commands, files, logs
- **RCA ladder** — with proximate / enabling / class-level causes distinguished
- **Self-challenge result** — what you tried and why it failed (proves you went deep enough)
- **Depth floor check** — did you hit it? If so, which rung did you back up to and why?
- **Why previous fix would be insufficient** — if relevant
- **Durable fix plan** — mapped to the lowest enforceable layer
- **Tests/evals/monitors** that would have caught this before the user did
- **Confidence and unknowns** — do not overclaim

## Bug log template

```
Title:
Affected IDs/scope:
Symptom:
Immediate failure:
Enabling condition:
Failed invariant:
Upstream admission failure:
Recovery/detection gap:
Class-level cause:
Self-challenge result: (what you tried, why it failed — proves depth)
Depth floor hit: (yes/no — if yes, which rung did you stop at and why)
Why edge-case patches are insufficient:
Recommended durable fix:
Regression/eval needed:
Evidence links/commands:
Confidence:
```
