# Scope Artifact

Task slug: `adopt-matt-review-forge-techniques`
Created: `2026-06-20T10:43:33-07:00`
Owner/session: `Codex / goal 019ee589-8862-7491-af8d-29262435ea47`

## Original operator instruction

```text
Implement, have claude do adversarial review and manage acceptance, once satisfied merge, commit and push
```

## Explicit constraints and non-goals from original instruction

- Constraint: implement the previously assessed Matt Pocock / Review Forge adoption recommendations in `agentic-uber-skills`.
- Constraint: run Claude adversarial review before final acceptance.
- Constraint: manage acceptance before committing and pushing.
- Constraint: keep the work scoped enough to commit and push from this repo.
- Non-goal: create new `uber*` skills or import the external workflows wholesale unless review proves the existing skill surfaces cannot absorb the useful mechanics.
- Non-goal: mutate Gaia/OpenClaw runtime behavior or post to external systems.

## Scope change ledger

### 2026-06-20T10:43:33-07:00 - initial capture

- Source: original operator instruction plus immediately preceding `uberassess` comparison result.
- Change type: initial
- User instruction or artifact path: current conversation and `/tmp/uberassess-matt-review-forge-assessment.md` scratch assessment.
- Effect on scope: implement narrow skill-contract and eval improvements for pre-PRD grilling/domain capture, vertical issue slicing, AFK/HITL handoff, and spec-vs-standards acceptance review.
- Approval evidence for narrowing/deferral: n/a for initial capture; the preceding assessment explicitly recommended narrow adoption and the user instructed implementation.
