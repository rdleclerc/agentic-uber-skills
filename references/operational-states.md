# Operational States And Runtime Topology

Single home for Uber runtime topology, parent/child execution state, and active-vs-hard blocker rules.

## Runtime Topology Presets

Plan-tree depth and spawned-agent depth are different. Treat configured/reportable subagent limits as hard platform policy.

| Preset | Use | Limits | Approval |
|---|---|---|---|
| standard | default campaign and plan-tree work | `max_threads=6`, `max_depth=2`; L0 root -> L1 workstream -> L2 worker/reviewer | no extra approval |
| deep | work truly needs L0 -> L1 -> L2 -> L3 delegation | `max_threads=8`, `max_depth=3` | ask first, record approval, restore target |
| wide | unusually broad/deep campaign where 8/3 is insufficient | `max_threads=10`, `max_depth=3` | separate explicit approval |

Never silently raise thread/depth limits. Record approval, chosen preset, config backup path, queued/skipped/cap-hit lanes, restore target, and restore proof/blocker. Do not count failed, unavailable, queued, or cap-hit lanes as evidence.

Tier 2+ review-board agents inspect, challenge, and recommend. They mutate only when assigned disjoint write scope. The root orchestrator owns scope, decomposition, integration, acceptance, and final receipt. Workers return digest-only receipts: outcome, independent_review true/false, agent/session id, model/runtime, changed files, commands, receipts, key findings, risks/gaps, and next decision.

## Per-Child Terminal States

Every child plan records runtime topology, intended operational outcome, proof/blocker/re-scope evidence, remaining gap, and one terminal state:

- `operational` — the child reached its Operational Outcome Contract with target-system proof unless the child explicitly scoped a local/proof-only artifact as final.
- `blocked` — exact blocker, evidence, owner/prerequisite, and next unblock action are recorded.
- `re_scoped_with_approval` — the operator approved a smaller target before completion; the original outcome remains visible as deferred/not done.

Do not merge children into one shared proof layer. Root demos, shared safe proof spines, registries, readiness gates, plans, local-only proofs, eval fixtures, or shadow-only proofs do not complete children unless each child explicitly scoped that artifact as its final outcome.

## Blocked-State Taxonomy

Use this split for production/runtime implementation goals, long unattended goals, and external/unsafe/irreversible stop points:

- `active_blocked` — a child is blocked on one path but still has runnable safe next actions. It remains active work and cannot count toward parent completion.
- `hard_blocked_after_safe_action_exhaustion` — safe autonomous predecessor work is exhausted; the remaining blocker is exact, external/unsafe/irreversible or approval-owned; evidence and next unblock owner/action are recorded.

Blocked children with runnable safe next actions stay active. Continue safe predecessor work until no safe autonomous action remains.

## Parent Completion Conditions

A parent with children can proceed to acceptance or completion only when every required child is `operational`, `re_scoped_with_approval`, or `hard_blocked_after_safe_action_exhaustion`, and both counts are zero:

- active blocked children;
- runnable safe next actions.

For Tier 3 expensive-proof/replacement/runtime proof campaigns, do not proceed from one flat plan into burn-in or final proof. Require `$uberplan` expensive-proof preflight, child/status-ledger structure, burn-in vs final-proof separation, or recorded user-approved flat-plan bypass.
