# Round 2 Fable Adversarial Review — design coherence of the revision

Reviewer: fresh Fable-class subagent (no round-1 participation). Reviewed: `scope.md`, `plan-v3.md`, `round1-judgment.md`, `failure-catalog.md` (v2); diff context from `plan-v2.md` + both round-1 reviews. Re-verified against the repos: pin-enforcing lint (confirmed), thread-cap ×4 (ubergoal:113 / uberplan:164 / uberskillevolver:152 / uberaccept:54), 19,176 pack words (exact), micro-intent section (ubergoal:43), both uberarchitect stepback packets (exist), channel divergence (GAIA_TESTING.md:151,443 `#gaia-test-alpha` read-only-default vs workspace CLAUDE.md:471–473 `#gaia-testing-alpha` pre-approved posting — **same channel ID `C0AUSU28ND7`, two names, two postures**), `~/.codex/skills` extras (match R4's ignore list), AGENTS.md:21 pin clause (present).

## 1. Role statement

**Accepted, unmodified.** I attack the revision, not round-1 rulings. Reject conditions:

1. **Nominal resolution:** any of the four safety/structure rulings (#1 R9b live gate, #3 P4 completeness, #4 tier audit, #6 reorder) is re-stated without a named binding mechanism (validator, fixture, gate, owner) → MAJOR.
2. **New hole from the fix:** the governance rework itself creates a new two-home rule or a new unaudited self-classification path that no listed fixture covers, and the repair is structural rather than a spec-line → MAJOR.
3. **Invariant weakening:** any round-1 fix leaves scope fidelity, live-proof-before-done, or no-self-approval weaker than in v2 → MAJOR.

Findings: RC1 does not fire (all four bind real mechanisms). RC2 fires **partially** — two genuine holes (NC1, NC3), both spec-line repairable, so no MAJOR. RC3 does not fire; invariants are strengthened (Tier-1 scope echo, tier bounce authority, R9b gate).

## 2. Resolution audit (19 rows)

| # | Status | Evidence (plan-v3) |
|---|---|---|
| 1 | RESOLVED | R9b: moves ONLY after (a) context-assembly citation, (b) before/after probe in alpha channel, (c) single-commit rollback; "Tier 3 if any ambiguity remains" |
| 2 | RESOLVED | Governance: "spine owns review-lane policy for gaia surfaces," pack carries portable default + explicit pointer, both fingerprinted; R1 reworded to match |
| 3 | PARTIAL | P4 enumerates 4 chokepoints + validator fields — but R6 answer key prompt 1 = "Tier 0, no artifacts," and R11's reference-form exit names no binding artifact at Tier 1 (NC3) |
| 4 | RESOLVED | Governance: receipt records tier+justification; reviewer's FIRST check w/ bounce authority; Tier-1 scope echo; R13 ≥2 under-tiered fixtures (Tier-0 residual → NC3) |
| 5 | RESOLVED | "Corrected baseline" section: 19,176 exact; uberarchitect two packets as keep-side evidence; thread-cap ×4; claw1 12/~25 + fixtures decision; conditional ≤12,000/≤14,500 + per-skill delta arithmetic |
| 6 | RESOLVED-BUT-BREAKS | Wave-2 entry block exists and is correctly placed — but its rule's letter ("No deletion before… precedence/ladder exist") is violated by Wave 1's own R1/R2 deletions (NC2) |
| 7 | RESOLVED | Cutover-ledger section: canonical→pointers→install-sync ordered subcommits, drift green per pushed state, no dangling pointers, ledger in wave receipt |
| 8 | RESOLVED | Measurement spine: 5 named baseline candidates, R13c fields, R15 comparison + one deterministic cross-check, DoD gains "outcome comparison published" (delivery risk → NC5) |
| 9 | RESOLVED | Every item carries typed Tests (EXEC/FIX/CHK/LIVE) with fixtures; all judgment-#9 minimum contents present (R2 portability oracle, R6 answer key, R7 fixtures, reproduced-red defined, R14 durable alert state) |
| 10 | PARTIAL | Instances bound (R3/R4 as aggregator modules; R1 migrates lint 106–109 w/ negative fixtures) but the standing rule sentence ("new CLIs only where fixtures prove need") appears nowhere in v3 body — future tools inherit nothing |
| 11 | RESOLVED | `references/drift-fingerprints.toml`, owner = pack maintainer, reword-⇒-update rule in AGENTS.md, seeded-failure self-tests in DoD, report-only wave w/ adoption state in registry; V9 names all owners |
| 12 | RESOLVED | R14+R15 = own file, Tier 3 where services touched, access assumptions enumerated, plist-pair rollback, `blocked_human_owned` fallback |
| 13 | RESOLVED | Catalog 20 cases; schema v2 `canonical_layer`; secret-scan in R16a Wave-1 build list; security lane out-of-scope in operator-decision register #1 |
| 14 | RESOLVED | R10 = "refactor of ubergoal's EXISTING micro-intent section," names the failure cause; standing per-skill word budgets in pack lint — caveat: R6's content list omits the section R10 presupposes (NC2b) |
| 15 | RESOLVED | R11 "separate skill ONLY if R6/R10 smoke evals show distinct trigger value"; exit is an intake chokepoint either way (binding gap for reference form → NC3) |
| 16 | PARTIAL | Ranges adopted; 7 of 8 implementer inputs bound — but the test-channel fingerprint entry names the string without stating which posture sentence wins (NC4) |
| 17 | RESOLVED | R5 entry gate: "session-level Codex reference-following CONFIRMED; subprocess case unproven"; fresh `codex exec` probe gates dedup; 2-line summary fallback |
| 18 | RESOLVED | R13d: "owner: operator; cadence: per-wave during campaign, monthly after; Hermes surfaces the backlog" + register #3 |
| 19 | RESOLVED | Catalog table carries judge-final verdicts + v3 repair column; plan delta references merged verdicts |

15 RESOLVED / 3 PARTIAL / 1 RESOLVED-BUT-BREAKS. No NOT-RESOLVED.

## 3. New challenges (max 5)

**NC1. The R6 smoke eval's isolation requirement forces duplication of the ladder the governance section says is stated once.**
- **Claim:** Governance: "Tier ladder (stated once, spine owns; pack points)." R6: fresh subagent routes each prompt "**reading only the new ubergoal**," with expected answers like "Tier 3 + live gate," "Tier 2 + drift-registry update."
- **Causal layer:** design.
- **Why:** to pass the smoke as designed, ubergoal's "tier table" must carry enough tier semantics — including the riders (live-injection ⇒ GAIA_TESTING gate; cross-repo doctrine ⇒ Tier 2; services ⇒ Tier 3) — to classify all 10 prompts without a hop. That is a functional second copy of the estate's most safety-relevant rule, drift-protected only on its header line: the case-9 mechanism reintroduced on the rule that decides review rigor for everything. When ubergoal and the spine diverge below the header, an agent cannot tell which governs.
- **Evidence:** Governance ¶2; R6 Tests; R3 registry ("tier-ladder header line"). Falsified if the registry entry were the whole table or the smoke allowed a pointer hop — it's neither.
- **Minimum impact:** one decision, stated: either fingerprint ubergoal's entire condensed tier table against the spine ladder (registry entry = full table), or relax the smoke to "ubergoal + one pointer hop" and grade the hop. Spec-line fix.

**NC2. The reordered wave structure contains two wording-level self-contradictions an implementer will trip on.**
- **Claim:** (a) Wave-2 entry block: "No deletion before its canonical home AND the precedence/ladder exist" — yet Wave-1 R1 **deletes the AGENTS.md pin clause** and R2 deletes Type0 paragraphs + dead storage paths, all before R7 lands. (b) R6's ubergoal content list ("routing table, tier table, scope gate, completion rule, pointers") omits the micro-intent fast path, which answer-key prompt 2 and Wave-3 R10 ("refactor of ubergoal's EXISTING micro-intent section") both presuppose survives R6.
- **Causal layer:** sequencing / internal consistency.
- **Why:** a literal implementer (unattended Codex sessions, per the effort section) either blocks Wave 1 on the entry rule or learns the rule is ignorable — both bad; and R10's referent can be compressed away in Wave 2, turning "refactor of existing" into a silent rewrite.
- **Evidence:** entry-block text vs R1 ("delete AGENTS.md pin clause") and R2 ("delete Type0 paragraphs"); R6 list vs R10 premise; ubergoal:43 holds the section today.
- **Minimum impact:** scope the entry rule ("no dedup/retire/unify deletion of a rule surviving elsewhere; same-commit replacements and dead-content removals with P1 receipts exempt") and add "micro-intent fast path" to R6's content list. Wording only.

**NC3. P4's completeness rule is not enforceable as stated — the four chokepoints do not cover Tier-0/Tier-1 terminal paths.**
- **Claim:** P4: "**every** terminal failure path has validator-enforced intake," enumerating uberrca exit, uberaccept surprises, uberdebug/R11 exit, gaia alert-RCA loop.
- **Causal layer:** design / goal-fit ("every failure… automatic").
- **Why:** Tier 1 takes "one exact-diff review pass," not uberaccept — `validate_acceptance_report.py` never sees it; if R11 lands in reference form, its "validated exit" names no artifact or validator for the everyday Tier-1 defect (the highest-volume path — the same volume-end leak M3 closed one level up). And Tier 0 is explicitly "no artifacts" (answer key prompt 1), contradicting "every terminal failure path" unless a de minimis rule is stated. The same blind spot infects ruling #4: tier-audit runs on receipts; Tier 0 produces none, so down-tiering to 0 is runtime-unauditable — only offline behavioral evals cover it.
- **Evidence:** P4; Governance ladder; R6 answer key (1); R10 "exactly one artifact"; R11 "validated intake chokepoint EITHER WAY" with no mechanism named for the reference form.
- **Minimum impact:** two spec lines: (i) the Tier-1 micro-intent artifact gains the `failure_case_id | case_updated | not_applicable_with_reason` field, checked by a validator named in R10/R11 (field infrastructure ships in Wave-1 R16a anyway); (ii) state the Tier-0 boundary (typo/cosmetic only; anything fixing observed misbehavior is ≥Tier 1) plus a cheap audit hook (`tier0:` commit trailer Hermes can sample).

**NC4. The fingerprint registry smuggles a live safety-posture decision inside a "string unification."**
- **Claim:** R3 initial registry: "test channel `#gaia-testing-alpha` (+ its approval posture sentence)."
- **Causal layer:** evidence / implementability (judgment #16 required this resolved).
- **Why:** verified: GAIA_TESTING.md says `#gaia-test-alpha`, **default read-only**; workspace CLAUDE.md says `#gaia-testing-alpha`, **pre-approved posting** — same channel, opposite defaults. R5 makes GAIA_TESTING the canonical owner of test doctrine, yet the registry canonicalizes the *other* file's spelling and never says which posture sentence wins. Codex at Wave-2c must either loosen the canonical owner's read-only default (a safety-posture change shipped as string cleanup, no decision receipt) or tighten to read-only — contradicting R9b's own protocol, whose live probes require posting there.
- **Evidence:** GAIA_TESTING.md:151,443; workspace CLAUDE.md:471–473; R9b probe requirement.
- **Minimum impact:** the registry entry states the winning sentence verbatim (workspace 471/473 content, since R9b depends on it), logs it in the operator-decision register, and GAIA_TESTING.md is edited to carry it as owner.

**NC5. The campaign's only named outcome-comparator is its most-blockable item.**
- **Claim:** DoD: "Outcome comparison published"; spine: "**R15's weekly Hermes report** compares post-change runs against baseline."
- **Causal layer:** feasibility.
- **Why:** the spine's metrics do measure the operator's goal (time-to-accepted-change, review rounds, tokens/change, rework — "faster" directly; "more powerful" proxied by the catalog status ladder). But delivery is single-pointed on R15 — launchd exit-78 repair, Tier 3, the one item with an explicit `blocked_human_owned` fallback. If R15 lands in fallback mode, the DoD is unsatisfiable or quietly waived — the "process metrics green, goal unmeasured" pattern M8 existed to kill.
- **Evidence:** Measurement spine ¶3; child-plan fallback clause.
- **Minimum impact:** one sentence: if Hermes is blocked, the orchestrator publishes the first comparison manually from R13c receipts.

## 4. Catalog v2 check

**Schema v2: sound.** `canonical_layer` on every case resolves the sanctioned-duplication hole; the shared-id drift fingerprint is coherent with R3's cross-repo checker; the `status` ladder doubles as the "more powerful" metric. Cases 2/12 correctly carry `both (runtime)`.

**Mappings: four minor gaps, no mis-mapped verdicts.** (i) Case 16's eval ("weakening the post-upgrade canary mandate fails the drift check") needs that mandate's sentence in R3's **initial** registry — it isn't there, so case 16 ships citing an eval that doesn't exist. (ii) Case 20 has no owning R-item to make "load-bearing plan claims cite checkable artifact paths" standing (natural homes: uberplan's plan contract + an R13 fixture). (iii) Cases 17 (class-eval beyond R1's fixtures) and 18 (ingest sanity thresholds) have evals unscheduled in any wave — legitimate at `status: seed`, but name landing items (17→R3/R13, 18→child plan) so they don't rot. (iv) Case 8's ignore list verified correct against the actual install.

**Case-20 dogfood: legitimate.** A real round-1 failure (false uberarchitect usage claim justifying R8), process-layer, sanitized, entered through the campaign's own P4 loop — the operator's mandated behavior, and first proof the pipe works.

## 5. Verdict

All five challenges are spec-line repairs — none requires re-sequencing, re-scoping, ownership redesign, or a new safety gate; the round-1 structural fixes are bound, not renamed.

VERDICT: MINOR_CHANGES_ONLY — implementation may start; fold NC1–NC5 (plus the row-10 standing-rule sentence and the four catalog notes) into Wave-1 execution as plan-text amendments before the first dedup/retire commit.
