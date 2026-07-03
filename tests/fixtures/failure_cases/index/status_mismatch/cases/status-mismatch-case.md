---
id: status-mismatch-case
date_observed: 2026-07-03
layer: process
canonical_layer: process
title: Status mismatch case
what_happened: A case file status disagreed with its local canonical index row.
failure_class: index status mismatch
cost: Receipts could count the wrong executable evals.
gate_that_missed_it: No status agreement check.
eval_check: validate_failure_case.py --index fixture.
eval_type: fixture
plan_items:
  - R16a
status: eval_built
---

Fixture case.
