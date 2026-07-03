**Role Statement**

I accept the adversarial role, modified to the implementer lens: I am judging whether I could build, test, operate, and defend this plan without relying on ceremony or model summaries. The operator-original instructions require more than cleanup: latest upstreams, a two-week work/process review, better/faster coding, more powerful skills, adversarial review before implementation, and automatic failure-to-eval capture. The plan can narrow that into “dedupe doctrine + add validators” and miss the “solve problems faster” and “automatic” mandates.

Reject conditions:

1. A wave can pass through model-written receipts without deterministic tests, fixtures, or live proof for its risk.
2. A canonical-pointer migration can leave any live session reading a deleted rule before the canonical home and drift check are in place.
3. The failure-eval DB becomes another optional form agents can skip under pressure.

**Challenges**

1. **Claim:** R1-R16 DoDs are mechanically testable. **Causal layer:** feasibility. **Why it matters:** I could “pass” many DoDs while leaving the intent undelivered. **Falsifying/satisfying evidence:** executable validators with failing fixtures and expected outputs per item. **Minimum impact:** add an R-item test matrix before Wave 1. Item check: R1 partial, because current `lint_pack_contract.py` and tests require pins and must be migrated with negative tests; R2 weak, because “absolute path exists or parameterized” can pass on Rob while still non-portable; R3 weak until canonical channel/canary/lane strings are specified; R4 testable if temp skill roots and extra-skill ignores are included; R16a partial, because schema/index/sanitization/status rules are unspecified; R5 weak, because deletion receipts can be prose-only and fingerprints do not prove semantic preservation; R6 partial, because “correct tier” needs an answer key and grader; R7 weak unless contradiction pairs are fixture-backed; R8 weak, because “real usage plan” is not a pass/fail contract; R9 partial, line/hop counts are testable but fresh-session smoke needs a harness; R10 partial, exact artifact count is testable but escalation judgment needs fixtures; R11 weak, red-on-real-path proof is undefined for non-runtime cases; R12 weak without dispatch fixtures/idempotency tests; R13 hard, transcript-graded fresh-agent evals are new infrastructure; R14 weak until “lane” and “human-owned blocker” are schema-backed; R15 live-only, depends on launchd/gateway access.

2. **Claim:** Wave order and push-per-wave policy make cross-repo migration safe. **Causal layer:** safety. **Why it matters:** pack, architecture-guide, Gaia, home CLAUDE, and installed skill roots cannot be atomically changed; ~10 sessions may read doctrine mid-move. **Falsifying/satisfying evidence:** a cutover ledger with canonical-home commit first, pointer commit second, installed-sync commit third, and drift check green at every intermediate pushed state. **Minimum impact:** split each wave into ordered cross-repo subcommits; do not push a wave whose intermediate state has dangling pointers.

3. **Claim:** Wave 2 may delete five inlined `claude-adversary` copies after V3. **Causal layer:** evidence. **Why it matters:** if Codex does not reliably read shared references, trigger-critical adversary rules disappear. **Falsifying/satisfying evidence:** My current Codex session did read `references/claude-adversary.md` on demand after reading `uberaccept/SKILL.md`/`uberrca/SKILL.md`, which point to it. That proves this session’s skill-following behavior, not a fresh unattended `codex exec` subprocess. **Minimum impact:** keep V3 as a Wave-2 gate; if subprocess proof is absent, retain a short invariant summary in each skill.

4. **Claim:** Uberrca + uberaccept-surprise validators will enforce failure intake. **Causal layer:** design. **Why it matters:** ordinary Codex/Claude flows will skip “append a case” unless the artifact they already need cannot validate without a case decision. **Falsifying/satisfying evidence:** `validate_uber_run_receipt.py`, `validate_acceptance_report.py`, and an RCA artifact validator fail when a material failure/surprise lacks `failure_case_id` or `no_case_reason`. **Minimum impact:** enforce at receipt/acceptance/RCA validators, not only in prose; require `case_added`, `case_updated`, or `not_applicable_with_reason`.

5. **Claim:** New scripts are right-sized. **Causal layer:** cost. **Why it matters:** the plan invents `check_doctrine_drift.py`, `check_skill_install_sync.py`, `validate_failure_case.py`, path-lint, and behavioral evals while this repo already has `lint_pack_contract.py`, `check_scope_fidelity_artifacts.py`, per-skill `lint_skill_package.py`, `quick_validate.py`, and validators for plans, receipts, acceptance, learning, and assessments. **Falsifying/satisfying evidence:** implementation reuses or extends these validators before adding standalone tools. **Minimum impact:** make `lint_pack_contract.py` the root contract aggregator; add install/path/drift modules only where fixtures prove they need separate CLIs.

6. **Claim:** R16a before R5/R8 is enough. **Causal layer:** sequencing. **Why it matters:** R7 precedence and R6 tier semantics must exist before deleting duplicated review/acceptance doctrine; otherwise receipts point to a still-moving authority. **Falsifying/satisfying evidence:** canonical ladder, tier templates, and contradiction fixtures land before dedupe. **Minimum impact:** reorder to R1/R2/R4/R16a scaffold, then R7/R6, then R3/R5/R8/R9.

