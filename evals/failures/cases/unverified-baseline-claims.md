---
id: unverified-baseline-claims
date_observed: 2026-07-03
layer: process
canonical_layer: process
title: Structural decisions rested on unverified baseline claims
what_happened: A plan justified retirement and restructuring decisions on usage claims that had not been spot-checked against artifacts.
failure_class: unverified load-bearing evidence
cost: A useful skill could have been retired or misclassified.
gate_that_missed_it: Review protocol did not require checkable artifact paths for load-bearing baseline claims.
eval_check: R13 load-bearing evidence fixture.
eval_type: checklist
plan_items:
  - R8
  - R13
status: seed
---

Canonical pack-layer case for unverified baseline claims. The durable check is to require artifact paths for load-bearing evidence and reviewer spot-checks before structural decisions.

Second observed instance: a dispatch-3 result receipt claimed `eval_built=3` and case 15 still seeded, while the landed tree had 4 `eval_built` cases including case 15; the receipt/diff mismatch was caught in Wave-1 review.

Third observed instance (case 20): the R8 ubershow retirement sweep claimed no real artifact because it searched only the conventional `coordination/<task>/ubershow/` directory shape. A content-marker search later found `${GAIA_ROOT:-~/repos/agfunder-gaia}/coordination/gaia-brain-wisdom-event-graph-activegraph/p0-wisdom-grading-board-2026-05-31.html` with `data-artifact-kind="ubershow-decision-board"` and its sibling receipt with `selected_decision: proceed_to_p1_minimal_candidate_design`, flipping the keep/archive recommendation.

Fourth observed instance: `coordination/process-rearchitecture-202607/wave3-dispatch1.md:18` claimed the reproduced-red receipt was already validator-defined. A direct validator/template search found no `reproduced_red` field or check before G2 added it.
