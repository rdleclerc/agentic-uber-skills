# Round 1 Fable Adversarial Review — design, architecture, goal-fit

Reviewer: independent Fable-class subagent (no stake in plan-v2). Artifacts reviewed: `plan-v2.md`, `scope.md`, `failure-catalog.md`, both review packets. Claims verified directly against `agentic-uber-skills`, `agentic-architecture-guide`, `agfunder-gaia`, home `CLAUDE.md`, and both installed skill roots.

## 1. Role statement

**I accept the adversary role unmodified.** The authoring agent is also Fable; I extend it no courtesy — my review counts only because my evidence was gathered independently, and I gathered it: every load-bearing baseline number was re-measured against the repos before assessment.

**What the operator's instructions require that the plan could narrow:** (a) "better and **more powerful** … code better, solve problems **faster**" — requires demonstrated speed/power gains, not just smaller prose; (b) failure→eval enshrined "**to be automatic** in our coding system and style" — a standing pipe covering every failure path, not selected chokepoints; (c) honest two-week review — the baseline evidence must be accurate, since three items (R6, R8, R9) draw their justification from it; (d) two rounds of codex 5.5 xhigh adversarial review — topology preserved in scope.md, satisfied.

**Three concrete reject conditions (stated before assessment):**

1. **RC1 — evidence base:** if a plan item's justification rests on a baseline claim the repos contradict (e.g., R8's "~zero usage" retirement evidence), the item's decision logic is invalid until re-grounded.
2. **RC2 — safety posture:** if any wave can change live Gaia runtime behavior (anything injected into OpenClaw session context) while classified as a "doctrine-surface" Tier-2 edit without the GAIA_TESTING live-proof gate, the plan's safety posture fails.
3. **RC3 — self-defeating design:** if the dedup/one-home program itself creates or leaves two canonical homes for the same rule, or the "automatic" failure→eval pipe leaves a common failure path with no intake, the plan fails its own P2/P4.

All three reject conditions fire in part. Details below.

**Baseline verification results (checked, not taken on faith):** 19,176 SKILL.md words — exact. Model pin ×10 + AGENTS.md clause — exact. Adversary block ×5 verbatim copies — exact. openclaw-agentic-skill-creator 5,034 words — exact. Two diverged guide copies, both "Version 1.5" (11,657 vs 11,837 lines) — confirmed. Canary command 3 spellings (workspace-symlink form ×5, repo form ×1, relative ×2) — confirmed. Test-channel divergence (`#gaia-test-alpha` in GAIA_TESTING.md:151,443 vs `#gaia-testing-alpha` in workspace CLAUDE.md) with opposite default postures (read-only-default vs pre-approved posting) — confirmed. Home CLAUDE.md stale lane (MiniMax default; workspace reversed to gpt-5.5 default) — confirmed. `learning/processed/` empty since 05-09 — confirmed. **Discrepancies found:** claw1 refs are 12 in skill text but 25 including test fixtures; thread-cap policy appears in 4 SKILL.md files (plan says 2→1); workspace CLAUDE.md is 790 lines today, not 782 (live drift mid-campaign, proving V1 is active now); plan-contract.md has 57 headings, not 54; and **uberarchitect has two real Architecture Stepback Packets dated 2026-06-30 and 2026-07-02 inside the review window** — the "3 skills with ~zero usage in 7 weeks" baseline is false for uberarchitect.

## 2. Challenges (ranked by severity)

**C1. The plan re-creates the dual-authority contradiction it claims to resolve.**
- **Claim:** R1 DoD: lane policy "stated once (**in pack AGENTS.md**)". R5: "opus-lane rule 5→1 (**spine owns**)". R7 resolves B1/B3/B10 to "a single unambiguous instruction."
- **Causal layer:** design.
- **Why it matters:** review-lane policy is the highest-traffic rule in the estate. R1 and R5 assign it two different canonical homes in the same plan. For gaia work run through pack skills — the dominant case — an agent finds a "policy stated once" in pack AGENTS.md *and* a differently-worded canonical rule in the spine. That is exactly contradiction B1 (pin vs best-available) reborn as pack-canonical vs spine-canonical, the proven drift mechanism of catalog case 9.
- **Evidence:** falsified if the plan already designates one owner — it doesn't; R7's precedence paragraph covers lifecycle/acceptance authority, not lane policy.
- **Minimum impact:** one sentence in R7: spine owns lane policy for gaia surfaces; pack AGENTS.md carries the portable default plus an explicit pointer for gaia contexts; both fingerprinted in the R3 drift check. (Structural: changes rule-ownership design.)

