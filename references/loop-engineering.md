# Loop Engineering Reference

Use this reference when an Uber run becomes a recurring, scheduled, watch-and-fix, or unattended agent loop. Keep it as a shared reference so `ubergoal`, `uberplan`, `uberaccept`, and `uberskillevolver` do not each grow duplicate loop prose.

## Source-derived frame

Loop engineering is one layer above a single agent harness. The harness equips one run; the loop wakes it, gives it work, verifies it, persists state, and decides whether to run again. The useful abstraction is not a new while-loop. The useful abstraction is the operating contract around the loop.

Use the Orange Book / loop-engineering source model as a checklist, not a ceremony generator. The smallest useful loop has a trigger, a discovery source, isolated handoff, verification, durable state, and a next-step decision. If any part is missing, keep the work as a manual goal or one-shot automation until the missing part exists.

## Five moves of one loop

1. **Discovery** — find this turn's work without a human manually listing each item. Examples: CI failures, open issues, recent commits, queue rows, alerts, inbox items, drift reports.
2. **Handoff** — isolate each actionable item before work starts. Use a worktree, thread, child plan, ticket, or explicit disjoint write scope.
3. **Verification** — install something that can say no. Prefer deterministic tests/builds/type checks. If judgment is required, use an independent maker/checker split and cite the rubric.
4. **Persistence** — write state outside the chat: markdown ledger, issue tracker, queue row, database, PR, receipt, or artifact path. The next turn must resume from this state, not from model memory.
5. **Scheduling / next decision** — decide whether to continue, sleep until the next trigger, stop complete, stop blocked, stop exhausted, or ask for approval.

## Six parts to check before launch

| Part | Loop question | Minimum acceptable answer |
|---|---|---|
| Automation / trigger | What wakes it? | schedule, event, queue, monitor, or explicit operator wakeup |
| Work isolation | How do parallel or repeated runs avoid collisions? | worktree, disjoint write set, lock, idempotency key, or single-run cap |
| Skill / context | What stable procedure/context does every run load? | named skill, compact contract, or reference; not a pasted wall of prompt |
| Connector / tool surface | What real systems can it inspect or mutate? | smallest focused tools with typed inputs, safe errors, and permission boundaries |
| Verifier / critic | What can reject bad work? | deterministic gate or independent checker; never maker-only self-review |
| Durable memory | Where does state survive? | ledger/issue/queue/receipt that the next run reads first |

## Loop Contract fields

Use these fields in `uberplan` when the plan is recurring, scheduled, watch-and-fix, or unattended:

- Loop mode: manual continuation / scheduled / event-triggered / queue-driven / monitor / background goal.
- Trigger and cadence: exact schedule, event source, queue query, or wakeup condition.
- Discovery source: what the loop reads to decide whether work exists.
- Handoff and isolation: worktree/thread/ticket/child-plan/write-scope strategy.
- Verification gate: deterministic command, evaluator, rubric, or human-review gate.
- Durable state: file/board/database/receipt path and schema.
- Stop conditions: complete, no work, blocked, budget exhausted, no progress, repeated failure, approval needed, safety boundary.
- No-progress rule: what repeated tool call, repeated diff, repeated failure family, or unchanged state proves spinning.
- Budget caps: per-run token/time/cost/retry limits plus daily/weekly ceiling when recurring.
- Idempotency and side effects: keys, dry-run mode, replay behavior, duplicate suppression, rollback.
- Human attention policy: what is silent, what goes to triage, what wakes a human, and maximum notification cadence.
- Comprehension-debt control: what output a human must spot-check and how often.
- Learning path: which findings become eval seeds, validators, templates, deletions, or `uberskillevolver` records.

## Acceptance lens

A loop is not accepted because an agent says it is done. `uberaccept` should look for:

- per-iteration receipts or a representative sampled receipt set;
- independent verification, not maker-only self-review;
- correct-stop proof for complete/no-work/blocked/exhausted/approval-needed states;
- no-progress and budget kill-switch evidence;
- replayable state that prevents the next run from starting from scratch;
- idempotency for repeated side effects and duplicate suppression for writes;
- human approval before irreversible merge, deploy, publish, payment, credential, data-loss, or external-send actions;
- an explicit statement of what the loop must never do unattended.

## Costs and anti-bloat guard

Loop engineering has four recurring costs: verification debt, comprehension rot, cognitive surrender, and token/cost blowout. A proposed loop should be rejected or downgraded when the task is one-off, verification is weak, budget is unclear, side effects are not idempotent, or the real problem is product judgment rather than repeated machine-checkable work.

Do not extract a standalone `uberloop` skill from this reference until repeated real runs prove extraction makes the common path smaller, faster, or safer. Promotion trigger: at least three real loop-building runs show the same loop contract being re-derived from scratch, or a loop-specific failure recurs because guidance is too hidden inside existing skills.
