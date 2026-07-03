---
id: unsanitized-body
date_observed: 2026-07-03
layer: process
canonical_layer: process
title: Unsanitized body fixture
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

Invalid because the Markdown body contains /Users/alice/private/secret.txt.