**C2. The ≤12,000-word target arithmetically presupposes the retire-or-prove outcome — and the usage evidence behind it is partly false.**
- **Claim:** Wave 2 "net SKILL.md word count … target ≤ 12,000"; R8 is honestly "retire-**or-prove**"; baseline: "3 skills with ~zero usage in 7 weeks."
- **Causal layer:** evidence.
- **Why it matters:** plausible non-retirement subtraction — ubergoal −~2,000 (R6), dedup across five skills −~2,200–2,700, uberskillevolver fossils −~600 — lands at ~13,900–14,400. Reaching ≤12,000 requires archiving essentially all of ubersimplify+uberarchitect+ubershow (900+822+1,273 = 2,995) or gutting uberplan (3,737, untouched by any itemized cut). So the "budget, not a score" (V7) is in fact a decision already made. And the evidence is wrong for one of the three: uberarchitect produced two real stepback packets on 06-30 and 07-02 (`coordination/codex-native-tool-recovery-2026-06-30/architecture-stepback.md`, `coordination/gaia-gmail-nonresponse-uberrca-2026-07-02/architecture-stepback.md`), one predating the audit. RC1 fires.
- **Evidence:** the two artifacts above; the arithmetic; falsified if the author shows an itemized ≤12,000 path that keeps all three skills.
- **Minimum impact:** correct the baseline; publish per-skill word-delta arithmetic with the target; either make the target conditional ("≤12,000 if retirements pass their ROADMAP evaluations, else ≤14,500") or pre-commit that missing the number is acceptable. Treat uberarchitect's stepbacks as counter-evidence in its R8 evaluation. (Structural: changes Wave-2 scope/DoD.)

**C3. R9 edits live runtime behavior while classified as a Tier-2 doc edit.**
- **Claim:** Plan dependencies: gaia-repo edits R9 are "Tier 2 … (doctrine surfaces, no runtime code)." R9 moves "runtime-persona content (Slack etiquette, heartbeats, group-chat rules, live-lane inventory)" out of workspace CLAUDE.md.
- **Causal layer:** safety.
- **Why it matters:** workspace CLAUDE.md is injected into live OpenClaw session context (its own "Session Startup" section: startup context "may already include … CLAUDE.md"). The Slack-etiquette section is Gaia's live posting posture. Moving it to "runtime skills/lane docs" changes what live Gaia sees unless OpenClaw's context assembly provably loads the new home. GAIA_TESTING's own rule — any change affecting Slack-visible behavior requires live Slack proof — applies; R9's DoD (line counts + a fresh-session orientation smoke) contains no runtime-parity or live-Slack proof. A silent etiquette regression in ~10 live sessions is a user-visible production incident caused by a "doc cleanup." RC2 fires.
- **Evidence:** falsified if OpenClaw context assembly is shown to load the destination docs; satisfied by the CLAUDE.md session-startup text.
- **Minimum impact:** split R9 into R9a (coding-process content — Tier 2) and R9b (runtime-persona relocation — GAIA_TESTING live-proof gate, before/after Slack-behavior probe in `#gaia-testing-alpha`). (Structural: changes tiering/safety posture.)

**C4. "Automatic" failure→eval intake misses the highest-volume failure path.**
- **Claim:** P4: intake enforced "at the two chokepoints every failure already passes through (uberrca, uberaccept surprises)."
- **Causal layer:** scope/goal-fit.
- **Why it matters:** the premise is false once R11 exists: uberdebug is *designed* to handle everyday defects **without** uberrca (escalation only on repeated same-class failure). Every ordinary reproduced-red bug — the bulk of real failures — then terminates in a lane with no intake validator. The operator's mandate was "**every** failure is an opportunity … automatic." As written, the pipe is automatic for rare deep failures and honor-system for common ones — a material narrowing of the instruction.
- **Evidence:** R11's own text (uberrca boundary); P4 naming only two chokepoints. Falsified if uberdebug's DoD includes intake.
- **Minimum impact:** add uberdebug's exit as a third validated chokepoint (reproduced-red ⇒ append case or state why not), and say in P4 that chokepoints must cover every terminal failure path, enumerated. (Structural: changes P4 and R11.)

