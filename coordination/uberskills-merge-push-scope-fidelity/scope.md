# Scope Artifact

Task slug: `uberskills-merge-push-scope-fidelity`
Created: `2026-05-28T08:00:00-0700`
Owner/session: `uberskills-merge-push`

## Original operator instruction

```text
Update the Uber skills to prevent scope laundering and ignored skill directives.

Context:
A recent `ubergoal`/`uberplan`/`uberaccept` run violated scope fidelity. The operator asked for a codebase-wide OpenClaw ownership audit and implementation, but Codex narrowed the work to a Slack/transcript patch, asked Claude to review only that narrowed patch, then marked the goal complete. This violated the existing Uber skill requirements that Claude/adversary review be anchored to the operator-original instruction.

Goal:
Implement the smallest durable change that materially prevents this recurrence. Do not add another reminder line that can get lost. Make scope fidelity a required artifact and structural acceptance gate.

Required design:
1. `ubergoal` must create or update `coordination/<task-slug>/scope.md` for Tier 1+ or explicit `ubergoal` work.
   - It must contain the operator’s original instruction verbatim.
   - It must preserve explicit constraints and later user scope changes as dated entries.
   - Later entries append; they do not overwrite the original scope.

2. `uberplan` must require a `## Scope fidelity` block in durable plans.
   It must include:
   - `Original scope:` quote or link to `scope.md`
   - `Plan scope:`
   - `Narrowing? yes/no`
   - `Operator approved narrowing in:` quote/link, required if narrowed
   - If narrowing is unapproved, plan is invalid / cannot proceed as completion.

3. `uberaccept` must require a `## Scope fidelity verdict` before any `SHIP`, completion, or goal-complete language.
   It must:
   - Quote or link to `scope.md`, not only the plan summary.
   - Answer whether implemented scope satisfies original scope.
   - Cite approval for any narrowing.
   - Treat unapproved narrowing as a blocker.

4. Add a small structural validator, e.g. `scripts/check_scope_fidelity_artifacts.py`.
   Keep it presence-only and non-semantic. It should fail when:
   - `scope.md` is missing.
   - acceptance/final report lacks `## Scope fidelity verdict`.
   - `SHIP` appears before the scope-fidelity verdict.
   - `Narrowing? yes` appears without a non-empty approval citation.
   Do not attempt to semantically compare original vs implemented scope.

5. Add or update templates so agents do not have to remember the format:
   - scope artifact template if appropriate
   - plan contract scope block
   - final acceptance scope verdict block
   - Claude/adversary prompt template should load `scope.md` as section 1 and diff/artifact under review as section 2.
   - Save generated Claude/adversary prompts into the coordination folder when used.

6. Add focused tests or fixtures:
   - Regression: original scope says “codebase-wide OpenClaw ownership audit,” plan/acceptance narrows to Slack-only with no approval; validator fails.
   - Legitimate narrowing: operator explicitly approves narrowing to Slack; validator passes.
   - SHIP before scope verdict; validator fails.

Ownership constraints:
- Agent/reviewer owns semantic judgment about whether implemented scope truly satisfies original scope.
- Uber skill text owns workflow obligations.
- Durable artifacts own the preserved operator instruction and scope ledger.
- Validator owns structural presence/order checks only.
- Do not build a deterministic semantic judge.
- Do not create a new top-level `uberscope` skill unless unavoidable.
- Keep changes surgical and avoid broad skill bloat.

Use Claude adversarial review if available, but make sure Claude receives this prompt and the relevant skill files, not a narrowed summary. Final output should include changed files, tests run, and any residual risk.
```

## Explicit constraints and non-goals from original instruction

- Constraint: smallest durable structural artifact/gate; avoid reminder-only patch.
- Constraint: validator is structural/presence/order only, not semantic comparison.
- Constraint: no new top-level `uberscope` skill unless unavoidable.
- Constraint: keep changes surgical and avoid broad skill bloat.
- Non-goal: deterministic semantic scope judge.
- Non-goal: OpenClaw/Type0 runtime changes.

## Scope change ledger

### 2026-05-28T08:00:00-0700 — initial capture

- Source: original operator instruction
- Change type: initial
- User instruction or artifact path: this file, original instruction block above
- Effect on scope: implement structural scope artifact/gate in existing Uber skills and validator/tests
- Approval evidence for narrowing/deferral: n/a for initial capture

### 2026-05-28T12:58:00-0700 — Operator scope addition: V0 premortem / Claude recs / overengineering

```text
"I slightly disagree with Claude’s wording “make the adversary question mandatory” if that implies mandatory external Claude review. I’d make the premortem block mandatory, while external Claude stays optional unless requested." -- disagree...  okay include the overengineering part and claudes recs, use uberskills and claude to build
```

- Scope change: extend the in-progress Uber skills patch to add a durable `uberplan` V0 premortem / failure-disposition gate, including overengineering/code-bloat failure analysis and Claude's recommendation that adversary failure questions become load-bearing for Tier 2+ plans.
- Constraint preserved: keep the change surgical; do not create a new top-level skill; avoid broad ceremony or semantic deterministic judgment.
- Review requirement: use Claude OAuth review on the actual updated artifacts, with prompt saved in the coordination folder.
