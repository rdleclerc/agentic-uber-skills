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
eval_check: scripts/validate_dispatch_ledger.py validates required dispatch ledger rows and rejects duplicate non-retry work_item rows.
eval_type: executable
plan_items:
  - R12
status: eval_built
---

Canonical pack-layer case for duplicate dispatch. `references/dispatch-and-sessions.md` now names the checklist: claim before launch, one dispatch per work item, duplicate cull before work starts, and a ledger row that survives orchestrator handoff. `scripts/validate_dispatch_ledger.py` is the executable check for the row shape and duplicate-cull rule.
