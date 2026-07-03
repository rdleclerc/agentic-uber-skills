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
eval_check: "references/dispatch-and-sessions.md#dispatch-mechanics and #dispatch-ledger checklist for claim-before-launch, one row per work item, and duplicate cull; validator not built."
eval_type: checklist
plan_items:
  - R12
status: seed
---

Canonical pack-layer case for duplicate dispatch. `references/dispatch-and-sessions.md` now names the checklist: claim before launch, one dispatch per work item, duplicate cull before work starts, and a ledger row that survives orchestrator handoff. This remains `seed` until an executable validator exists.
