# Wave 1 — Tier-2 Independent Adversarial Review

Reviewer: fresh Claude (Fable 5) adversarial lane, no prior involvement in implementation or orchestration. Read-only except this file.
Scope reviewed: pack repo `agentic-uber-skills` `a7f35f0..HEAD` (slices 1–3, commits 4d4f9a7 / 35fa142 / 4b38119) + gaia repo commit `e0f9c17c` (merge of `098093b5`, dispatch 4). Authority: `plan-v3.md` Wave 1 (R1/R2/R3-tool/R4/R16a) + round2 amendments A, B, C, D, G-partial, J, K, L.
Method: full read of new/changed validators, lint, registry, fixtures, case files (all 12 pack + all 9 gaia), independent rerun of every suite/lint, and empirical adversarial probes against the validators and oracle. Gaia reviewed from git objects only; its working tree (another session's WIP branch) was not touched.

## Verification of claimed green (independent rerun)

- `python3 -m pytest tests/ -q` → 39 passed. Per-skill: ubergoal 9, uberaccept 30, uberrca 5, uberplan 41, uberassess 9, ubersimplify 12, uberskillevolver 9, ubershow 6(+14 subtests), uberarchitect 3, uber-skill-creator 10 — all pass.
- `lint_pack_contract.py` default, `--drift --strict`, `--install-sync --strict`, `--secret-scan --strict` → all exit 0. `quick_validate.py` spot-checked green.
- `validate_failure_case.py` → 12 pack cases PASS; 9 gaia cases (extracted from commit `e0f9c17c`) PASS.
- Drift MATCH lines hand-verified non-vacuous (gaia CLAUDE.md posture sentence, GAIA_TESTING canary-mandate line 21, `Version: 1.5` in both guide copies, lane-policy sentences in AGENTS/README, canary command in `~/CLAUDE.md`). Seeded-divergence self-test is real (fixture registry: 1 MATCH via whitespace normalization + 1 DIVERGED; `--strict` fails).
- Old-lint parity: compared against `a7f35f0` lint — no enforcement dropped besides the pin itself; claw1 phrases replaced with portable equivalents plus a NEW Claude install-target phrase; all other required-phrase groups preserved.
- Targeted false-green probes that correctly FAIL: empty intake value; whitespace `lane_used`; rejected report without intake; missing cost `source`; invalid cost source; pinned frontmatter; machine path in doctrine; nonexistent absolute path; missing RCA invariant/surface/intake.
- Content spot-checks: all gaia case evidence anchors exist on gaia main lineage (`check_gmail_hook_terminality.py`, both coordination RCA folders, `hermes-overseer.md`, etc.); ubergoal work-contract guide paths exist in `~/repos/agentic-architecture-guide`; no `/Users/claw1/` remains in doctrine text (only historical `reviews/` + the case id/fixtures, which are out of oracle scope by design).

## Findings (ranked)

### BLOCKER

**F1. The Wave-1 gaia deliverable has been clobbered off gaia `main` and the clobbered state is pushed.**
Evidence: `agfunder-gaia` reflog — `main@{1} = e0f9c17c` ("Merge failure-eval DB runtime seed"), `main@{0}: branch: Reset to feat/e6-auto-post-updates` → `c7586aa0`, whose parent is `a4514260` (not the merge). `git merge-base --is-ancestor e0f9c17c main` → NOT ancestor; no ref contains `e0f9c17c`/`098093b5`; `main:evals/failures/INDEX.md` → MISSING; `origin/main == c7586aa0`. The parallel session's branch-reset workflow silently dropped the already-merged Wave-1 commit, and the loss is now on the remote.
Why it matters: campaign DoD requires "Failure-eval DB live in both layers"; the runtime layer is currently not on main at all. This is also a live instance of the campaign's own failure class (case 11 family: parallel writers on one ref without claim/ledger), made silent by F2 (nothing in gaia CI references the new tree). A wave receipt claiming "landed" would be untruthful today.
Minimal fix: coordinate with the owning session, then re-merge `e0f9c17c` (or cherry-pick `098093b5`) onto current gaia main and re-verify with an ancestor check at push time; file P4 intake for this campaign-internal failure (see intake suggestion below); land F2's wiring so a future reset cannot drop the tree silently.

### MAJOR

**F2. `validate_failure_case.py` is not invoked by the gaia test suite — spec says it must be.**
Evidence: plan R16a — "`validate_failure_case.py` (shared, invoked by both repos' test suites)"; the script's own docstring justifies its standalone-CLI status (amendment J) by "Gaia's test suite invokes it cross-repo via `${UBER_SKILLS_ROOT:-…}/scripts/validate_failure_case.py`". `git grep validate_failure_case main -- tests/ scripts/ GAIA_TESTING.md` in gaia → no hits; only the runtime README documents the command for humans.
Why it matters: the runtime layer is unvalidated in CI, the amendment-J justification recorded in the code is currently false, and F1 proved the practical consequence (tree vanished with zero test signal).
Minimal fix: add one gaia test (or GAIA_TESTING mandatory-trigger hook) that runs the validator over `evals/failures/cases/` and asserts the INDEX id-set matches the case files; note UBER_SKILLS_ROOT fallback and skip-with-loud-warning if the pack checkout is absent.

**F3. Case-19 writeability-preflight EXEC gate did not ship, despite plan-v3 marking it a Wave-1 deliverable.**
Evidence: plan v3 Wave-1 addendum — "dispatch-preflight writeability gate (case 19): … EXEC, part of R12's contract but shipped early since implementation starts at Wave 1"; catalog §"builds the Wave-1 executable evals (cases 7, 8, 9, 14-helper, 15, 19)". Landed: `evals/failures/cases/dispatch-preflight-writeability.md` is `status: seed`, eval_check "R12 dispatch preflight writeability fixture" (Wave 3), body: "remains seeded for the future dispatch wrapper". No dispatch doc or judgment records a re-scope.
Why it matters: 1 of 6 promised Wave-1 executable evals silently became a Wave-3 item; silent descoping is the exact class the campaign's tier/scope machinery exists to prevent.
Minimal fix: either ship the small probe (git-writeability + temp-dir probe script + one fixture) now, or record an explicit operator-visible re-scope with rationale in the wave receipt and update catalog line 45.

**F4. Cross-layer case index has zero enforcement and is already inconsistent; the required shared-id drift fingerprint is missing.**
Evidence: catalog schema — "shared ids carry a drift fingerprint"; R16a — "cross-index per layer + shared-id drift fingerprint". `references/drift-fingerprints.toml` has no such entry, and no validator reads either INDEX.md. Already diverged at birth: pack INDEX marks 4 ids `eval_built` (claw1-path-rot, install-drift-uberarchitect, doctrine-drift-trio, credential-exposure-by-agent) and still says "(pending dispatch 4)" on all 9 runtime rows; gaia INDEX lists all 21 ids as `seed`. Additionally `wave1-dispatch3-result.md` claims "eval_built=3, seed=18" and "kept case 15 status as seed", contradicting the landed tree (case 15 is `eval_built`) — a receipt/diff mismatch the exact-diff review did not reconcile.
Why it matters: the two-layer DB's central consistency mechanism (per spec) doesn't exist; the indexes drifted before the wave even shipped, and a dispatch receipt misstates the landed state.
Minimal fix: extend `validate_failure_case.py` (or a small aggregator module) to parse both INDEX files and assert id-set + status agreement with case-file frontmatter; refresh both INDEXes (drop "pending dispatch 4", sync statuses); correct the dispatch3-result discrepancy in the wave receipt.

### MODERATE

**F5. Portability oracle has a line-level exemption hole (proven).**
`scripts/lint_pack_contract.py:226` — `is_parameterized_path_line()` exempts the entire line when any `${VAR:-default}` token appears; probe: `"Use ${UBER_GUIDE_ROOT:-~/repos/…}/docs and also /Users/claw1/secret/machine/path"` → machine path not flagged. Same line-level pattern in `validate_failure_case.py:99-105` (`"${" or "~/" or "<name>" or "<user>"` anywhere on the line exempts a `/Users/<x>/` path in `what_happened`).
Minimal fix: exempt per-match (match must lie inside a `${…:-…}` default), not per-line.

**F6. Terminal-status mode gaps vs amendment A (two proven, two coverage).**
(a) `acceptance_status: blocked_with_failure_intake` validates with `not_applicable_with_reason` as the sole intake field (probe passed) — the status promises intake, the validator accepts "nothing to file". (b) `failure_case_id: made-up-case-that-does-not-exist` passes — intake ids are never checked against `evals/failures/cases/` in any of the three validators. (c) No fixture/test exists for `blocked_with_failure_intake` at all, and no test for an invalid status string ("fixtures both ways" is only fully met for `rejected`). (d) `acceptance_status` semantics appear nowhere in uberaccept/SKILL.md — only the template line.
Minimal fix: require `failure_case_id | case_updated` when status is `blocked_with_failure_intake`; add a blocked pass/fail fixture pair + invalid-status test; add an optional `--cases-dir` existence check (warn-level is fine for cross-repo); one SKILL.md sentence.
Note: the leniency of terminal mode itself (a rejected report needs only status + intake + a named blocker/finding) is per amendment A's intent and is not counted as a defect.

**F7. Learning-record privacy default regressed from ignored to tracked.**
`uberskillevolver/scripts/new_learning_record.py` default `--root` changed `.uberlearn` (gitignored) → `learning/inbox/local` (tracked); `cross-machine-learning.md` step 1 now creates the RAW record under `learning/inbox/$(hostname -s)` while `.gitignore` covers only `learning/private/`. The same slice's SKILL.md says "keep private/raw detail out of Git" — the tooling default now contradicts it, and step 3's cp-into-inbox flow no longer makes sense (raw and sanitized both live in the inbox, in two different sub-layouts).
Minimal fix: default `--root learning/private/local`; docs: create raw under `learning/private/`, copy sanitized packet into `learning/inbox/`.

**F8. RCA validator accepts vacuous surface enumeration (proven).**
`uberrca/scripts/validate_rca_artifact.py:71-73` — any `- ` bullet satisfies `surface_enumeration`; probe with `- tbd` passed.
Minimal fix: reject bullets whose text normalizes into the existing PLACEHOLDERS set.

**F9. Spine lane-policy fingerprint missing from the initial registry.**
Plan R3 initial registry names "lane-policy sentences (spine + pack versions)". Landed registry fingerprints only the pack sentence (AGENTS.md/README.md). The canonical copy — the gaia spine's lane policy in `knowledge/coding-agent-operating-spine.md`, which per Governance OWNS lane policy — can drift with no signal. The omission originates in the dispatch-2 instruction, not the implementer.
Minimal fix: add a `report_only` entry targeting `${GAIA_ROOT:-~/repos/agfunder-gaia}/knowledge/coding-agent-operating-spine.md`, blocking_wave=2, matching the other gaia-side entries.

### MINOR

**F10. Secret-scan false-negative classes (all proven undetected) + one future false-positive.** Misses: `github_pat_` fine-grained PATs, JWTs (base64url `-`/`_` defeats `base64_32`), `xoxc`/`xoxs`/`xapp` Slack tokens, AWS secret keys with no `+`/`=` on the line. Future noise: `hex_32` will flag full 40-char git SHAs quoted in coordination docs, and `test_secret_scan_…` asserts the real repo passes `--strict`, so the suite goes red the first time a coordination doc quotes a full SHA. Report-only this wave, so no gate impact; fix patterns (add `github_pat_`, base64url class, more Slack prefixes; exempt 40-hex when preceded by "commit"/in backticks) before blocking_wave=2.

**F11. `validate_failure_case.py` robustness/coverage nits.** Nonexistent target → raw traceback instead of clean FAIL (observed), i.e. a non-truthful terminal state from the tool that enforces truthful terminal states; sanitization scans only `what_happened` (a `/Users/rob/...` in `title`, `notes`, `cost`, or the body passes); `none` is not in its placeholder set. Small fixes, one function each.

**F12. Born-diverged registry targets carry no `pending` note.** 5 of 16 target checks are DIVERGED at seed time (test-channel-posture ×3, canary-command ×2) — known Wave-2 propagation TODOs per dispatch 2, but the report renders them identically to genuine drift (V9 "checks bypassed as noise" risk). The `pending` field exists and prints; set it on those entries.

**F13. R3's reword rule lives only as a TOML comment.** Plan: "rule in AGENTS.md: 'reword a fingerprinted rule ⇒ update registry in the same commit.'" AGENTS.md has no such line (grep confirms); only the registry header carries it. One AGENTS.md line (and optionally a required-phrase entry) closes it.

**F14. Process-case `date_observed` values look synthesized.** Cases mapped to catalog rows 6–11 carry exact consecutive dates 2026-06-19…24; the catalog has no per-case dates backing them. Runtime cases handled this honestly (explicit "Date note" disclosures); process cases assert precision that doesn't exist. Cosmetic now, misleading once the DB feeds telemetry — prefer an "audit-window date" note like the gaia files.

**F15. DoD "report-only for one wave before blocking" not applied to the portability oracle (or pin prohibition).** Both are immediately blocking in the default lint. Deviation is in the safe direction (repo is green; R2's own test text says "fail"), but it contradicts the campaign DoD sentence and is recorded nowhere. Note it in the wave receipt. Related: `blocking` drift entries and install-sync violations only actually gate under focused `--strict` runs, which no test executes against the real registry — the AGENTS/README required-phrase checks are the real guard for the lane-policy sentence today (acceptable; be aware the registry's `blocking_wave=1` is currently advisory).

**F16. Coordination/receipt hygiene before push.** `wave1-dispatch4.md` + `wave1-dispatch4-result.md` are untracked (operator decision #4: campaign folder commits with waves); no wave receipt / cutover-ledger entry exists yet; dispatch4-result states "High-tier Claude review was not reachable … locally verified only" — the orchestrator's exact-diff review of dispatch 4 must be explicitly recorded in the wave receipt so the no-self-approval invariant is auditably satisfied. Also note `tests/test_pack_contract.py` defines `UberassessContractTests` after the `unittest.main()` guard (runs under pytest/discover, silently skipped under direct `python tests/test_pack_contract.py`) — pre-existing pattern, worth a cleanup ticket only.

## Positive findings (what genuinely holds)

- The specific false-green hypotheses in the review charter all fail correctly: empty intake value, whitespace `lane_used`, `rejected` with no blocker text, receipt missing cost/source, pinned frontmatter, machine-specific doctrine path. Negative fixtures are real and exercised by named tests (grep-verified, rerun-verified).
- Pin migration lost nothing: every non-pin enforcement from the old lint survives; the new AGENTS/README phrase checks + registry entry double-cover the lane-policy sentence. The "omit acceptance_status → legacy accepted" backdoor does NOT weaken anything: omitted status routes to the FULL strict battery, so failure reports can't dodge terminal-mode rules by omission — the failure mode of the old contract (truthful failure reports could not validate) is genuinely fixed.
- Drift machinery is real, not vacuous: MATCH lines hand-verified against target files; seeded-divergence self-test asserts both MATCH and DIVERGED plus strict failure; registry schema validation has its own invalid fixture.
- Install-sync verified against the real machine (both roots symlinked to this checkout) and against a seeded desync fixture covering missing/copy/wrong-target/allowed-extra/unknown-extra.
- Gaia case content is well-grounded: all evidence anchors exist on the merged lineage; date conflicts are disclosed in-file rather than papered over; the run-twice skeleton is correct for its stated purpose and safely unwired.
- Amendments B, C (mostly), D (Wave-1 fields), J, K, L are genuinely implemented; flagged contradictions (lane-policy literal-vs-two-forms, 20-vs-21 cases, case dates) were surfaced by the implementer rather than silently resolved.

## Tier check and scope echo

- **Tier: Tier 2 is correct as landed.** Cross-repo doctrine/pointer edits ⇒ Tier 2 minimum per the plan's ladder; nothing in Wave 1 injects into live OpenClaw session context (`evals/` is additive; `run_twice_idempotency_check.sh` is explicitly unwired; no launchd/Hermes/service edits), so no GAIA_TESTING live-proof gate or Tier 3 is triggered. This review constitutes the required independent adversarial lane; the orchestrator's exact-diff pass plus this lane satisfies the Tier-2 shape, provided F16's recording gap is closed in the wave receipt.
- **Scope echo:** operator approved implementation of R1–R16 after two review rounds (scope.md approvals #1–#4), with the two-layer DB home in `agfunder-gaia` explicitly approved (#2). Wave 1 as landed stays inside that scope: R1/R2/R3-tool/R4/R16a only, no Wave-2 dedup/retire work smuggled in, no runtime behavior changes. One visibility note: approval #4 names commit+push for `agentic-uber-skills` and `agentic-architecture-guide`; gaia-side commits ride on approval #2 and the cutover ledger — defensible, but the wave receipt should say so explicitly. The guide repo received no Wave-1 changes (none were required).

## Failure-catalog intake suggestion

**New case (runtime-canonical or `both`): `parallel-branch-reset-clobbers-merge`** — a parallel session's branch-reset workflow (`git branch -f main <feature>` pattern, visible in gaia reflog) silently dropped an already-merged wave commit from `main`, and the push made the loss durable; zero test signal because the new tree had no CI reference (F2). Distinct from case 11 (duplicate dispatch/no-claim on work) — this is a ref-level lost-update between an orchestrated wave merge and an unrelated session's ref rewrite. Eval: (a) gaia suite invokes `validate_failure_case.py` over `evals/failures/` (F2 wiring — makes the loss loud), (b) wave-push protocol gains a "landed-commit ancestor check": before declaring a wave pushed, assert each landed SHA `--is-ancestor` of the target branch tip. Secondary candidate (cheaper: `case_updated`): `unverified-baseline-claims` gains the dispatch3-result receipt/diff mismatch (claimed eval_built=3 vs landed 4) as a second instance of unspot-checked load-bearing claims.

## Verdict

Pack-side slices 1–3 are accept-quality: claimed green independently reproduced, validators genuinely able to fail, no weakened checks found, spec deviations mostly disclosed. But the wave as a unit cannot truthfully be declared landed: its gaia half is currently absent from gaia `main` (F1), the wiring whose absence made that silent is itself a Wave-1 spec item (F2), one promised Wave-1 executable eval was silently deferred (F3), and the DB's cross-layer consistency mechanism is missing and already inconsistent (F4). Per the campaign's own truthful-terminal-state doctrine these are blockers, not fix-alongs.

Required to convert to accept: (1) re-land `e0f9c17c`/`098093b5` on gaia main with an ancestor check at push, plus P4 intake for the clobber; (2) wire `validate_failure_case.py` + INDEX-consistency assertion into the gaia suite; (3) ship or explicitly re-scope the case-19 preflight; (4) sync both INDEXes and reconcile the dispatch3-result status claim in the wave receipt. F5–F9 are strongly recommended for the same wave (small diffs); F10–F16 may ride Wave 2 with receipt notes.

WAVE VERDICT: REJECT (blockers: F1 gaia deliverable clobbered off main; F2 gaia-suite validator wiring missing per R16a; F3 case-19 Wave-1 EXEC gate silently deferred; F4 cross-layer index enforcement missing and already diverged)
