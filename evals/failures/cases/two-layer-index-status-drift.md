---
id: two-layer-index-status-drift
date_observed: 2026-07-03
layer: both
canonical_layer: process
title: Shared failure case statuses drifted across indexes
what_happened: Pack and Gaia INDEX rows for shared failure ids diverged while each repo's local suite stayed green.
failure_class: two-layer catalog drift
cost: Operators could believe a case had an executable eval on one layer while the other layer still treated it as a seed.
gate_that_missed_it: Shared validation checked local file/index consistency but did not compare shared ids across INDEX files.
eval_check: scripts/validate_failure_case.py --index evals/failures/INDEX.md --cross-index ${GAIA_ROOT:-~/repos/agfunder-gaia}/evals/failures/INDEX.md.
eval_type: executable
plan_items:
  - G1
status: eval_built
---

Canonical process-layer case for two-layer INDEX status drift. Runtime and process indexes may own different canonical case bodies, but shared ids must not disagree on status. The durable check is the `--cross-index` validator mode plus a fixture that proves a divergence fails.
