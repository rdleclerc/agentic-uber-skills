---
id: gaia-dialect-runtime-case
date_observed: 2026-07-03
layer: runtime
canonical_layer: runtime
title: Gaia dialect fixture
what_happened: Gaia-style INDEX rows include date segments and repo-prefixed canonical directories.
failure_class: index dialect drift
cost: Shared validation could reject a valid Gaia index.
gate_that_missed_it: Pack validator grammar omitted the Gaia runtime dialect.
eval_check: validate_failure_case.py --index gaia dialect fixture.
eval_type: fixture
plan_items:
  - G1
status: eval_built
---

Fixture for Gaia-style runtime-canonical INDEX rows.
