---
id: scope-laundering-20260528
date_observed: 2026-05-28
layer: process
canonical_layer: process
title: Scope laundering through narrowing and self-certification
what_happened: A process run narrowed the operator's intended scope and then treated same-agent self-certification as sufficient proof.
failure_class: scope narrowing plus self-certification
cost: Rework risk and false confidence in completion.
gate_that_missed_it: Tier assignment, scope-fidelity review, and reviewer frame-independence were not binding.
eval_check: R7/R13 tier-assignment and scope-fidelity fixtures requiring operator-original scope echo and reviewer first-check.
eval_type: fixture
plan_items:
  - R7
  - R13
status: seed
---

Canonical pack-layer case for scope narrowing, self-down-tiering, reviewer frame adhesion, and self-certification. The future eval should reject receipts that lack tier justification, reviewer tier check, and scope echo against the operator-original request.

Promoted fossil lessons from `uberskillevolver`: a scope-fidelity learning record must preserve the operator original instruction, agent-interpreted scope, proposed narrowed scope, explicit deferrals/non-goals, approval evidence, original-vs-summary diff, reviewer scope-fidelity verdict, and what would have blocked mistaken sign-off. For frame-adhesion failures, the reviewer prompt must name the invited role, state the original-vs-summary gap, list three reject conditions before approval language, and preserve the caveat that model review is reduced-noise rather than a replacement for human spot-checks or observable success criteria. Hidden semantic judges, persistent debate harnesses, and broad reviewer bureaucracy are explicitly not the durable fix.
