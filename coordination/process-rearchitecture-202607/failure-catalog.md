# Real-World Failure Catalog v2 — seed cases for the failure→eval database (R16)

v2 after round-1 review: 14 → 20 cases (5 added per judgment #13; case 20 added by orchestrator as P4 dogfood on the round's own baseline errors). Verdicts below are the JUDGE-FINAL merged grades for plan v2, with the v3 repair that lifts each case below PREVENTED (now baked into plan-v3). Round 2 verifies the mapping, it does not re-litigate round-1 grades.

## Schema v2 (formalized in Wave 1 as YAML frontmatter + md body, `validate_failure_case.py`)

```
id, date_observed, layer (process|runtime|both), canonical_layer (process|runtime — the ONE
authoritative copy for layer="both" cases; the other layer holds a pointer, and shared ids
carry a drift fingerprint), title, what_happened (sanitized per rules below), failure_class,
cost, gate_that_missed_it, eval_check, eval_type (executable|fixture|checklist|live),
plan_items, status (seed → eval_built → enforced)
```

Sanitization rules (pack layer is pushed to GitHub): no named individuals, no credentials/secret values, no message contents; runtime-layer copies in agfunder-gaia may carry incident detail. The secret-pattern scan (case 15's eval) runs over this folder too.

## Cases

| # | id | layer (canonical) | failure class | judge-final verdict for plan v2 | v3 repair → target |
|---|---|---|---|---|---|
| 1 | gmail-silent-lane-12d | runtime | unattended lane w/o proof-of-life | PREVENTED (class = silent multi-day death, not the human-owned credential expiry) | — |
| 2 | hermes-overseer-dead-9w | both (runtime) | watcher w/o watcher; docs claim live w/o evidence | PREVENTED | R14 inventory asserts docs' "live" claims against liveness artifacts |
| 3 | silent-nonresponse-class | runtime | point-patch instead of class-fix | SHORTENED (inherent: first patch of a novel class ships) | uberrca validator requires `class_invariant` + `surface_enumeration` |
| 4 | false-apology-fix-of-fix | runtime | fix not proven red on real failure path | SHORTENED → PREVENTED | reproduced-red receipt defined + acceptance-validator-checked (R11) |
| 5 | scope-laundering-20260528 | process | scope narrowing + self-certification; NEW vector = self-down-tiering | WEAK → PREVENTED | tier-assignment audit: receipt records tier+justification, reviewer's first check, Tier-1 scope echo, under-tier fixtures (R7/R13) |
| 6 | evaluator-saturation | process | gate that cannot say no | PREVENTED | — |
| 7 | claw1-path-rot | process | machine-specific paths in portable text | PREVENTED (instance); class needs portability oracle | path-lint flags machine-specific absolute paths even if they exist here; fixture scope defined (R2) |
| 8 | install-drift-uberarchitect | process | no install-sync contract | PREVENTED | + extra-skill ignore list (verified: 4 non-pack extras in ~/.codex/skills) |
| 9 | doctrine-drift-trio | process | duplicated rules drift | PREVENTED contingent on machinery ownership | fingerprint registry owned + reword rule + seeded-divergence self-test (R3, V9) |
| 10 | sandbox-fake-row-shape | process | fakes encode author beliefs, not real interfaces | SHORTENED → PREVENTED | interface-shape receipt required by acceptance validator when fakes stand in for external interfaces/DB (R12) |
| 11 | dispatch-double-launch | process | dispatch w/o idempotency/single-writer | SHORTENED → PREVENTED | dispatch ledger + claim-before-launch + duplicate-cull check, executable (R12) |
| 12 | human-owned-blocker-grind | both (runtime) | automation retrying human-owned blockers | PREVENTED | R14c text gains "durable/stateful alert state" |
| 13 | op-hang-under-launchd | runtime | blocking secret fetch in unattended context | SHORTENED → PREVENTED (secret-fetch subclass) | standing entrypoint-grep gaia check + GAIA_TESTING new-unattended-service trigger (child plan) |
| 14 | pg-null-upsert-dup | runtime | dialect edge case; non-idempotent writer | WEAK → PREVENTED | executable run-twice idempotency helper + GAIA_TESTING mandatory trigger for new `--apply` writers (child plan) |
| 15 | credential-exposure-by-agent | process | secrets echoed into transcripts/artifacts forcing rotation | NEW (round 1) | eval: secret-pattern scan over pack + coordination artifacts (ships Wave 1, R16a); standing doctrine: 1P-backed refs only, never echo values |
| 16 | post-upgrade-silent-breakage | runtime | dependency/vendor upgrade silently breaks a lane (origin of GAIA_TESTING's mandatory trigger, 2026-04-29 gmail break) | NEW (round 1) | case guards the trigger itself: any weakening of the post-`openclaw upgrade` canary+integration mandate fails the drift check |
| 17 | pinned-external-identifier-rot | process | hardcoded external ids (model ids) age into silent downgrades; pin was lint-ENFORCED | NEW (round 1) | R1 flips lint to pin-prohibition w/ negative fixtures; class eval: external identifiers in doctrine require an alias-or-policy, not a literal, unless marked intentional |
| 18 | library-silent-truncation | runtime | library choice silently loses input data (markdownify vs html2text, legacy-HTML essays) | NEW (round 1) | eval: ingest lanes assert output-vs-input size/content sanity thresholds; standing fix documented in runtime layer |
| 19 | dispatch-preflight-writeability | process | implementer runtime lacks git/temp writeability; commit promises fail late (kin of case 10: sandbox-blind claims) | NEW (round 1, Codex) | writeability preflight (git + temp probe) before any implementation dispatch or commit promise — ships Wave 1 |
| 20 | unverified-baseline-claims | process | plan justified structural decisions (R8 retirement) on un-spot-checked usage claims; one was false (uberarchitect WAS in use) | NEW (orchestrator dogfood, round 1's own failure) | eval: load-bearing evidence claims in plans must cite checkable artifact paths; reviewers/judge spot-check them (this round's protocol, now standing) |

## How the catalog is used (unchanged core, amended per P4)

1. **Reviewer test set**: round 2 verifies the verdicts/repairs above are implemented in plan-v3.
2. **Seed of the R16 database**: Wave 1 formalizes schema v2, splits cases by `canonical_layer` (pointers + shared-id drift fingerprint for `both` cases), builds the Wave-1 executable evals (cases 7, 8, 9, 14-helper, 15, 19).
3. **Automatic intake (P4 completeness rule)**: every terminal failure path has validator-enforced intake — uberrca exit, uberaccept surprise rows, uberdebug/R11 exit, gaia alert-RCA loop — requiring `failure_case_id | case_updated | not_applicable_with_reason`. Campaign-internal failures are appended under the same rule (case 20 is the first).
