---
id: subprocess-dies-without-terminal-state
date_observed: 2026-07-03
layer: process
canonical_layer: process
title: Dispatched subprocess exited without a truthful terminal state
what_happened: A dispatched subprocess exited nonzero without an expected output artifact or terminal message, and only a retry revealed the path.
failure_class: dispatch without terminal-state contract
cost: One lost review run of roughly fifteen minutes.
gate_that_missed_it: Dispatch wrapper did not require exit-code plus expected-output checks before ledgering the child.
eval_check: R12 dispatch wrapper exit-code and expected-output fixture.
eval_type: executable
plan_items:
  - R12
  - R16a
status: seed
---

Canonical pack-layer case for subprocess terminality. The future dispatch wrapper should retry once, then ledger the failure intake with the child terminal state.
