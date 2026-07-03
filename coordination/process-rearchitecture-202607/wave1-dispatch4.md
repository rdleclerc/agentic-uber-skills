# Wave 1 — Dispatch 4 of 4: R16a gaia side (runtime-canonical failure cases)

You are Codex, implementer for the process-rearchitecture campaign. You are working in a CLEAN GIT WORKTREE of agfunder-gaia (branch `evals/failure-db-runtime-seed`) — work ONLY under `evals/failures/` and `scripts/`; NO git commands; touch nothing else.

Source of truth for case content: `${UBER_SKILLS_ROOT:-~/repos/agentic-uber-skills}/coordination/process-rearchitecture-202607/failure-catalog.md` (21 cases, judge-final verdicts) and the pack-side schema at `${UBER_SKILLS_ROOT}/evals/failures/README.md` (read both first; follow the schema exactly — validate with `python3 ${UBER_SKILLS_ROOT}/scripts/validate_failure_case.py evals/failures/cases/`).

## Deliverables

1. `evals/failures/README.md` — SHORT (≤25 lines): this is the RUNTIME layer of the two-layer failure-eval DB; schema + intake grammar live in the pack README (pointer via `${UBER_SKILLS_ROOT}`); runtime-layer cases may carry incident detail but NEVER credentials/secret values; new-case intake rule (uberrca exits + gaia alert-RCA loop; enforcement validators live in the pack).
2. `evals/failures/cases/<id>.md` for the 9 RUNTIME-canonical cases: gmail-silent-lane-12d, hermes-overseer-dead-9w, silent-nonresponse-class, false-apology-fix-of-fix, human-owned-blocker-grind, op-hang-under-launchd, pg-null-upsert-dup, post-upgrade-silent-breakage, library-silent-truncation. Populate from the catalog rows; date_observed: use the real incident dates where the catalog/body names them (gmail ≈2026-06-19 onset detected 2026-07-01; hermes 2026-05-04 onset detected 2026-07-02; silent-nonresponse flagged 2026-06-11; false-apology 2026-07-02; human-owned-blocker-grind 2026-06-24; op-hang and pg-null-upsert are standing lessons — use 2026-07-03 with a note; post-upgrade 2026-04-29; library-silent-truncation 2026-07-03 with a note). status: seed for all. layer/canonical_layer per catalog (cases hermes + human-owned-blocker are layer=both, canonical_layer=runtime). Where the repo has receipts (coordination folders, RCA dirs), cite 1-2 real artifact paths in the body as evidence anchors.
3. `evals/failures/INDEX.md` — all 21 cases one line each; the 12 process-canonical cases marked `canonical: agentic-uber-skills/evals/failures/`.
4. `scripts/run_twice_idempotency_check.sh` — SKELETON helper for case 14 (pg-null-upsert-dup): takes a command as arguments, runs it twice, compares a caller-supplied row-count probe (`--probe "psql ... -c 'select count(*) ...'"`) between runs, exits nonzero if the second run inserted rows. Keep it ~40 lines, defensive, clearly marked SKELETON with usage examples in the header; do NOT wire it into any live lane (that is the Wave-3 child plan).

## Wrap-up

Run the pack validator over your cases dir and print its output. Print: files created, case list with dates/status, any contradiction between catalog content and repo evidence you found (FLAG, do not silently resolve — e.g. if a coordination artifact contradicts a catalog date, keep the catalog value and flag it).
