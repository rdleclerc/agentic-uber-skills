---
id: install-drift-uberarchitect
date_observed: 2026-06-21
layer: process
canonical_layer: process
title: Installed skill drifted from source checkout
what_happened: A skill package could be updated in the repo while local runtime skill roots still pointed at an older or copied package.
failure_class: install drift without sync contract
cost: Agents could invoke stale skill instructions after source changes.
gate_that_missed_it: No install-sync check verified symlink targets across runtime roots.
eval_check: scripts/lint_pack_contract.py --install-sync --strict.
eval_type: executable
plan_items:
  - R4
status: eval_built
---

Canonical pack-layer case for install drift. The executable aggregator module checks pack skill directories against local Codex and Claude symlink installs.
