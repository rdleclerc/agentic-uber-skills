# Plan Tree Artifact Layout

Use this when a plan creates child plans, subplans, or “plans that generate plans.” Keep the root small and put child proof in child artifacts so parent completion cannot hide shallow inner-loop work.

## Split trigger

Prefer a plan tree instead of one giant file when any of these are true:

- more than five child operational outcomes
- more than two execution levels
- multiple subagents or disjoint workstreams
- child plans have different proof/terminal-state requirements
- parent completion depends on child-specific operational proof

Keep a single file for Tier 0/1 work or one coherent implementation path.

## Directory shape

```text
plans/<goal-slug>/
  index.md                 # root plan, dependency graph, child registry
  status-ledger.md         # child terminal states and parent roll-up
  children/
    C1-<slug>.md
    C2-<slug>.md
  receipts/
    C1-acceptance.md
    C2-test-output.md
    final-acceptance.md
```

## Root `index.md` must contain

- objective, scope, non-goals, and Operational Outcome Contract
- dependency graph and recursive execution pseudocode
- child registry with path, owner, dependency, intended outcome, and terminal-state target
- pointer to `status-ledger.md`
- parent acceptance criteria and final acceptance receipt path
- rule that parent/shared proof cannot substitute for child proof

## Child plan files must contain

- parent link and child ID
- objective/scope/non-goals for that child
- child-specific Operational Outcome Contract
- proof required for `operational`, `blocked`, or `re_scoped_with_approval`
- tests/evals/live or target-system proof required
- receipt path and parent roll-up fields

## Status ledger must contain

| Child ID | Child plan path | Intended outcome | Terminal state | Evidence/receipt path | Blocker or re-scope approval | Parent impact |
|---|---|---|---|---|---|---|

Allowed terminal states: `operational`, `blocked`, `re_scoped_with_approval`.

## Anti-bloat rule

This is an artifact layout, not a runtime harness. Do not add a scheduler, controller, database, semantic judge, or hidden reviewer loop just because the plan is split into files. Agents still own execution judgment; the files make the work inspectable.
