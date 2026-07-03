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
eval_check: "references/dispatch-and-sessions.md#dispatch-mechanics and #dispatch-ledger checklist for exit-code assertions, required artifacts, and retry-once-then-ledger; wrapper validator not built."
eval_type: checklist
plan_items:
  - R12
  - R16a
status: seed
---

Canonical pack-layer case for subprocess terminality. `references/dispatch-and-sessions.md` now records the rule: assert exit codes and required output artifacts, never grep failure text as success evidence, retry once, then ledger the child terminal state and failure intake. This remains `seed` until a wrapper validator exists.
