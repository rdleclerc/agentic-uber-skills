Implemented Dispatch 5 pack-side fixes F3-F9 plus F12/F13 and case intake updates.

**Summary**
- Added `scripts/lint_pack_contract.py --dispatch-preflight [path]` with `.git` writability, `git status` probe, and TMPDIR write/delete probe.
- Added `validate_failure_case.py --index INDEX.md --cases cases/` and pack tests for id/status mismatches.
- Tightened path sanitization to per-match `${...:-...}` spans instead of whole-line exemptions.
- Tightened `blocked_with_failure_intake` acceptance reports to require `failure_case_id:` or `case_updated:`.
- Moved learning-record default root to `learning/private/local`.
- Rejected placeholder-only RCA surface enumeration.
- Added Gaia spine lane-policy drift entry, pending notes, AGENTS reword rule, case 22, and case-20 second-instance note.

**Verification**
- `python3 scripts/lint_pack_contract.py` passed.
- `python3 scripts/validate_failure_case.py evals/failures/cases` passed: 13 cases.
- `python3 scripts/validate_failure_case.py --index evals/failures/INDEX.md --cases evals/failures/cases` passed.
- `python3 -m unittest discover -s tests -v` passed: 47 tests, 1 skipped.
- Touched skill tests/lints passed:
  - `uberaccept`: lint + 34 tests.
  - `uberrca`: lint + 5 tests.
  - `uberskillevolver`: lint + 10 tests.
- Strict subreports passed: `--drift --strict`, `--install-sync --strict`, `--secret-scan --strict`.
- `quick_validate.py` passed for `uberaccept`, `uberrca`, `uberskillevolver`.

**Word Deltas**
- `AGENTS.md`: +12
- `uberaccept/SKILL.md`: +20
- `uberskillevolver/references/cross-machine-learning.md`: +6
- `evals/failures/INDEX.md`: -17
- `dispatch-preflight-writeability.md`: -2
- `unverified-baseline-claims.md`: +33
- `parallel-branch-reset-clobbers-merge.md`: +164 new
- `references/drift-fingerprints.toml`: +95
- New/updated fixtures aggregate: +496

**FLAG Contradictions**
- F3 asks for a real-machine preflight pass, but this runtime reports `.git` as not writable. The real-root test is present and skipped here; fixture pass/fail tests are green.
- `uv run --with pyyaml ... quick_validate.py` was blocked by `/Users/rob/.cache/uv` permissions. Direct `python3 quick_validate.py` succeeded for all touched skills.
- F9 required reading the Gaia spine sentence read-only outside this repo; no outside-repo edits were made.