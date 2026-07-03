Implemented R16a pack-side changes in this repo only, with no git commands.

**Changed Files**
- Failure DB: `evals/failures/README.md`, `evals/failures/INDEX.md`, 12 process-canonical case files under `evals/failures/cases/`
- Validators/lint: `scripts/validate_failure_case.py`, `scripts/lint_pack_contract.py`, `uberaccept/scripts/validate_acceptance_report.py`, `ubergoal/scripts/validate_uber_run_receipt.py`, `uberrca/scripts/validate_rca_artifact.py`
- Templates/SKILLs: `uberaccept/templates/final-acceptance.md`, `ubergoal/templates/uber-run-receipt.md`, `uberrca/templates/rca-artifact.md`, plus one-line pointers in `ubergoal/SKILL.md`, `uberaccept/SKILL.md`, `uberrca/SKILL.md`
- Tests/fixtures: new failure-case fixtures/tests, secret-scan fixture, acceptance terminal-mode fixtures, receipt cost/intake tests, RCA artifact fixtures/tests

**SKILL.md Word Deltas**
- `ubergoal/SKILL.md`: 2763 → 2767, `+4`
- `uberaccept/SKILL.md`: 2628 → 2641, `+13`
- `uberrca/SKILL.md`: 1668 → 1684, `+16`

**Validation**
- `python3 scripts/lint_pack_contract.py`: pass
- `python3 -m unittest discover -s tests -v`: 39 tests pass
- `ubergoal` lint + tests: pass, 9 tests
- `uberaccept` lint + tests: pass, 30 tests
- `uberrca` lint + tests: pass, 5 tests
- `scripts/validate_failure_case.py evals/failures/cases/`: pass, 12 cases
- `python3 uber-skill-creator/scripts/quick_validate.py` for `ubergoal`, `uberaccept`, `uberrca`: pass
- `uv run --with pyyaml ... quick_validate.py` was blocked by sandbox/network: default uv cache was not writable, then PyPI DNS fetch failed. The direct validator path passed via its built-in YAML fallback.

**Case Index Summary**
- 21 total cases indexed
- 12 process-canonical cases live here
- 9 runtime-canonical cases marked `canonical: agfunder-gaia/evals/failures/ (pending dispatch 4)`
- Statuses: `eval_built=3`, `seed=18`
- `eval_built`: cases 7, 8, 9 only, per dispatch instruction

**Contradictions Flagged**
- `plan-v3.md` / catalog prose still says “20 cases” in places, but the catalog includes case 21 and the dispatch requested all 21. I implemented the 21-case index.
- `scope-laundering-20260528` encodes `2026-05-28`, while the dispatch says cases 1-14 use observed dates in `2026-06-18..2026-07-02`. I used the requested Wave-1 range and left the ID unchanged.
- Case 15 now has an implemented `--secret-scan` eval path, but the dispatch said only cases 7/8/9 should be `eval_built`; I kept case 15 status as `seed` and pointed `eval_check` at the new module.