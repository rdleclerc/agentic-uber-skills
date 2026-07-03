Implemented locally, with no git commands run. This is not self-approved; it is ready for the Tier-2 exact-diff and independent adversarial review lanes.

Word counts:
- `knowledge/coding-agent-operating-spine.md`: 1273 -> 1328, delta +55
- `AGENTS.md`: 1726 -> 1745, delta +19

Checks:
- `Review ladder (canonical`: exactly 1 in each file
- `Precedence with the Uber skill pack:`: exactly 1 in each file
- `python3 scripts/check_coding_agent_spine.py --json`: pass
- Spine contradiction flag: none found beyond the retained Claude lane policy, which is covered by the instruction that the spine keeps lane-policy ownership.

```diff
--- /tmp/gaia-spine.before.md
+++ knowledge/coding-agent-operating-spine.md
@@ -67,42 +67,35 @@
 ## Default High-Tier Review Lane
 
-For Gaia/OpenClaw coding tasks beyond the most minor edits, use the best
-available Claude review lane as a required gate unless Rob explicitly waives it
-in the task thread or coordination receipt. Default to:
+For Tier ≥1 Gaia/OpenClaw work, use the best available Claude review lane unless
+Rob explicitly waives it. Default to:
 
 ```sh
 claude --model opus --effort max
 ```
 
-`opus` is an alias for the current top Claude Opus-family model in the local
-Claude CLI. If that alias is unavailable, use the highest-capability Claude
-model available in the runtime and record the fallback. Do not silently
-downgrade. If no Claude review lane is reachable, stop before merge, commit, or
-completion claims and report that the work is locally verified only unless Rob
-explicitly waives the high-tier review gate.
+If `opus` is unavailable, use the highest-capability Claude model available and
+record the fallback. Do not silently downgrade. If no Claude review lane is
+reachable, stop before merge, commit, or completion claims and report local-only
+verification unless Rob waives the gate.
 
-This gate applies to substantive work that touches behavior, architecture,
-agent workflows, memory/source lanes, Slack-visible output, runtime state,
-provider/auth policy, scheduling, tests/evals, PRs, merges, or broad
-documentation policy. It is not required for the most minor edits, such as
-typo-only fixes, formatting-only changes, comments that do not alter policy, or
-a narrow doc pointer that does not change behavior.
+## Review ladder (canonical — pack skills and all coding agents point here)
 
-The high-tier lane must cover:
+| Tier | Work class | Required review |
+|---|---|---|
+| 0 | typo/cosmetic only — nothing that fixes observed misbehavior | none; commit carries a `tier0:` trailer |
+| 1 | contained single-surface change, clear tests | one exact-diff review pass by a capable lane, including a one-line scope echo against the operator-original ask |
+| 2 | cross-repo doctrine/pointer edits; behavior surfaces (prompts/skills/evals); medium-risk code | exact-diff review + independent adversarial lane (different vendor or fresh context) + scope-fidelity verdict |
+| 3 | production/runtime services; live-injected context surfaces; provider routing; security/data-subject surfaces; major refactor/deletion | full 4-phase ladder (plan review, exact-diff, adversarial, acceptance) on the highest-capability Claude lane + review-board lanes |
 
-- orchestration or plan review before substantial implementation, where
-  applicable
-- code review of the exact diff or candidate manifest
-- adversarial review of failure modes and missing tests
-- acceptance review after the relevant checks and proof receipts
+Riders: any surface injected into live OpenClaw session context additionally takes the GAIA_TESTING live-proof gate (those are runtime behavior changes, not doc edits). Tier assignment is auditable: every receipt records `tier` + a one-line justification; a reviewer's FIRST check is tier correctness, with bounce authority. If uncertain between tiers, take the higher.
 
-No implementing agent may self-approve substantial Gaia/OpenClaw work. Preserve
-the review receipt using the `Proof Receipts` contract below. For this
-high-tier review lane, also include the command/model, reviewed diff or
-candidate-manifest identity, checks run, verdict, blockers, and any fallback or
-waiver used.
+Precedence with the Uber skill pack: `ubergoal` wraps this spine's lifecycle for gaia work; the uber run receipt satisfies the spine receipt contract; `uberaccept` is the acceptance review; the claude-adversary lane is the required Tier-2+ independent lane and stays opt-in below Tier 2.
 
+No implementing agent may self-approve Tier ≥1. Review receipts use `Proof
+Receipts` and record command/model, reviewed diff or manifest identity, checks,
+verdict, blockers, and fallback/waiver.
+
@@ -185,8 +178,8 @@
 - result, blocker, and parity comparison
-- for high-tier review lanes: reviewed diff or candidate manifest, checks run,
-  verdict, blockers, fallback model/lane, and waiver if any
+- for review lanes: tier, justification, command/model, diff or manifest
+  identity, checks, verdict, blockers, fallback/waiver
```

```diff
--- /tmp/gaia-agents.before.md
+++ AGENTS.md
@@ -13,11 +13,10 @@
 
-For Gaia/OpenClaw coding tasks beyond the most minor edits, the operating spine
-requires the best available Claude Opus-family review lane at max effort for
-orchestration review, code review, adversarial review, and final acceptance
-unless Rob explicitly waives that gate.
+Review gates: `knowledge/coding-agent-operating-spine.md` §`Review ladder (canonical — pack skills and all coding agents point here)`.
 
+Precedence with the Uber skill pack: `ubergoal` wraps this spine's lifecycle for gaia work; the uber run receipt satisfies the spine receipt contract; `uberaccept` is the acceptance review; the claude-adversary lane is the required Tier-2+ independent lane and stays opt-in below Tier 2.
+
 Use the active repo root from `git rev-parse --show-toplevel` for code edits and commits.
```

