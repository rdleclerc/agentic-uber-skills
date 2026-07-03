---
id: unsanitized-title
date_observed: 2026-07-03
layer: process
canonical_layer: process
title: Local path /Users/alice/private leaked in title
what_happened: Sanitized case body.
failure_class: fixture
cost: Sanitization misses can leak operator-local context.
gate_that_missed_it: fixture
eval_check: fixture
eval_type: checklist
plan_items:
  - R16a
status: seed
---

Invalid because `title` contains a named user path.
