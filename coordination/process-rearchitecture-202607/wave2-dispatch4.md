# Wave 2 — Dispatch 4: R8 retire-or-prove evaluations + uberskillevolver fossils (pack side)

You are Codex, implementer. Pack repo only; NO git commands. Two jobs:

## 1. Retirement evaluations (EVIDENCE + RECOMMENDATION ONLY — the operator decides at wave acceptance; do NOT uninstall, archive, or edit the evaluated skills)

Pass/fail contract per plan-v3 R8: a skill stays installed only with (a) a named owner, (b) a real triggering task class observed in coordination history, (c) an eval that would exercise it within a month. Evaluate ubersimplify, ubershow, uberarchitect:

- Evidence sweep: grep/search `/Users/rob/repos/agfunder-gaia/coordination/` (read-only) and this repo's coordination/ + reviews/ + learning/ for real artifacts produced BY each skill (ubersimplify audit trails/reports; ubershow HTML boards + receipts; uberarchitect stepback packets — two are known: codex-native-tool-recovery-2026-06-30 and gaia-gmail-nonresponse-uberrca-2026-07-02). Also check ROADMAP.md's dogfooding/retirement-trigger entries for each.
- Write `coordination/process-rearchitecture-202607/wave2-r8-retirement-evaluations.md`: per skill — evidence found (paths), contract test (a/b/c) verdict each, RECOMMENDATION (keep / keep-slimmed / archive) + one-paragraph rationale + what archiving would mean concretely (uninstall from both roots, tombstone in README, restore = symlink; skill dir stays in git). Where the recommendation is keep-slimmed, name the specific sections to cut.

## 2. uberskillevolver fossil sections → catalog + reference

The remaining incident-history sections in uberskillevolver/SKILL.md ("Regression lessons from scope-fidelity failures", "Regression lessons from completion-claim failures", "Red/green and false-green lessons", and any similar fossil prose remaining post-D3): convert each lesson into either (a) an UPDATE to an existing failure-eval case (scope-fidelity lessons → case scope-laundering-20260528; completion-claim/false-green lessons → likely case unverified-baseline-claims or a NEW process case `false-green-completion-claims` if the class is genuinely distinct — create it with schema v2 if so), or (b) a compact Trigger/Do/Fallback/Invalid row in a new short `uberskillevolver/references/regression-lessons.md` for anything that is guidance rather than incident record. Then delete the fossil sections from SKILL.md, leaving one pointer line. Update evals/failures/INDEX.md for any case changes; run the case validator.

Receipt: extend the d4 deletion receipt (same table format). Word deltas for uberskillevolver (budget: adjust in lint to new count +10%, round to 50). Run: pack tests + lint + evolver tests/lint + validate_failure_case (cases + --index). Print everything; FLAG contradictions.
