## Role statement

I accept the round-2 implementer role: I am judging whether v3 is buildable, testable, and safe to start without hidden assumptions. Reject conditions: (1) a round-1 change is counted resolved without a bound mechanism, fixture, or owner; (2) Wave 1 depends on validator behavior the current suite cannot support; (3) the catalog claims enforcement for cases not mapped to a concrete plan item/check.

Artifacts reviewed: `scope.md`, `plan-v3.md`, `round1-judgment.md`, `failure-catalog.md`, plus `plan-v2.md`, both round-1 reviews, and current validators/templates/tests.

## Resolution audit

| # | Audit | v3 evidence |
|---:|---|---|
| 1 | RESOLVED | R9a/R9b split; R9b requires context-assembly citation, Slack before/after probe, rollback. |
| 2 | RESOLVED | Governance: spine owns gaia lane policy; pack carries portable default + gaia pointer. |
| 3 | RESOLVED-BUT-BREAKS-TERMINAL-VALIDATION | P4 requires intake at four chokepoints via receipt/acceptance/RCA validators, but current acceptance validator only accepts successful reports. |
| 4 | RESOLVED | Governance: receipts record `tier` + justification; reviewer first check; under-tier fixtures. |
| 5 | RESOLVED | Corrected baseline, uberarchitect use, thread-cap/claw1 counts, conditional word target. |
| 6 | RESOLVED | Wave-2 entry block: R7/R6 before dedup/retire/unify. |
| 7 | RESOLVED | Cross-repo cutover ledger: canonical home, pointers, install sync; no dangling pointers. |
| 8 | RESOLVED | Measurement spine: baseline 3-5 tasks, receipt fields, weekly comparison. |
| 9 | RESOLVED | Item matrix names EXEC/FIX/CHK/LIVE checks and fixtures/commands. |
| 10 | RESOLVED | R3/R4 are aggregator modules; R16a reuses receipt/acceptance validators plus new RCA validator. |
| 11 | PARTIAL | Owners/adoption named for registry and learning; owner/schema still thin for failure DB, path-lint, install-sync. |
| 12 | RESOLVED | R14/R15 Gaia child plan includes access assumptions, rollback, fallback, LIVE/EXEC gates. |
| 13 | RESOLVED | Catalog now 20; `canonical_layer`; secret scan; full security lane explicitly out of scope. |
| 14 | RESOLVED | R10 is refactor of existing micro-intent; standing word budgets in lint. |
| 15 | RESOLVED | R11 form evidence-contingent; reproduced-red receipt and intake either way. |
| 16 | PARTIAL | Effort ranges adopted and many inputs named, but exact drift target manifest and shared-index format remain underspecified. |
| 17 | RESOLVED | V3 session-level evidence recorded; subprocess probe remains Wave-2 gate. |
| 18 | RESOLVED | Learning owner/cadence: operator-facing, per-wave now, monthly later. |
| 19 | PARTIAL | Catalog updated to 20, but schema fields `plan_items`, `eval_type`, `status` are not represented per case. |

## New challenges

1. **Claim:** P4 can use the existing acceptance validator path for terminal failures. **Causal layer:** validator contract. **Why:** `validate_acceptance_report.py` requires `100% confident within scope? yes`, clear blockers, and a complete/ready/accept recommendation, so a rejecting acceptance report with `failure_case_id` cannot validate. **Evidence:** current acceptance validator final checks; v3 P4 says every terminal failure path is validator-enforced. **Minimum impact:** add an explicit terminal-status mode or separate failure-acceptance validator, with pass/fail fixtures for accepted and rejected reports.

2. **Claim:** The fingerprint registry is now implementer-ready. **Causal layer:** source authority. **Why:** v3 lists initial strings but not target paths, normalization, allowed absence rules, or literal-vs-regex/hash semantics. I could build a drift checker only by inventing policy. **Evidence:** R3 names strings and `references/drift-fingerprints.toml`; current `lint_pack_contract.py` is hardcoded phrase checks. **Minimum impact:** define TOML fields: `id`, `owner`, `adoption_state`, `canonical_source`, `target_paths`, `match`, `normalization`, `allowed_absences`, `severity`, `blocking_wave`.

3. **Claim:** Catalog v2 mappings are complete. **Causal layer:** eval coverage. **Why:** cases 16-18 have prevention targets not bound to v3 mechanisms: post-upgrade canary weakening is not in the initial fingerprint list; external-id rot is broader than frontmatter model pins; library truncation has no named Gaia child-plan check. **Evidence:** catalog schema includes `plan_items/eval_type/status`, but the case table omits them; R16a executable list omits 16-18. **Minimum impact:** add per-case mapping/status/eval fields, or mark these checklist/runtime-follow-on with owners and enforcement waves.

4. **Claim:** New validator fields compose by template addition. **Causal layer:** false-green validation. **Why:** current templates contain fields validators do not enforce: tier rationale, red/green ledger, requirement ledger, and generic “shape” language. **Evidence:** plan validator only requires `tier decision` section; acceptance `REQUIRED_SECTIONS` omits red/green ledger; receipt validator requires `Tier` but not justification, cost fields, or failure intake. **Minimum impact:** add validator functions and negative fixtures for tier justification, reproduced-red, interface-shape receipt, cost fields, and intake fields.

## Catalog v2 check

Schema v2 is directionally sound: `canonical_layer` fixes the “both” duplication problem if single-layer cases set `canonical_layer == layer` and noncanonical copies are pointer-only. The shared-id fingerprint is coherent, but the algorithm and cross-index file shape must be specified before implementation.

Case 20 is legitimate dogfood: v3’s baseline correction proves the class is real. It should be `eval_type: checklist`, `status: seed`, unless a load-bearing-claim citation validator is added.

Wave 1 is achievable only at the top of 2-4 sessions. Two sessions is not credible for R1/R2/R3/R4/R16a plus measurement/writeability, two-layer schema, validator changes, and fixtures. Four sessions is plausible if Gaia work stays to scaffold/helper level and live service repair is not pulled forward.

Implementer inputs now sufficient: routing answer key, install symlink policy, cutover ledger. Still not buildable exactly from v3 alone: drift target manifest, shared-index/fingerprint format, and concrete Gaia service labels/paths for the child plan.

VERDICT: MINOR_CHANGES_ONLY — implementation may start once Wave 1 explicitly adds the terminal-failure validator mode, registry manifest schema, and per-case catalog mappings/status fields.