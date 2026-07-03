---
id: unsanitized-user-path
date_observed: 2026-07-03
layer: process
canonical_layer: process
title: Unsanitized user path fixture
what_happened: A local path /Users/alice/private/project leaked into a pack-layer case.
failure_class: fixture
cost: none
gate_that_missed_it: fixture
eval_check: fixture
eval_type: checklist
plan_items:
  - R16a
status: seed
---

Invalid because `what_happened` contains a named user path.
