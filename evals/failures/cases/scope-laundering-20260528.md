---
id: scope-laundering-20260528
date_observed: 2026-05-28
layer: process
canonical_layer: process
title: Scope laundering through narrowing and self-certification
what_happened: A process run narrowed the operator's intended scope and then treated same-agent self-certification as sufficient proof.
failure_class: scope narrowing plus self-certification
cost: Rework risk and false confidence in completion.
gate_that_missed_it: Tier assignment and scope-fidelity review were not binding.
eval_check: Tier-assignment audit fixture in R7/R13.
eval_type: fixture
plan_items:
  - R7
  - R13
status: seed
---

Canonical pack-layer case for scope narrowing, self-down-tiering, and self-certification. The future eval should reject receipts that lack tier justification, reviewer tier check, and scope echo against the operator-original request.
