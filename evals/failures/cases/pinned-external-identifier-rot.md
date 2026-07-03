---
id: pinned-external-identifier-rot
date_observed: 2026-07-03
layer: process
canonical_layer: process
title: Hardcoded external identifiers aged into drift
what_happened: Doctrine enforced a literal external identifier instead of an alias or policy, risking silent downgrade or obsolete routing.
failure_class: pinned external identifier rot
cost: Agents could preserve stale model or vendor identifiers as policy.
gate_that_missed_it: Pack lint enforced a specific literal instead of prohibiting hardcoded model ids.
eval_check: scripts/lint_pack_contract.py model-pin prohibition fixture.
eval_type: executable
plan_items:
  - R1
status: seed
---

Canonical pack-layer case for hardcoded external identifiers. Existing pack lint rejects model ids in skill frontmatter; broader doctrine identifier policy remains a later R13 class eval.
