---
id: dispatch-double-launch
date_observed: 2026-06-24
layer: process
canonical_layer: process
title: Dispatch without idempotency or single-writer claim
what_happened: Work dispatch could launch duplicate agents without a claim-before-launch ledger or duplicate-cull check.
failure_class: non-idempotent dispatch
cost: Duplicate work, conflicting writes, and unclear ownership.
gate_that_missed_it: No dispatch ledger enforced single-writer claims before launch.
eval_check: R12 dispatch-ledger validator and duplicate-cull fixture.
eval_type: executable
plan_items:
  - R12
status: seed
---

Canonical pack-layer case for duplicate dispatch. The future eval should require claim-before-launch, disjoint write scopes, and duplicate-cull evidence.
