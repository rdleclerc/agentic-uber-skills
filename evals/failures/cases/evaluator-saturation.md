---
id: evaluator-saturation
date_observed: 2026-06-19
layer: process
canonical_layer: process
title: Gate that cannot say no
what_happened: An evaluator accumulated broad checks but stopped providing a calibrated rejection path for known-bad artifacts.
failure_class: saturated evaluator with no effective negative signal
cost: Agents could pass a process gate without meaningful evidence.
gate_that_missed_it: Quality/eval instrumentation accepted weak artifacts instead of forcing a rejection.
eval_check: R13 instrument-replacement known-bad skill fixture at tests/fixtures/skill_shape/bad-mini-skill plus shape-lint and pack battery tests.
eval_type: fixture
plan_items:
  - R13
status: eval_built
---

Canonical pack-layer case for evaluator saturation. The standing fix is to keep seeded known-bad fixtures and demote broad scoring instruments that cannot reject. R13 adds a deliberately bad mini-skill fixture that must be flagged by `lint_skill_shape.py` and must trip the pack word-budget, model-pin, and portability batteries when inserted into a pack skill slot.