7. **Claim:** R8/R10/R11 improve power without bloat. **Causal layer:** scope/goal-fit. **Why it matters:** retiring three skills and adding `ubertask`/`uberdebug` are product decisions, not mechanical refactors; they can make the pack smaller but less usable. **Falsifying/satisfying evidence:** usage evidence, trigger fixtures, and operator-approved archive policy. **Minimum impact:** default R10 to an `ubergoal` section and R11 to a reference/loop inside `uberrca` until evals prove standalone trigger value.

8. **Claim:** R14/R15 fit this campaign cleanly. **Causal layer:** feasibility. **Why it matters:** Gaia liveness and Hermes launchd repair require live services, secrets/config, scheduler state, and runtime proof; they are not just doctrine edits. **Falsifying/satisfying evidence:** lane inventory, runnable safe checks, launchd logs, proof-of-life artifact, and exact human-owned blocker classifier fixtures. **Minimum impact:** carve R14/R15 into a Gaia child plan with access assumptions, rollback, and “local docs only” fallback.

9. **Claim:** Effort is ~1 session Wave 1 and tractable thereafter. **Causal layer:** cost. **Why it matters:** underestimating by >2x will recreate pressure to skip eval intake. **Falsifying/satisfying evidence:** implementation tickets with fixture counts and touched repos. **Minimum impact:** re-estimate: Wave 1 = 2-4 Codex sessions / 8-16 hours; Wave 2 = 4-7 sessions / 18-35 hours; Wave 3 = 5-10 sessions / 25-60 hours, with R13/R14/R15 each likely >2x plan estimate. Missing inputs: canonical fingerprint values, schema/sanitization rules, expected routing answer key, install roots policy for symlink vs copy, whether coordination artifacts are committed, live-session cutover protocol, Gaia/Hermes access, and operator decisions on skill retirement/new skill creation.

**Failure-Catalog Pass**

1. `gmail-silent-lane-12d`: SHORTENED; liveness canary detects stale lane, but does not prevent credential expiry.
2. `hermes-overseer-dead-9w`: SHORTENED; R15 helps, but docs-vs-runtime proof is underspecified.
3. `silent-nonresponse-class`: SHORTENED; R11 names class invariants, but surface enumeration is not yet enforced.
4. `false-apology-fix-of-fix`: SHORTENED; red/green rule helps, but “real failure path” fixture is undefined.
5. `scope-laundering-20260528`: PREVENTED; existing scope-fidelity validators plus R7 preserve the invariant if not weakened.
6. `evaluator-saturation`: PREVENTED; known-bad fixtures and demoting scores directly address it.
7. `claw1-path-rot`: WEAK; path-lint can pass on one machine while preserving non-portable assumptions.
8. `install-drift-uberarchitect`: PREVENTED; install-sync with seeded desync is the right test.
9. `doctrine-drift-trio`: SHORTENED; fingerprints catch known strings, not semantic drift.
10. `sandbox-fake-row-shape`: WEAK; R12 says live verify, but no real-interface fixture or contract exists.
11. `dispatch-double-launch`: WEAK; a dispatch contract is not an idempotent launch harness.
12. `human-owned-blocker-grind`: SHORTENED; classifier helps if alerts are stateful and suppress repeats.
13. `op-hang-under-launchd`: WEAK; grep-based evals miss environment-specific hangs.
14. `pg-null-upsert-dup`: WEAK; “run-twice harness pattern doc” is not an executable idempotency gate.

Missed failure class: implementation-runtime writeability and sandbox drift. In this review runtime, `git status` worked but emitted `/tmp/xcrun_db` permission warnings, and the session is read-only. The campaign needs an early git/temp/writeability gate before assigning Codex implementation or promising commits.

**Open Questions Q1-Q4**

Q1: Use an `ubergoal` fast-path section first, not a new `ubertask`; de-escalation should shrink the common path before growing the skill surface.

Q2: Tier 1 is too weak for doctrine edits; cross-repo doctrine/pointer changes should be Tier 2 minimum, and runtime liveness/Hermes fixes Tier 3 when services are touched.

Q3: Uberrca + uberaccept-surprises are insufficient alone; enforce failure-case decisions in existing receipt/acceptance/RCA validators and have the Gaia health loop write runtime-layer cases for repeated alerts.

Q4: Self-reported cost accounting is useful only as a starter field; require `tokens/minutes/lane_used/source` with `unknown` allowed, then replace with wrapper-measured values where available.

**Scope-Fidelity Verdict**

Original-scope satisfaction: no, not yet. The plan addresses process cleanup and some failure automation, but the implementable contract for “automatic,” “more powerful,” and “solve problems faster” is incomplete. Gaps: fresh-agent behavioral eval harness, failure-intake enforcement, live-session cutover mechanics, V3 subprocess proof, and Gaia liveness access/fixtures.

Narrowing check: the plan partially dilutes the operator mandate by treating validator/prose scaffolding as automatic eval enshrinement and by pushing several “power” claims into later capability waves without a measurable speed/productivity target.

VERDICT: MAJOR_CHANGES_REQUIRED — the structure, ordering, and enforcement mechanics need revision before this is safe for implementation.