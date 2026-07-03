---
id: unsanitized-cost
date_observed: 2026-07-03
layer: process
canonical_layer: process
title: Unsanitized cost fixture
what_happened: Sanitized case body.
failure_class: fixture
cost: Rotation work exposed /Users/alice/private/secret.txt in cost notes.
gate_that_missed_it: fixture
eval_check: fixture
eval_type: checklist
plan_items:
  - R16a
status: seed
---

Invalid because `cost` contains a named user path.
