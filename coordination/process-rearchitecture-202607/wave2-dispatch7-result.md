Implemented Dispatch 7 pack-side fixes.

Changed:
- Corrected R8 `ubershow` evaluation to `keep-slimmed` with the verified Gaia decision-board HTML + sibling receipt evidence.
- Added the third `unverified-baseline-claims` instance.
- Added strict default lint blocking for drift + install-sync failures.
- Added real-registry strict drift test, full `--strict` seeded-divergence test, and tier-table mirror test with failing fixture.
- Added `uberaccept` “100% confident” semantics.
- Added word budgets for `uberarchitect`, `ubershow`, and `uber-skill-creator`.
- Added the `ubergoal` fingerprinted-rule routing row without trimming; `ubergoal` is exactly at budget.
- Added W10 receipt notes, W11 answer-key note, and the runtime-canonical `unverified-context-assembly-assumption` index pointer.

Verification:
- `python3 scripts/lint_pack_contract.py` PASS
- `python3 scripts/lint_pack_contract.py --strict` PASS
- `python3 scripts/lint_pack_contract.py --drift --strict` PASS
- `python3 scripts/lint_pack_contract.py --install-sync --strict` PASS
- `python3 scripts/lint_pack_contract.py --secret-scan --strict` PASS
- `python3 -m unittest discover -s tests -v` PASS: 57 tests, 1 expected skip for local `.git` writeability
- `validate_failure_case.py evals/failures/cases` PASS
- `validate_failure_case.py --index ...` PASS
- Per-skill tests/lint/quick_validate passed for touched surfaces; `uberarchitect` has no local lint script, but its tests and quick_validate passed.

Word deltas:
- `ubergoal/SKILL.md`: 786 -> 800, budget 800
- `uberaccept/SKILL.md`: 1930 -> 1948, budget 2150
- `uberarchitect/SKILL.md`: 818 -> 818, budget 900
- `ubershow/SKILL.md`: 1263 -> 1263, budget 1400
- `uber-skill-creator/SKILL.md`: 1215 -> 1215, budget 1350

Flagged contradictions:
- Existing R8 archive policy still conflicts with `AGENTS.md` “all skills installed/exposed” policy, but this dispatch now keeps `ubershow`, so it is not blocking here.
- I ran no direct git commands, but the requested drift validators use their existing `git_ref(main)` reader internally.