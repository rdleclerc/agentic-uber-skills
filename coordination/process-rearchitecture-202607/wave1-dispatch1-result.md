Implemented R1/R2 inside `agentic-uber-skills`. No git commands were run.

**Changed Files**
- `scripts/lint_pack_contract.py`: flipped model pin enforcement to frontmatter prohibition, added hardcoded model-id detection, and added the portability oracle inside the pack-contract aggregator.
- `AGENTS.md`, `README.md`: replaced pin policy with portable `lane_used` policy; updated install policy to checkout-relative symlinks. Added amendment J aggregator rule.
- `ROADMAP.md`, `uberskillevolver/SKILL.md`, `uberskillevolver/references/cross-machine-learning.md`, `uberskillevolver/scripts/new_learning_record.py`: moved learning paths to repo `learning/` and coordination references.
- All 10 `*/SKILL.md` files: removed `model:` and `effort:` frontmatter.
- `ubergoal/SKILL.md`: parameterized work-contract paths via `${UBER_GUIDE_ROOT:-~/repos/agentic-architecture-guide}`.
- `ubershow/SKILL.md`: replaced old OpenClaw runtime output paths with `coordination/<task-slug>/ubershow/`.
- `uberplan/SKILL.md`, `uberaccept/SKILL.md`: deleted the Type0-specific product-spine paragraphs:
  - `For Type0, the default spine is: real feed/tip/wire input -> normalized signal -> admission decision -> lane/story assignment -> story processing -> fact-check/publish/reject guard -> traceable result.`
  - `For Type0, default spine: real feed/tip/wire input -> normalized signal -> admission decision -> lane/story assignment -> story processing -> fact-check/publish/reject guard -> traceable result.`
  The generic Basic Spine First and operational-outcome language remains in place.
- `ubergoal/templates/uber-run-receipt.md`, `ubergoal/scripts/validate_uber_run_receipt.py`, `ubergoal/tests/test_validators.py`, `ubergoal/tests/fixtures/...`: added required non-empty `lane_used`.
- `tests/test_pack_contract.py`, `tests/fixtures/pack_contract/*`: added negative fixtures for pinned frontmatter, nonexistent absolute path, and machine-specific path.
- Fixture path cleanup: neutralized old `/Users/claw1/...` paths to `/Users/example/...` in relevant `ubergoal`, `uberplan`, and `uberassess` fixtures; updated ubersimplify learning fixture paths.
- `uber-skill-creator/scripts/quick_validate.py`: added a stdlib YAML-subset fallback so quick validation runs in restricted environments without PyYAML/network.

**SKILL.md Word Deltas**
- `uber-skill-creator`: 1219 -> 1215 (-4)
- `uberaccept`: 2657 -> 2628 (-29)
- `uberarchitect`: 822 -> 818 (-4)
- `uberassess`: 2104 -> 2100 (-4)
- `ubergoal`: 2755 -> 2763 (+8)
- `uberplan`: 3737 -> 3706 (-31)
- `uberrca`: 1672 -> 1668 (-4)
- `ubershow`: 1273 -> 1263 (-10)
- `ubersimplify`: 900 -> 896 (-4)
- `uberskillevolver`: 2037 -> 2058 (+21)
- Total: 19176 -> 19115 (-61)

**Tests**
- `python3 scripts/lint_pack_contract.py`: PASS
- `python3 -m unittest discover -s tests -v`: 28 tests OK
- `python3 -m pytest tests/ -q`: 28 passed
- Per-skill package lints: PASS for all skills with lint scripts (`uberarchitect` has no local lint script)
- Per-skill unit tests: 129 tests OK across touched skills
- `python3 uber-skill-creator/scripts/quick_validate.py <skill>`: all 10 skills valid

