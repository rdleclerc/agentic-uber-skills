# Claude review packet

## Decision requested

Return `ACCEPT`, `FIX_WITHIN_SCOPE`, `REPLAN`, or `USER_DECISION` for the
uncommitted Tier 2 UberPlan/UberGoal/UberAccept candidate. Do not edit.

This is a re-review after
`coordination/uber-skills-56-eval-iteration/claude-review-2026-07-26.md`
returned `FIX_WITHIN_SCOPE`. Verify that all five findings there are resolved
without weakening the lean contract:

1. UberGoal has a compact implicit-trigger description and saved implicit
   trigger replay.
2. Goal-objective and Tier 0/1 work-contract authority pointers are reachable.
3. Tier 3 keeps review-board lanes while specialist lenses are risk-activated.
4. README skills-invoked wording applies only when a durable receipt activates.
5. The passing rejected-without-intake fixture lives under `fixtures/valid/`.

## Exact candidate

- Branch: `codex/uberplan-transfer-v1`
- Base: `c8469eec7297df7d420d528441d42d7662e76f48`
- UberPlan SHA-256 chunks: `d03b6a48f0a735d8` `b18a21986990a7f9` `38c0e040cbcc7a8c` `dd57fd97fedaf248`
- UberGoal SHA-256 chunks: `beb917b58ed412bc` `807b03fbcd1b9cc4` `4d72b94228dad1b2` `e7a8df9ba22be1d7`
- UberAccept SHA-256 chunks: `703c315578c04730` `ebb863ad285d6e10` `732d85a232e705b6` `2e09a76f1ed4bc6e`

Abort and regenerate the affected receipt if any hash differs.

## Read

1. `AGENTS.md`
2. `coordination/uber-skills-56-eval-iteration/scope.md`
3. `git diff` and `git status --short --branch`
4. `uberplan/SKILL.md`, `ubergoal/SKILL.md`, `uberaccept/SKILL.md`
5. Each suite manifest and `results/current-promotion.json`
6. UberAccept original/corrected rubrics, first blind receipt, and correction receipts
7. `coordination/uber-skills-56-eval-iteration/independent-review.md`
8. `coordination/uber-skills-56-eval-iteration/post-run-learning.md`
9. Changed validators and tests

## Reject conditions

- A promoted behavior lacks exact current-skill binding or complete declared
  working/holdout/forward/transfer coverage.
- Source-reading, causal completeness, authority, or safety was removed to save
  words/tools.
- Missing/unknown state can become accepted or authoritative rejected.
- `fix_within_scope`, `replan`, `user_decision`, unavailable gate, and
  authoritative rejection are conflated.
- Tier 2 recreates a review board, or contained acceptance requires universal
  evidence/report ceremony.
- A phrase/shape test is being presented as behavioral proof.
- Rubric correction erased the original expectation or first blind result.
- The diff widens into a new service, skill, harness, or unrelated pack rewrite.

## Current local proof

- UberPlan local validator tests: 43 pass.
- UberGoal local validator tests: 9 pass.
- UberAccept local validator tests: 38 pass.
- Behavioral boundary tests: 16 pass.
- Full pack suite: 81 pass, 1 skipped, and only the expected install-sync
  failure because live installs intentionally remain on the champion.
- Pack contract lint: pass; install-sync differences are reported because live
  installs intentionally remain on the champion.
- `git diff --check`: pass.
- Fresh-context Sol exact-diff review accepted UberPlan/UberAccept and the
  superseded UberGoal hash. Current-hash UberGoal coverage is supplied by the
  2026-07-26 Claude Opus rereview.

## Review output

State `lane_used`, model, exact files read, and one typed verdict. Findings need
file paths and the smallest correction. Treat the installed-symlink mismatch as
expected for an unpromoted worktree.
