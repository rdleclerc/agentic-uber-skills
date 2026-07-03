Implemented and locally verified only.

Files created/changed:
- [failure_evals.test.mjs](/Users/rob/repos/worktrees/gaia-failure-evals-reland/tests/integration/failure_evals.test.mjs)
- [INDEX.md](/Users/rob/repos/worktrees/gaia-failure-evals-reland/evals/failures/INDEX.md)
- [PARALLEL-SESSION-NOTE-failure-evals-reland-2026-07-03.md](/Users/rob/repos/worktrees/gaia-failure-evals-reland/coordination/PARALLEL-SESSION-NOTE-failure-evals-reland-2026-07-03.md)

Test output:

```text
TAP version 13
# Subtest: failure cases validate with the process-pack validator
ok 1 - failure cases validate with the process-pack validator
  ---
  duration_ms: 33.331292
  type: 'test'
  ...
# Subtest: failure INDEX mirrors local runtime cases and frontmatter
ok 2 - failure INDEX mirrors local runtime cases and frontmatter
  ---
  duration_ms: 1.041375
  type: 'test'
  ...
1..2
# tests 2
# suites 0
# pass 2
# fail 0
# cancelled 0
# skipped 0
# todo 0
# duration_ms 97.709875
```

Contradictions flagged:
- Repo instructions ask for git-root/writeability checks, but your dispatch said no git commands. I ran no git commands.
- Repo instructions ask for `memory/live-context.md` read/append, but that file is absent and your dispatch said touch only the four deliverables. I did not create or touch it.
- Required Claude review lane was not reachable: local Claude is installed but not logged in, and `type0` / `agclaw` do not resolve from this runtime.