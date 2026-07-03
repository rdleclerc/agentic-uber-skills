---
id: doctrine-drift-trio
date_observed: 2026-06-22
layer: process
canonical_layer: process
title: Duplicated doctrine drifted across surfaces
what_happened: The same rule lived in multiple doctrine files and could be edited in one place while remaining stale elsewhere.
failure_class: duplicated policy drift
cost: Agents received conflicting or stale process authority.
gate_that_missed_it: No owned fingerprint registry asserted canonical wording across copies.
eval_check: scripts/lint_pack_contract.py --drift --strict.
eval_type: executable
plan_items:
  - R3
  - R5
status: eval_built
---

Canonical pack-layer case for doctrine drift. The executable drift registry starts report-only and becomes blocking after the adoption wave.
