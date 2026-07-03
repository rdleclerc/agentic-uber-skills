Implemented R6 in the pack repo only, with no git commands.

Key changes:
- Rewrote [ubergoal/SKILL.md](/Users/rob/repos/agentic-uber-skills/ubergoal/SKILL.md) to 786 words.
- Added [references/operational-states.md](/Users/rob/repos/agentic-uber-skills/references/operational-states.md) as the single home for runtime topology, child terminal states, and active/hard blockers.
- Added tiered templates: [plan-tier1.md](/Users/rob/repos/agentic-uber-skills/uberplan/templates/plan-tier1.md), [plan-tier3.md](/Users/rob/repos/agentic-uber-skills/uberplan/templates/plan-tier3.md), and a 3-line tombstone at [plan-contract.md](/Users/rob/repos/agentic-uber-skills/uberplan/templates/plan-contract.md).
- Added `--tier tier1|tier3` support to [validate_plan_contract.py](/Users/rob/repos/agentic-uber-skills/uberplan/scripts/validate_plan_contract.py), while preserving numeric tier modes.
- Added [evals/routing/answer-key.md](/Users/rob/repos/agentic-uber-skills/evals/routing/answer-key.md).
- Added the `ubergoal/SKILL.md <= 800` word-budget check and failing test fixture path.
- Added deletion receipt: [wave2-d2-deletion-receipt.md](/Users/rob/repos/agentic-uber-skills/coordination/process-rearchitecture-202607/wave2-d2-deletion-receipt.md).

Verification:
- `python3 scripts/lint_pack_contract.py` passed.
- `python3 -m unittest discover -s tests -v` passed: 48 tests, 1 skipped because `.git` is not writable.
- `python3 -m unittest discover -s ubergoal/tests -v` passed: 9 tests.
- `python3 -m unittest discover -s uberplan/tests -v` passed: 43 tests.
- `python3 ubergoal/scripts/validate_goal_objective.py --help` ran successfully.
- `python3 uber-skill-creator/scripts/quick_validate.py ubergoal` passed.
- `python3 uber-skill-creator/scripts/quick_validate.py uberplan` passed.
- Drift: `tier-ladder-table` now MATCHES `ubergoal/SKILL.md`. Gaia spine target still reports divergent from the direct checkout view; I did not use `git show main:...` because the task also said no git commands.

Deletion receipt inline:

| Removed block | New home | verified |
|---|---|---|
| Coding Agent Work Contract, 76 words | `ubergoal/SKILL.md#routing-table` | yes |
| Task Understanding Review, 245 words | `uberplan/SKILL.md#micro-intent--spec-first-fast-path-with-task-understanding-review` | yes |
| Lifecycle, 356 words | `ubergoal` routing / fast path / scope gate / completion rule | yes |
| Implementation effort table, 93 words | `ubergoal/SKILL.md#review-ladder` | yes |
| Goal ownership detail, 110 words | `ubergoal` routing + `goal-objective.md` + validator | yes |
| Thread/session topology, 192 words | `references/operational-states.md#runtime-topology-presets` | yes |
| Parent/child execution, 174 words | `references/operational-states.md` terminal/blocker/parent sections | yes |
| Architecture stepback prose, 57 words | `ubergoal/SKILL.md#routing-table` + `uberarchitect` | yes |
| Inlined Claude adversary block, 426 words | `references/claude-adversary.md` + ubergoal’s 3 questions | yes |

Flagged gap: the spine main-branch read could not be performed exactly as requested because that specific instruction required `git show`, and the dispatch also said no git commands. I used the direct file plus the drift fingerprint result instead.