**C5. The tier ladder relocates self-certification to tier self-assignment.**
- **Claim:** R7: "no implementing agent self-approves at any tier ≥1" preserves case 5.
- **Causal layer:** design.
- **Why it matters:** under the ladder, the cheapest laundering move is no longer skipping review — it's *classifying down*. Tier 1 gets one exact-diff review pass; scope-fidelity verdicts are required only at Tier 2+ (catalog case 5's own eval says so). A scope-narrowed task self-classified Tier 1 passes a diff review that never sees the operator-original scope. Who assigns tier? The orchestrating agent — the interested party. This is the binary-maximal problem one level down: the gate that always ran becomes the tier claim nobody audits.
- **Evidence:** falsified if R7 includes tier-assignment audit; it doesn't — R6/R10's 10 canned routing prompts test fresh-agent routing, not adversarial down-tiering on live work.
- **Minimum impact:** receipts record tier + one-line justification; any reviewer's first check is "is the tier right?" with authority to bounce; add ≥2 known-bad under-tiered fixtures to R13. (Structural: changes ladder design.)

**C6. No outcome measurement — the plan cannot prove "faster" or "more powerful."**
- **Claim:** Objective: "cost becomes risk-proportional"; operator: "code better, solve problems faster."
- **Causal layer:** goal-fit.
- **Why it matters:** every success metric in the plan is a process metric (word counts, gates green, evals passing). R13c records tokens/minutes/lane per run — collection, not comparison. Nothing defines before/after outcome measures: time-to-accepted-fix, tokens per accepted change, review-round count, rework rate. The estate could hit every DoD and be no faster; nobody would know. The audit's own instrument-saturation lesson (case 6) applies to the campaign itself: a rearchitecture whose success metric can't say "no" isn't measured.
- **Evidence:** absence of any baseline capture item or comparison in R13/R15; falsified if I missed one — I didn't find it.
- **Minimum impact:** Wave-1 addendum: capture current-cost baseline from existing receipts/artifacts for 3–5 recent representative tasks; R15's weekly report compares post-change runs against it. (Structural: adds a measurement spine the operator's goal requires.)

