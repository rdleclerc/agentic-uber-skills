# UberGoal champion/challenger comparison

## Binding

- Frozen champion: commit `c8469eec7297df7d420d528441d42d7662e76f48`,
  skill `e4d30ffe…eeb3`
- Selected challenger: skill `beb917b5…be1d7`
- Same working/holdout/forward fixtures and implicit trigger shape
- Fresh lanes did not read the competing skill, hidden rubrics, or prior results

## Decision-quality comparison

| Dimension | Frozen champion | Selected challenger | Verdict |
|---|---|---|---|
| Source reading | Reads decisive owners/evidence; avoids forbidden archive content | Same, with explicit named-source/owner/caller/proof rule | no regression |
| Scope | Mandatory `scope.md` can conflict with contained no-artifact plans | Durable scope ledger only when activated | challenger better |
| Lifecycle truth | Safe but varied prose; no literal non-complete state vocabulary | Literal `continue`, `ready_for_acceptance`, `replan`, `user_decision`, `blocked` | challenger better |
| External authority | Preserves authorization, rollback, receipt, readback | Same safeguards with literal `user_decision` | challenger better |
| Tier 2 review cost | Defaults to a bounded specialist board | Exactly one independent risk-specific lane | challenger better |
| Tier 3 safety | Retains full ladder and board | Retains full ladder/board; risk-activates specialist lenses | no regression |
| Implicit trigger | Triggers, but assumes at least Tier 2 and a board | Triggers, classifies actual surfaces, routes planning without premature execution | challenger better |
| Working execution | Both focused cases pass | Both focused cases pass with literal acceptance handoff | challenger better |

## Promotion verdict

Promote the challenger behaviorally. It preserves every material source,
authority, external-action, and Tier 3 protection exercised by the champion
while removing universal artifact/review ceremony and making non-complete
lifecycle states explicit. No case became shallower or less safe.

Raw sanitized receipts are
`baselines/champion-c8469eec.md` and `results/final-hash-replay.md`.
