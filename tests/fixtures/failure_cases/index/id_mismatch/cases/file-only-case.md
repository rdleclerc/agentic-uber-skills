---
id: file-only-case
date_observed: 2026-07-03
layer: process
canonical_layer: process
title: File only case
what_happened: A case file existed without a local canonical index row.
failure_class: index id mismatch
cost: Catalog rows could disappear from the index.
gate_that_missed_it: No index consistency check.
eval_check: validate_failure_case.py --index fixture.
eval_type: fixture
plan_items:
  - R16a
status: seed
---

Fixture case.
