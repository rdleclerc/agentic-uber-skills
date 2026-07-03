Implemented R13 in the pack repo only, with no standalone git commands.

Changed:
- Renamed evaluator to `uber-skill-creator/scripts/lint_skill_shape.py`.
- Left `evaluate_skill_quality.py` as a 3-line executable deprecation shim that exits nonzero.
- Removed score fields/output from shape lint.
- Added `evals/routing/run_routing_eval.py`, answer-key keyword grading, MUST-ESCALATE fixtures, and tests.
- Added bad mini-skill fixture and promoted `evaluator-saturation` to `eval_built`.
- Added `promote-now` `words_added/words_removed` validation for `uberskillevolver`.
- Added drift freshness NOTE for behind `git_ref` upstreams.
- Recorded W13 R9a smoke verification in the Wave-2 deletion receipt.

Verification:
- `python3 -m unittest discover -s tests -v`: PASS, 62 tests, 1 environment skip.
- `python3 scripts/lint_pack_contract.py --strict`: PASS.
- Routing pass fixture: PASS 12/12.
- Routing under-tier fixture: FAILS as intended on R11/R12 MUST-ESCALATE.
- `uber-skill-creator` lint/tests: PASS.
- `uberskillevolver` lint/tests: PASS.
- `quick_validate.py` direct local Python: PASS for both touched skills.
- `uv run --with pyyaml ...` could not run because sandbox/network blocked `pyyaml` fetch; direct `quick_validate.py` passed.
- Word budgets hold. Tightest is `ubergoal/SKILL.md` at 799/800; touched skills are `uber-skill-creator` 1240/1350 and `uberskillevolver` 1436/1550.

Contradictions flagged:
- Initial full test run found the failure-case index still listed `evaluator-saturation` as `seed`; fixed and reran green.
- Historical review artifacts still contain old “Skill Quality Report” score text; I left those as historical receipts, not active docs or runnable paths.