**C7. The plan's new machinery ships without owners, adoption states, or self-tests — new rot surfaces.**
- **Claim:** P2: "a mechanical drift check replaces the manual propagate-everywhere duty"; R3/R4/R16 add 4–5 standing scripts + a fingerprint list + a two-layer DB.
- **Causal layer:** feasibility / second-order effects.
- **Why it matters:** the fingerprint list is a new manually-maintained coupling: every deliberate rule rewording now requires a fingerprint update, or the check false-positives (gets bypassed — the fate of every noisy gate) or false-negatives (silent, case-2 pattern). R4's DoD includes a seeded-desync test; **R3's does not** — the drift checker itself has no known-bad fixture. Nothing assigns the fingerprint list a home/owner, and the new gates go from birth to wave-blocking with no shadow period, under ~10 concurrent sessions. The estate ends with less prose but strictly more maintained artifacts; the plan never states this inventory or its ownership. (Answering my lens's estate-shape question: smaller prose, larger machinery — defensible per "validators over prose," but only if the machinery has owners and self-tests.)
- **Evidence:** R3 DoD text; absence of adoption-state language (contrast the estate's own sidecar/shadow-mode discipline).
- **Minimum impact:** R3 DoD gains a seeded-divergence test; fingerprint list gets a canonical home + "reword ⇒ update fingerprint" rule in pack AGENTS.md; new gates run report-only for one wave before blocking.

**C8. R10 re-ships a fast path ubergoal already has, without explaining why the existing one failed; word budgets are one-time with no standing enforcement.**
- **Claim:** R10 (Wave 3, "new powers"): micro-intent artifact = scope sentence + acceptance criteria + verify command + out-of-scope note.
- **Causal layer:** design.
- **Why it matters:** ubergoal lines 43–67 already contain exactly this ("Task Understanding Review / Micro-intent fast path": 2–3 sentences scope, checkable acceptance criteria, out-of-scope note, verification command). It exists and the toll persisted — so the root cause is not a missing artifact but non-enforced de-escalation plus context load. R10's genuinely new content is the hard de-escalation rule + evals; the artifact is a rewrite. Same pattern with budgets: pack AGENTS.md already commands "Keep ubergoal thin" — prose that lost to 2,755 words; `lint_pack_contract.py` has no size checks; R6's word counts are checked once at DoD, then nothing prevents regrowth. A plan whose thesis is "prose rules drift; mechanize them" mechanizes neither its fast path's trigger history nor its own budgets.
- **Evidence:** ubergoal SKILL.md:43–67; AGENTS.md edit rules; lint script contents.
- **Minimum impact:** R10 explicitly refactors (not adds) the existing fast path and names its failure cause; add per-skill word budgets to pack lint as a standing test.

**C9. Counting drifts, and the failure DB's dual-layer cases are sanctioned duplication with no drift protection.**
- **Claim:** "12 `/Users/claw1/` references"; "thread-cap policy 2→1"; workspace CLAUDE.md "782 lines"; catalog cases 2/12 are layer "both," "runtime-layer copies may carry more detail."
- **Causal layer:** evidence / cost.
- **Why it matters:** claw1 is 12 in skill text but 25 including test fixtures — R2's path-lint DoD ("every absolute path in skill text") must decide whether fixtures count, or the lint passes while fixtures keep teaching agents dead paths. Thread-cap is ×4 (ubergoal, uberplan, uberaccept, uberskillevolver), so R5's dedup receipt as scoped would leave copies behind. CLAUDE.md at 790 proves doctrine moved during the campaign — V1 is live, not hypothetical. And two-layer "both" cases are two copies of one rule — the exact case-9 mechanism — with no canonical-layer field in the schema and no drift fingerprint on shared case ids. The anti-duplication campaign's own database ships a new duplication class.
- **Evidence:** all measured above; schema draft in failure-catalog.md.
- **Minimum impact:** correct the counts; define path-lint scope over fixtures; extend R5's dedup list to all 4 thread-cap copies; add `canonical_layer` to the case schema + shared-id drift fingerprint.

## 3. Failure-catalog pass (plan as written, fully implemented)

1. **gmail-silent-lane-12d — PREVENTED.** R14 TTL liveness + loud freshness canary bounds silence to the TTL; R16 eval enforces per-lane.
2. **hermes-overseer-dead-9w — PREVENTED.** R15 revival + R14 liveness-on-the-watcher + R3 docs-vs-reality fingerprint close all three gaps.
3. **silent-nonresponse-class — SHORTENED.** R11's repeat-escalation to class-invariant RCA cuts 3 weeks to ~1 cycle; the first point-patch still ships.
4. **false-apology-fix-of-fix — PREVENTED.** R11's reproduced-red-on-real-path rule blocks exactly this ship, if the eval binds it (R11 DoD does).
5. **scope-laundering — WEAK.** Preserved at Tier 2+, but tier self-assignment is unaudited and scope-fidelity verdicts don't exist at Tier 1 — the laundering vector moves down a level (C5).
6. **evaluator-saturation — PREVENTED.** R13 demotion + must-fail known-bad fixtures + variance is the correct instrument-design fix.
7. **claw1-path-rot — PREVENTED.** R2 + standing path-lint; scope over fixtures needs defining (C9).
8. **install-drift-uberarchitect — PREVENTED.** R4 with seeded-desync test; both roots verified symlink-based today, so the check is cheap and decisive.
9. **doctrine-drift-trio — PREVENTED** for fingerprinted rules; coverage is enumerated, not structural — new duplications post-campaign depend on fingerprint upkeep (C7).
10. **sandbox-fake-row-shape — SHORTENED.** R12 promotes the doctrine and orchestrator live-verify catches at review; no named gate forces fake-vs-real-shape comparison at authoring time.
11. **dispatch-double-launch — PREVENTED.** R12 contract (idempotent launch, duplicate cull, disjoint writes) + eval addresses the class.
12. **human-owned-blocker-grind — PREVENTED.** R14c alert-once-with-exact-action-and-stop is the class fix.
13. **op-hang-under-launchd — SHORTENED.** Pattern doc + Hermes applies it; the entrypoint-grep eval isn't wired as a standing gaia gate anywhere in R1–R15.
14. **pg-null-upsert-dup — WEAK.** R16a ships a "harness pattern doc," not an executable run-twice idempotency gate; no GAIA_TESTING mandatory trigger is added for new `--apply` writers, so the next writer can skip it.

**Missing failure classes the catalog omits (from repo history / operational memory):**
- **Credential/secret exposure by agents** (echoing keys into transcripts/files, forcing rotation) — a real incident class in this estate's doctrine; no case, no eval, and no security lane anywhere in the plan.
- **Post-dependency-upgrade silent breakage** (the 2026-04-29 gmail break after `openclaw upgrade` — the stated origin of GAIA_TESTING's trigger) — the trigger exists but no catalog case guards the trigger itself.
- **Pinned-external-identifier rot** (model ids: the pack pins `claude-opus-4-8` in a Fable-5 world) — R1 *is* this failure's fix, yet the class isn't in the DB; the campaign's first item violates its own P4 dogfood rule.
- **Library-silently-truncates-input** (markdownify vs html2text essay ingest) — silent data-loss via tool choice; runtime layer, real recurrence.

## 4. Open questions

- **Q1 (fast path: skill vs section): Section.** The failure was never a missing trigger surface — the fast path already exists inside ubergoal (C8); a separate skill adds routing ambiguity and estate growth while the de-escalation evals do the real work.
- **Q2 (Tier 1 for doctrine edits): Tier 2 minimum, plus:** any surface injected into live OpenClaw session context (workspace CLAUDE.md persona content) additionally takes the GAIA_TESTING live-proof gate, because those edits are runtime behavior changes, not doc edits (C3).
- **Q3 (intake chokepoints): Not sufficient.** Add the gaia alert-RCA intake (per default) **and** uberdebug's exit (C4); state the completeness rule — every terminal failure path has a validated intake — so future lanes inherit it.
- **Q4 (cost accounting): Self-report now, but label every field as estimate and add one deterministic cross-check** in R15 (Hermes compares receipt claims against transcript/log sizes); gameable-but-audited beats absent, and pure self-report on the instrument meant to keep subtraction honest would recreate case 6.

## 5. Scope-fidelity verdict

**Original-scope satisfaction: yes, with gaps.** The plan genuinely covers the two-week review (baseline is mostly accurate and unusually well-evidenced), rearchitecture of all four estates, the failure-eval DB in the approved two-layer shape, and the mandated review topology. Gaps: (1) "solve problems **faster**" has no measurement plan (C6); (2) "**automatic**" enshrinement leaks the everyday-defect path (C4); (3) the audit's security lane finding is dropped entirely — no security-shaped item, case, or eval; (4) the additive-only learning loop is surfaced (R15 telemetry) but nobody owns promotion cadence, so `learning/processed/` can stay empty with better dashboards.

**Narrowing check:** two quiet narrowings. The ≤12,000 target converts "retire-or-prove" into "retire" by arithmetic (C2) — a dilution of the plan's own honesty about R8. And "more powerful" is delivered as evals/telemetry/liveness (real power) but "code better/solve faster" is narrowed to cost *recording* without before/after comparison — the operator could not tell from the plan's receipts whether the goal was achieved.

**VERDICT: MAJOR_CHANGES_REQUIRED** — C1 (dual canonical home for lane policy), C2 (word target presupposes retirements on partly false usage evidence), C3 (R9 runtime-injection mis-tiered without live proof), and C4 (automatic intake missing the commonest failure path) each change the plan's structure, scope, or safety posture, though all are repairable within the existing wave architecture.
