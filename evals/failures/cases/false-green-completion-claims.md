---
id: false-green-completion-claims
date_observed: 2026-07-03
layer: process
canonical_layer: process
title: Completion claimed from insufficient green proof
what_happened: Process runs can claim completion from a green command, shared proof spine, or parent-level receipt that does not exercise the actual user-visible, black-box, integration, eval, or target-system risk.
failure_class: false-green completion proof
cost: Operators receive completion confidence while the important outcome can still be missing.
gate_that_missed_it: Acceptance did not require proof tied to the intended operational outcome and skipped evidence-layer falsifiers.
eval_check: uberaccept/scripts/validate_acceptance_report.py requires reproduced_red or no_repro_reason for defect-fix claims, plus R13 false-green proof-ledger checks.
eval_type: fixture
plan_items:
  - R8
  - R13
status: eval_built
---

Canonical pack-layer case for false-green completion claims. Promote future lessons here when a run treats a convenient green check as proof of the actual outcome.

The durable check should force the artifact to name the baseline result, expected red/failing fixture when relevant, first green proof, black-box or user-visible proof, skipped evidence layers, and what would falsify the completion claim. For child-plan or shared-proof failures, use `references/operational-states.md` for terminal-state and parent-completion rules. Durable fixes should be template fields, validators, negative fixtures, or acceptance wording, not a hidden runtime controller, semantic judge, or new standalone testing skill from a single incident.
