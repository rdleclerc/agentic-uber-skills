# Wave 2 Dispatch 2 Deletion Receipt

| Removed block (first words + word count) | Invariant it carried | New home (file + anchor) | verified-present-there |
|---|---|---|---|
| For Tier 1+ coding, prompt... (76 words) | Tier 1+ coding/prompt/skill/workflow work uses the Coding Agent Work Contract unless risk routes to uberplan; parameterized guide/template paths stay available. | `ubergoal/SKILL.md#routing-table` | yes |
| Before implementation, run a Task... (245 words) | Task Understanding Review seven-question misunderstanding-prevention review, ambiguity gate, spec/code review split, and escalation from micro-intent. | `uberplan/SKILL.md#micro-intent--spec-first-fast-path-with-task-understanding-review` | yes |
| Lifecycle: Classify tier. Frame enough... (356 words) | Classify, frame, create/bind goal, plan by tier, execute with root ownership, adapt on test failure, ledger receipts, and route assess/simplify/accept/learn. | `ubergoal/SKILL.md#routing-table`; `ubergoal/SKILL.md#micro-intent-fast-path`; `ubergoal/SKILL.md#scope-artifact-gate`; `ubergoal/SKILL.md#completion-rule` | yes |
| Implementation effort recommendation Effort Use... (93 words) | Effort scales by tier and xhigh is only justified when smaller slices cannot preserve safety/progress. | `ubergoal/SKILL.md#review-ladder` | yes |
| Goal ownership ubergoal is a... (110 words) | Platform goal is a compact durable execution spine, not the whole plan; objective fields are validated and token budget is explicit-only. | `ubergoal/SKILL.md#routing-table`; `ubergoal/references/goal-objective.md`; `ubergoal/scripts/validate_goal_objective.py` | yes |
| Treat subagent/session limits as hard... (192 words) | Standard/deep/wide topology presets, approval/restore rules, review-board role, disjoint write scopes, digest-only receipts, and safe side-effect boundaries. | `references/operational-states.md#runtime-topology-presets` | yes |
| For multiple plans or an... (174 words) | Per-child terminal states, no shared parent proof substitution, active-vs-hard blocker taxonomy, and parent completion conditions. | `references/operational-states.md#per-child-terminal-states`; `references/operational-states.md#blocked-state-taxonomy`; `references/operational-states.md#parent-completion-conditions` | yes |
| When the goal is Tier... (57 words) | Architecture-shaped failures route to uberarchitect before local patches harden. | `ubergoal/SKILL.md#routing-table`; `uberarchitect/SKILL.md#uberarchitect` | yes |
| Use this only when the... (426 words) | Claude/cross-model adversary trigger, scope-fidelity packet, frame-independence, challenge format, reconciliation, and non-evidence rules. | `references/claude-adversary.md#cross-model-adversary-opt-in-contract`; `ubergoal/SKILL.md#optional-claude-adversary` | yes |

## Orchestrator verification (exact-diff review)

- All 9 deletion-receipt rows spot-checked: TUR present in uberplan/SKILL.md; operational-states.md (467 words) carries topology presets + blocked-state taxonomy + parent-completion rules; adversary contract pointer + 3 unique questions retained.
- ubergoal 2,767 → 786 words (budget ≤800, now lint-enforced). tier-ladder-table fingerprint MATCH on ubergoal.
- Fresh-agent routing smoke (sonnet lane, single-file read): 5/5 vs answer key, including both adversarial cases (provider-routing "quick fix" → Tier 3 escalation; repeated-timeout symptom-patching → uberarchitect stepback + uberrca). Transcript: session agent acc65416b8975c794.
- Packet self-contradiction flagged by implementer (no-git-commands vs git-show read) — resolved acceptably via drift fingerprint; orchestrator error, noted.

## Dispatch 7 receipt notes

- Logged policy reversal: uncertain-tier default flipped from lower to higher to prevent down-tiering; this is case 5 aligned with the spine review ladder.
- Deleted deferred-skills paragraph from `ubergoal`; surviving homes are `ROADMAP.md`, `uberplan`, and `uberskillevolver`.

## R9a Fresh-Session Orientation Smoke Record

- Formal smoke record: the Wave-2 acceptance reviewer verified R9a fresh-session orientation by direct read. `INIT.md` reaches the spine, testing doctrine, and review ladder in 1 hop, satisfying the planned <=3-hop reachability smoke for the coding-process cold-start path.
