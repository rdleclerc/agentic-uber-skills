---
id: claw1-path-rot
date_observed: 2026-06-20
layer: process
canonical_layer: process
title: Machine-specific paths in portable doctrine
what_happened: Portable skill text carried machine-specific absolute paths, making the pack appear configured while encoding one workstation's layout.
failure_class: portability rot through local absolute paths
cost: Fresh installs inherited stale or wrong path assumptions.
gate_that_missed_it: Path lint only checked existence on the current machine.
eval_check: validate_portability_oracle in scripts/lint_pack_contract.py.
eval_type: executable
plan_items:
  - R2
status: eval_built
---

Canonical pack-layer case for portability rot. The executable aggregator module rejects machine-specific `/Users/<name>/...` paths unless parameterized or fixture-marked.
