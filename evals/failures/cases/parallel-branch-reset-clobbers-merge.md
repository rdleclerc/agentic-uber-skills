---
id: parallel-branch-reset-clobbers-merge
date_observed: 2026-07-03
layer: both
canonical_layer: process
title: Parallel branch reset clobbered a merged wave commit
what_happened: A parallel session's branch-reset workflow dropped an already-merged wave commit from the shared main ref and pushed the loss; zero CI signal fired because the new tree had no test reference; the Tier-2 adversarial review caught it with an ancestor check.
failure_class: ref-level lost-update between parallel sessions
cost: A landed wave could be reported complete while the shared branch no longer contained the work.
gate_that_missed_it: Wave push protocol lacked a landed-SHA ancestor check, and cross-repo suite wiring did not make the missing tree loud.
eval_check: Wave-push protocol asserts each landed SHA is ancestor of the target branch tip before a wave is declared landed; cross-repo suite wiring makes the tree loud.
eval_type: checklist
plan_items:
  - R12
status: seed
---

Canonical pack-layer case for parallel ref-level lost updates. The durable check belongs in the orchestrator push protocol, with the Gaia-side suite wiring as the cross-repo signal.
