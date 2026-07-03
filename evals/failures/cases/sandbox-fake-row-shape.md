---
id: sandbox-fake-row-shape
date_observed: 2026-06-23
layer: process
canonical_layer: process
title: Fake interface rows encoded author assumptions
what_happened: A sandbox fake stood in for an external interface but did not prove its row shape matched the real interface.
failure_class: sandbox-blind interface fake
cost: Local tests could pass while integration failed on real data shape.
gate_that_missed_it: Acceptance did not require an interface-shape receipt for fakes.
eval_check: uberaccept/scripts/validate_acceptance_report.py requires interface_shape_receipt when fakes/stubs/mocks stand in for external interfaces.
eval_type: fixture
plan_items:
  - R12
status: eval_built
---

Canonical pack-layer case for fake interface shape. `references/dispatch-and-sessions.md` is the contract home: external-interface or DB fakes need shape evidence from the real interface before a sandbox pass can support an integration claim. The acceptance validator now rejects reports that mention such stand-ins without an `interface_shape_receipt`.
