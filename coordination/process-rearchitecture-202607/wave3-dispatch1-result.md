Implemented pack-only changes; no direct `git` commands were run.

**Changed**
- Added [references/dispatch-and-sessions.md](/Users/rob/repos/agentic-uber-skills/references/dispatch-and-sessions.md) as the R12 single home.
- Added [references/debug-loop.md](/Users/rob/repos/agentic-uber-skills/references/debug-loop.md) as the R11 everyday defect loop.
- Wired both into [ubergoal/SKILL.md](/Users/rob/repos/agentic-uber-skills/ubergoal/SKILL.md) and added the `uberrca` boundary line.
- Added `dispatch-mechanics-header` drift fingerprint.
- Updated cases 10/11/21/22 to cite the dispatch reference; cases 11 and 21 remain `seed` because they are checklist-backed until a validator exists.
- Bound catalog cases 3/4 to `references/debug-loop.md` in the campaign catalog.

**Word Counts**
- `references/dispatch-and-sessions.md`: 472 / 700
- `references/debug-loop.md`: 228 / 350
- `ubergoal/SKILL.md`: 799, delta `800 -> 799` (`-1`)
- `uberrca/SKILL.md`: 1374, delta `1346 -> 1374` (`+28`)

**Receipts**
- `python3 scripts/lint_pack_contract.py --strict`: PASS
- `python3 -m unittest discover -s tests -v`: PASS, 57 tests, 1 skip for local `.git` writeability
- `python3 scripts/validate_failure_case.py evals/failures/cases/`: PASS, 14 cases
- `python3 scripts/validate_failure_case.py --index ...`: PASS
- `python3 ubergoal/scripts/lint_skill_package.py "$PWD/ubergoal"`: PASS
- `python3 -B -m unittest discover -s ubergoal/tests -v`: PASS, 9 tests
- `python3 uberrca/scripts/lint_skill_package.py "$PWD/uberrca"`: PASS
- `python3 -B -m unittest discover -s uberrca/tests -v`: PASS, 5 tests
- `python3 uber-skill-creator/scripts/quick_validate.py ubergoal`: PASS
- `python3 uber-skill-creator/scripts/quick_validate.py uberrca`: PASS

**Flagged Contradictions**
- `uv run --with pyyaml ... quick_validate.py` failed because the sandbox cannot access `/Users/rob/.cache/uv`; direct `python3` quick-validate passed using the script’s built-in parser.
- Case 23 has no pack case file; it is indexed as Gaia-canonical: `unverified-context-assembly-assumption · both(runtime) · canonical: agfunder-gaia/evals/failures/`. I did not fabricate a local pack case file.

