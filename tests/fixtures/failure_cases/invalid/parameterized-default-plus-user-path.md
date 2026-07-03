---
id: parameterized-default-plus-user-path
date_observed: 2026-07-03
layer: process
canonical_layer: process
title: Parameterized default hid separate user path
what_happened: The valid default ${X:-~/ok}/docs appeared on the same line as /Users/other/secret and must not exempt the second path.
failure_class: line-level portability exemption
cost: Private paths could pass sanitization.
gate_that_missed_it: The path sanitizer exempted an entire line.
eval_check: validate_failure_case.py path sanitizer fixture.
eval_type: fixture
plan_items:
  - R2
status: seed
---

Invalid fixture for per-match path sanitization.
