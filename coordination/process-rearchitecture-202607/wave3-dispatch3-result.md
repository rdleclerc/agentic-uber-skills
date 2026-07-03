Implemented the pack-side Wave 3 dispatch fixes without touching `ubergoal` and without running standalone git commands.

Changed:
- [validate_failure_case.py](/Users/rob/repos/agentic-uber-skills/scripts/validate_failure_case.py): Gaia INDEX dialect support, repo-prefixed canonical dirs, and new `--cross-index`.
- [validate_acceptance_report.py](/Users/rob/repos/agentic-uber-skills/uberaccept/scripts/validate_acceptance_report.py): `reproduced_red` / `no_repro_reason` and `interface_shape_receipt` gates with conservative heuristics.
- [validate_dispatch_ledger.py](/Users/rob/repos/agentic-uber-skills/scripts/validate_dispatch_ledger.py): new ledger row + duplicate non-retry validator.
- [run_routing_eval.py](/Users/rob/repos/agentic-uber-skills/evals/routing/run_routing_eval.py): packet marker leak removed; tier grading now token/qualifier based.
- [lint_pack_contract.py](/Users/rob/repos/agentic-uber-skills/scripts/lint_pack_contract.py): `origin/main` freshness note now uses stale `.git/FETCH_HEAD`.
- Failure catalog/INDEX statuses, new `two-layer-index-status-drift` case, G3/G2 notes, dispatch/reference wording, and uberskillevolver owner/cadence sentence.

Verification:
- `python3 scripts/lint_pack_contract.py --strict` PASS.
- `GAIA_ROOT=/private/tmp/absent-gaia-for-cross-index python3 -m unittest discover -s tests -v` PASS, 67 run, 3 skipped.
- Real Gaia present: `python3 -m unittest discover -s tests -v` FAILS only the new live cross-index guard.
- `validate_failure_case.py` cases PASS; pack `--index` PASS; Gaia dialect fixture PASS; real Gaia `--index` PASS.
- Routing pass fixture: 12/12 PASS. Under-tier fixture: R11/R12 FAIL as intended.
- `uberaccept` tests PASS; `uberskillevolver` tests PASS; touched skill package lints PASS.
- `quick_validate.py uberaccept` and `quick_validate.py uberskillevolver` PASS via local Python. `uv run --with pyyaml ...` was blocked by network/cache, then local Python worked.
- Word budgets: `ubergoal` 786/800 unchanged; `uberaccept` 1948/2150; `uberskillevolver` 1445/1550.

Flagged contradictions:
- The real Gaia INDEX still has these shared ids at `seed`, so the requested live cross-index test correctly fails until Gaia is synced: `dispatch-double-launch`, `evaluator-saturation`, `sandbox-fake-row-shape`, `subprocess-dies-without-terminal-state`.
- G6 and G8 target Gaia files, not pack files. I did not edit them under the “pack repo only” constraint.

Gaia patch block needed for G8:
```diff
*** Begin Patch
*** Update File: scripts/check_lane_liveness.py
@@
     Lane("slack-live-sync", "memory/slack-sync-state.json", 1, "every 30 minutes", ("last_run_at",)),
+    Lane("openclaw-gateway", "memory/gateway-canary-state.json", 2, "gateway canary", ("finished_at", "last_success_at", "checked_at", "ran_at")),
     Lane("brain-health-snapshot", "memory/health-snapshots", 48, "daily 08:55 PT"),
*** End Patch
```

Gaia INDEX status sync needed for the live cross-index guard:
```diff
*** Begin Patch
*** Update File: evals/failures/INDEX.md
@@
-- evaluator-saturation · process(process) · seed · canonical: agentic-uber-skills/evals/failures/
+- evaluator-saturation · process(process) · eval_built · canonical: agentic-uber-skills/evals/failures/
@@
-- sandbox-fake-row-shape · process(process) · seed · canonical: agentic-uber-skills/evals/failures/
-- dispatch-double-launch · process(process) · seed · canonical: agentic-uber-skills/evals/failures/
+- sandbox-fake-row-shape · process(process) · eval_built · canonical: agentic-uber-skills/evals/failures/
+- dispatch-double-launch · process(process) · eval_built · canonical: agentic-uber-skills/evals/failures/
@@
-- subprocess-dies-without-terminal-state · process(process) · seed · canonical: agentic-uber-skills/evals/failures/
+- subprocess-dies-without-terminal-state · process(process) · eval_built · canonical: agentic-uber-skills/evals/failures/
*** End Patch
```

