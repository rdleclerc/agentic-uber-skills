# Lifecycle authority

- `lifecycle.py` owns execution-tier and final-status policy.
- `runtime_adapter.py` is the direct consumer exposed to coding agents.
- `test_lifecycle.py` is the focused proof.
- Tier 2 requires exact-diff review plus exactly one independent risk-specific
  lane, not a default review board.
- Final outcomes are distinct: `accepted`, `fix_within_scope`, `replan`,
  `user_decision`, `blocked_with_failure_intake`, and authoritative `rejected`.
  Missing or unknown status fails closed.
- Planning never authorizes an external action. Executed actions require exact
  target and authorization, idempotency, rollback, execution receipt, and
  authoritative readback.
- Tier 3 retains plan review, exact-diff review, independent adversarial review,
  acceptance, rollback rehearsal, canary, and runtime readback.
- Agent-behavior proof must inspect ordered reads, actions, reviewers, and
  verdicts. A manifest or required phrase is not behavioral proof.
- UberRCA is a conditional utility and is outside this repair.
