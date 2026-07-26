# Failure intake

- failure_case_id: `claude-opus-quota-2026-07-25`
- Gate: required Tier 2 highest-capability available Claude review
- Local Opus attempt: `claude --model opus --effort max` -> weekly limit reached
- Local Sonnet fallback attempt: `claude --model sonnet --effort max` -> same weekly limit
- Documented remote `type0` lane: unavailable because the host alias cannot be resolved from this machine
- Documented remote `agclaw` lane: unavailable because the host alias cannot be resolved from this machine
- Third consecutive goal-turn audit: the exact Opus, Sonnet, `type0`, and `agclaw` attempts above were repeated against the unchanged review packet on 2026-07-25 with the same results
- 2026-07-26 retry: local `claude-opus-5` became reachable and returned
  `FIX_WITHIN_SCOPE`; receipt:
  `coordination/uber-skills-56-eval-iteration/claude-review-2026-07-26.md`
- Gate resolution: local Claude Opus became reachable on 2026-07-26; the
  current-hash rereview satisfied the required lane after receipt-only
  corrections documented in `claude-rereview-2026-07-26.md`
- Candidate mutation caused by failure: none
- Resolution evidence: local structural checks, behavioral
  working/holdout/forward/transfer receipts, current-hash Claude Opus rereview,
  and receipt corrections are complete
- Remaining action for this historical case: none; final UberAccept runs under
  the parent goal, not this resolved failure case
- Historical restriction while unresolved: install, commit, merge, final
  promotion, and platform-goal completion were forbidden
