---
name: testing-strategy
description: "Use when an agent writes, removes, refactors, reviews, selects, or debugs tests, or decides which tests or product validation to run or whether they are needed. Do not use for command-only execution of an already specified test when no testing decision remains. Choose the smallest contract-preserving proof: one owner per contract, table-driven variants, current-checkout or installed-artifact evidence, and a named reason before escalating to broader suites."
---

# Testing Strategy

Choose proof that can fail for the changed behavior, then stop. More tests, more
reviews, and broader suites are not evidence unless they cover a distinct risk.

## Scope and lifecycle

- Run automatically for a testing or product-validation decision, inside or outside
  `$ubergoal`.
- Do not activate for command-only execution of an already specified test when no
  selection, debugging, escalation, or evidence-reuse decision remains.
- This is a utility, not an Uber lifecycle phase: it does not own goals, authorize
  changes, replace `$uberaccept`, or require a planning ceremony.
- Do not create a runner, framework, coverage target, or test inventory merely to
  apply this skill. It grants no authorization to delete tests, change CI, commit,
  push, or deploy.

## Production contract

- **Owned recurring job:** select or simplify proof for a changed contract without
  losing independent risk coverage.
- **Maturity, owner, targets:** Production; `agentic-uber-skills` maintainers;
  Codex, Claude, and SKILL.md-compatible coding agents.
- **Evaluation and review:** the data-only fixtures cover routing and output; review
  after a missed trigger, bad proof choice, or three real cleanup/selection runs.
- **Runtime caveat:** automatic discovery is host-dependent; when unavailable,
  load this SKILL.md explicitly rather than silently dropping the test decision.

## Decide whether a test is needed

First name the observable contract that changed and its failure signal.

- Add or change proof when behavior, a failure mode, a public/package boundary, a
  data transformation, or a regression contract changed.
- Usually do not add a test for formatting, comments, dead/unreachable code, or a
  rename that leaves all observable behavior unchanged. Say `test needed: no` and
  give the one-sentence reason; still run a formatter or type check only when that
  is the applicable product validation.
- If the change is only a hypothesis or the contract is unknown, inspect first.
  Do not manufacture unit cases to make progress look measurable.

## Give each contract one home

Map `changed seam → consumer/boundary → distinct failure class → proof owner`.
Keep one canonical test owner for a contract; remove or convert overlap only after
the successor proves the same contract.

- Test pure logic directly in the current checkout.
- Test package, build, plugin, or resolver delivery through the built or cleanly
  installed artifact and its first real call. A source-file assertion or mocked
  resolver is not a substitute when consumers load the artifact.
- Test an external integration at its actual boundary. Do not hard-code another
  workspace, runtime symlink, or local interpreter into a test to reach it.
- Keep source-text checks only when the source text itself is the contract (for
  example generated output or an intentionally static policy file).

## Keep distinct risks distinct

Table-drive values that take the same path, assert the same contract, and fail for
the same reason. Do not collapse independently meaningful dimensions merely to
reduce a test count: authorization, privilege/tenant isolation, source authority,
idempotency, destructive effects, money, and security boundaries need independent
proof where they differ.

For existing tests, classify each candidate as `keep`, `table-drive`, `move to the
right boundary`, `delete after successor proof`, or `defer`. A slightly different
input is not a distinct test if it only re-exercises the same rejection branch.

## Select proof with an escalation ladder

Run the first level that can falsify the changed contract; do not run every level
as ceremony.

1. Direct, focused contract test in the current checkout.
2. Boundary smoke: real package/build/install or first real call where that seam
   changed.
3. Focused suite for the affected component or integration.
4. Broad suite only for a named reachability, compatibility, shared-infrastructure,
   release, or explicit operator gate.

Reuse prior green evidence when the changed files and dependency path cannot reach
it. Rerun only when that path changed, the proof is nondeterministic or expired, a
new artifact was produced, or a required release gate says so. A tiny packaging or
metadata edit normally needs artifact proof, not a repeated broad source suite.

## Required proof choice

Before writing or running tests, state compactly:

- `changed seam` and `distinct failure class`;
- `test needed: yes/no`, including why;
- `selected proof` and exact target or command;
- `skipped proof` and why it would duplicate, miss, or overreach the contract;
- `escalation trigger` that would justify the next ladder level.

After cleanup, record the surviving contract owner and any deleted test's proven
successor. If no focused proof can be named, stop and report the missing boundary
or ask for direction instead of substituting a broad suite.

## Learning and retirement

Use `$uberskillevolver` to turn repeated missed contracts or bad selections into a
new fixture, not more default prose. Reassess after three real cleanup/selection
runs: if this utility adds ceremony without reducing duplicate execution,
wrong-artifact proof, or redundant branches, fold its useful checklist into
`$ubergoal`/`$uberplan` and retire it.

`evals/golden_skill_invocations.json` is data-only routing and output-fixture
coverage; use it when changing this skill's trigger or output contract.
