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
eval_check: scripts/validate_dispatch_ledger.py validates exit, output_path, and retry_count columns for dispatch terminal-state ledgers.
eval_type: executable
plan_items:
  - R12
  - R16a
status: eval_built
---

Canonical pack-layer case for subprocess terminality. `references/dispatch-and-sessions.md` now records the rule: assert exit codes and required output artifacts, never grep failure text as success evidence, retry once, then ledger the child terminal state and failure intake. `scripts/validate_dispatch_ledger.py` is the executable row-shape guard for the terminal-state fields.

Second instance (2026-07-03, b47849a): `pytest | tail -1` masked a failing suite behind the pipe exit code and a red commit was pushed; repaired same hour. Standing rule reinforced: assert on the command exit code, never on piped/grepped output — applies to orchestrator shell habits, not only dispatched pipelines.
