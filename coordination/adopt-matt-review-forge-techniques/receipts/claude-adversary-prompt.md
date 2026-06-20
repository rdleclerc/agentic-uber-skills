Operator original instruction, verbatim:

```text
Implement, have claude do adversarial review and manage acceptance, once satisfied merge, commit and push
```

You are Claude running an adversarial review for Codex. Accept, modify, or refuse that role before any approval language. Codex remains owner and reconciler; do not edit files. Review the candidate diff and return only findings/review text.

## Section 1: Scope Fidelity Packet

Scope artifact: `coordination/adopt-matt-review-forge-techniques/scope.md`

Read that file and answer:

- Original-scope satisfaction: Does the candidate diff satisfy the operator-original instruction?
- Narrowing approval: If scope is narrowed, was that narrowing explicitly operator-approved? Cite evidence.
- Scope fidelity verdict: pass / fail / uncertain.

Also answer the frame-independence check before approval language:

1. Invited role: what role is Codex asking you to play, and should you accept, modify, or refuse it?
2. Original-vs-summary gap: what does the operator's original instruction require that Codex's summary, plan, or terminology might hide, narrow, or skip?
3. Reject conditions: name three concrete outcomes that would make you reject this work.

## Section 2: Artifact Under Review

Candidate diff artifact: `coordination/adopt-matt-review-forge-techniques/receipts/candidate.diff`

Relevant local files in the diff:

- `uberplan/SKILL.md`
- `uberplan/templates/plan-contract.md`
- `uberplan/evals/golden_skill_invocations.json`
- `uberplan/tests/test_validators.py`
- `uberaccept/SKILL.md`
- `uberaccept/templates/final-acceptance.md`
- `uberaccept/evals/golden_skill_invocations.json`
- `uberaccept/scripts/validate_acceptance_report.py`
- `uberaccept/tests/test_validators.py`
- `uberaccept/tests/fixtures/valid/final_acceptance.md`
- `uberaccept/tests/fixtures/valid/production_hard_blocked_acceptance.md`

## Review Task

Assess whether the diff correctly implements narrow adoption of Matt Pocock / Review Forge techniques into existing Uber skills without importing a parallel workflow.

Known intended behavior:

- `uberplan` should gain pre-PRD interrogation/domain capture guidance: one blocking question at a time, recommended answer, code/doc inspection when possible, and a guardrail against using glossary/context docs as PRDs/status logs.
- `uberplan` should gain vertical PRD-to-issue slicing guidance: tracer-bullet issues, dependencies, acceptance evidence, AFK/HITL boundaries, and no horizontal tickets when end-to-end slices are possible.
- `uberaccept` should separate spec fidelity from repo standards, with validator/template/eval coverage so standards-only review cannot masquerade as product correctness.
- The patch should not create new skills or broad machinery.

## Required adversarial questions

Answer each with causal layer, evidence, and minimum impact:

1. Receipt reproducibility. Are receipts reproducible by deterministic tool output, or are they model summaries?
2. Scope/diff match. Does the diff match stated scope? Name any out-of-scope change.
3. Inherited assumption. What assumption does the next task inherit that could be wrong?

Then answer:

Ship: yes/no, one sentence.

If you raise challenges, format each as:

- Claim
- Causal layer
- Why it matters
- Falsifying/satisfying evidence
- Minimum impact threshold
