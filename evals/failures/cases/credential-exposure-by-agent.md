---
id: credential-exposure-by-agent
date_observed: 2026-07-03
layer: process
canonical_layer: process
title: Secret material echoed into artifacts
what_happened: An agent could echo credential-like values into transcripts or artifacts, forcing rotation instead of using approved secret references.
failure_class: credential exposure in agent artifacts
cost: Secret rotation and loss of trust in transcript safety.
gate_that_missed_it: No pack-layer secret-pattern scan over doctrine, coordination, and eval artifacts.
eval_check: scripts/lint_pack_contract.py --secret-scan --strict.
eval_type: executable
plan_items:
  - R16a
status: eval_built
---

Canonical pack-layer case for credential exposure. The Wave-1 scan is report-only by default; strict mode is available before it becomes blocking in a later wave.
