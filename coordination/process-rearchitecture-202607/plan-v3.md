# Plan v3 — Process Rearchitecture (R1–R16)

Status: REVISED after round-1 adversarial review (Fable + Codex gpt-5.5 xhigh, both MAJOR_CHANGES_REQUIRED; Fable judge reconciliation in `round1-judgment.md`, 19 ordered changes; orchestrator accepted all 19). This document supersedes `plan-v2.md` and is the artifact for round 2. Companion docs: `scope.md` (operator instructions + approvals), `failure-catalog.md` (NOW 20 cases, schema v2).

## Delta from v2 (round-1 changes, by judgment item #)

#1 R9 split (R9a doc / R9b runtime-injected persona w/ live-proof gate) · #2 lane-policy single ownership · #3 P4 completeness rule + validator-enforced intake at 4 chokepoints · #4 tier-assignment audit · #5 corrected baseline + conditional word target + corrected counts · #6 reorder (R7/R6 before dedup/retire) · #7 cross-repo cutover ledger · #8 measurement spine · #9 per-item test matrix · #10 tooling-reuse rule · #11 machinery owners/adoption states · #12 R14/R15 Gaia child plan · #13 catalog →20 cases + canonical_layer + minimal secret-scan eval + explicit security-lane out-of-scope note · #14 R10 as refactor + standing word budgets · #15 R11 form evidence-contingent · #16 effort re-estimated + implementer inputs resolved · #17 V3 probe status recorded · #18 learning-promotion owner/cadence · #19 catalog mapping updated to merged verdicts.

## Objective (unchanged in intent)

Rearchitect the coding-process estate — `agentic-uber-skills` (10 skills), `agentic-architecture-guide/skills` (7), gaia doctrine surfaces, home CLAUDE.md — preserving the proven rigor invariants while making cost risk-proportional, giving every rule exactly one home, making failure→eval intake automatic on **every terminal failure path**, and making liveness a property of every unattended lane.

### Definition of Done (campaign) — amended

- All 16 items landed or explicitly re-scoped with operator approval; per-item DoD + test-matrix checks met with receipts here.
- Pack contract tests (extended aggregator), per-skill tests, quick_validate green; drift-check, install-sync, path-lint green across surfaces — each new check with a seeded-failure self-test, and report-only for one wave before blocking.
- Wave-2 word target **conditional**: ≤12,000 pack SKILL.md words if R8 retirements pass their evaluations; else ≤14,500. Per-skill delta arithmetic published in the wave receipt. Missing the number with behavior preserved and receipts explaining why is acceptable (budget, not a score).
- Failure-eval DB live in both layers, 20 seed cases, `canonical_layer` on every case, validator-enforced intake at all four chokepoints, ≥1 executable eval per Wave-1-buildable case, minimal secret-pattern scan eval included.
- **Outcome comparison published**: post-change runs compared against the Wave-1 cost baseline (see Measurement spine).
- Every wave committed + pushed per the cutover ledger; campaign-internal failures appended to the DB (dogfood; includes the round-1 baseline errors — see catalog case 20).

## Corrected baseline (errors found in round 1 — themselves catalog case 20)

- 19,176 pack SKILL.md words (exact; note openclaw-agentic-skill-creator's 5,034 words live in the guide repo, OUTSIDE this baseline and outside the word target).
- **uberarchitect is in real, recent use**: two genuine Architecture Stepback Packets (2026-06-30 codex-native-tool-recovery; 2026-07-02 gaia-gmail-nonresponse-uberrca). "3 skills ~zero usage" was false for it; R8 treats this as keep-side evidence. ubersimplify and ubershow remain without real-usage artifacts.
- Thread-cap policy appears in **4** SKILL.md files (ubergoal:113, uberplan:164, uberaccept:54, uberskillevolver:152), not 2.
- `/Users/claw1/` refs: **12** in doctrine text (9 SKILL.md + 3 AGENTS.md), **~25** including test fixtures + the lint constant. R2 states the fixtures decision explicitly.
- Workspace CLAUDE.md is 790 lines today (was 782 at audit — live drift mid-campaign; premortem V1 is active fact).
- `lint_pack_contract.py:106–109` **enforces** the opus-4-8 pin — R1 is a lint+tests migration with negative fixtures, not a frontmatter edit.
- plan-contract.md has ~57–58 headings (immaterial to the tiering argument).

## Design principles (P4 amended)

- P1. Subtraction with instrumentation: no scar deleted without its invariant moved to a named home; deletion receipts map old text → new home.
- P2. One canonical home per rule; pointers elsewhere; mechanical drift check with an owned fingerprint registry replaces manual propagation.
- P3. Risk-priced gates; a gate that always passes or always maxes is miscalibrated.
- **P4 (amended). Failure→eval is a standing pipe with a completeness rule: every terminal failure path has validator-enforced intake.** Enumerated chokepoints today: uberrca exit, uberaccept surprise rows, uberdebug/R11 exit, gaia alert-RCA loop. Enforcement lives in the validators agents already must pass (`validate_uber_run_receipt.py`, `validate_acceptance_report.py`, new RCA validator): each requires `failure_case_id | case_updated | not_applicable_with_reason`. Any future lane inherits the obligation at birth.
- P5. Liveness is a property of lanes; anything scheduled/unattended exposes TTL-bound proof of life.

## Measurement spine (new — judgment #8)

- **Wave-1 baseline capture**: from existing receipts/coordination artifacts, record cost for 3–5 recent representative tasks (candidates: model-week WS2-S2 orphan-edge reconciliation; comms-campaign E1 gmail outcome contract; a small Tier-1-equivalent fix; the gbrain read-mirror plan cycle; one automated health-RCA run): tokens where recorded, wall-clock span, review rounds, rework commits, artifact count.
- **Receipt fields (R13c)**: `tokens / minutes / lane_used / source` — self-reported, `unknown` allowed, estimates labeled.
- **Comparison**: R15's weekly Hermes report compares post-change runs against baseline (time-to-accepted-change, review rounds, tokens/change, rework rate) and runs one deterministic cross-check per week: receipt claims vs transcript/log sizes. Campaign DoD requires the first comparison published.

## Governance (R7 detail — judgment #2, #4; Q2 riders)

- **Single ownership of review-lane policy**: the gaia **spine** owns review-lane policy for gaia surfaces. Pack **AGENTS.md** carries only the portable default ("highest-capability available Claude lane; record `lane_used`; never silently downgrade") plus an explicit pointer: "in gaia contexts the spine's lane policy governs." Both statements fingerprinted. R1's DoD is reworded to match — no second canonical home.
- **Tier ladder (stated once, spine owns; pack points)**: Tier 0 none · Tier 1 one exact-diff review pass by a capable lane **including a one-line scope echo against the operator-original ask** · Tier 2 exact-diff + independent adversarial lane + scope-fidelity verdict · Tier 3 full 4-phase opus-family ladder + review-board lanes. Riders: cross-repo doctrine/pointer edits = Tier 2 minimum; any surface **injected into live OpenClaw session context** additionally takes the GAIA_TESTING live-proof gate (they are runtime behavior changes); runtime liveness/Hermes service work = Tier 3.
- **Tier-assignment audit (anti-down-tiering — catalog case 5)**: every receipt records `tier` + one-line justification; every reviewer's FIRST check is tier correctness with bounce authority; R13 ships ≥2 known-bad under-tiered fixtures that must be caught.
- **Precedence** (gaia AGENTS.md + pack AGENTS.md, identical fingerprinted sentence): ubergoal wraps the spine lifecycle for gaia work; the uber run receipt satisfies the spine receipt contract; uberaccept IS the acceptance review; the claude-adversary lane is the required Tier-2+ independent lane, opt-in below.
- **No implementing agent self-approves at Tier ≥1** (unchanged, non-negotiable).

## Items (with test matrix — judgment #9; check types: EXEC = executable w/ known-bad fixture, FIX = fixture-backed, CHK = checklist, LIVE = live-proof)

### Wave 1 — scaffold + mechanical

- **R1. Unpin models (lint migration).** Migrate `lint_pack_contract.py:106–109` + associated tests from pin-enforcement to pin-PROHIBITION (no hardcoded model ids in pack frontmatter); delete AGENTS.md pin clause; add portable lane-policy default + gaia pointer per Governance. Receipt template gains `lane_used`. Tests: EXEC — negative fixtures both ways (a pinned skill must fail; an unpinned skill must pass); AGENTS.md fingerprint in drift check.
- **R2. Portability rot.** Fix/parameterize 12 doctrine-text claw1 refs (repo-relative or `UBER_GUIDE_ROOT` w/ documented fallback); correct ubergoal work-contract pointers to the real guide path; delete Type0 paragraphs; remove dead storage paths. **Fixtures decision**: test fixtures keep claw1 strings ONLY where the fixture explicitly tests path-handling; otherwise neutralized to example.invalid paths — each retained instance carries a `# fixture-path: intentional` marker the lint exempts. Tests: EXEC — path-lint as a `lint_pack_contract.py` module: (a) nonexistent absolute paths in doctrine text fail; (b) **portability oracle**: machine-specific absolute paths (`/Users/<name>/…`) in portable text fail even if they exist here, unless parameterized or marker-exempted.
- **R3 (tool build only in Wave 1; unifications move to Wave 2c).** Build `check_doctrine_drift.py` as a module of the pack contract aggregator, cross-repo capable. **Canonical fingerprint strings (initial registry)**: test channel `#gaia-testing-alpha` (+ its approval posture sentence); canary command repo-root spelling `/Users/rob/repos/agfunder-gaia/scripts/run_gateway_health_canary.sh`; lane-policy sentences (spine + pack versions); precedence sentence; tier-ladder header line; guide version line `Version: 1.5` (must match across both copies until R3a stubs one). Registry lives at `references/drift-fingerprints.toml` with owner = pack maintainer, rule in AGENTS.md: "reword a fingerprinted rule ⇒ update registry in the same commit." Tests: EXEC — seeded-divergence self-test (a fixture doc pair that must fail); report-only for one wave before blocking (adoption state recorded in the registry file).
- **R4. Install-sync check.** Module in the aggregator: repo skill dirs ↔ `~/.claude/skills` ↔ `~/.codex/skills`; symlink-target equality (policy: **symlink is the required install mode**, both roots verified symlink today); explicit ignore-list for non-pack extras (`chronicle`, `harmonic`, `codex-primary-runtime`, `gaia-session-lane`, plus the guide-repo skills listed by name). Tests: EXEC — seeded desync fixture (temp roots); current install passes.
- **R16a. Failure-eval DB scaffold + seed (20 cases).** Two-layer per approval; schema v2 (see catalog: adds `canonical_layer`, `status`, sanitization rules); `validate_failure_case.py` (shared, invoked by both repos' test suites); cross-index per layer + shared-id drift fingerprint; intake enforcement wired into `validate_uber_run_receipt.py` + `validate_acceptance_report.py` + new `validate_rca_artifact.py` (fields per P4; RCA validator also requires `class_invariant` + `surface_enumeration` fields — case 3). Executable evals built in Wave 1: path-lint (case 7), install-sync (case 8), drift (case 9), **secret-pattern scan over pack + coordination artifacts** (case 15, minimal security eval), run-twice idempotency helper skeleton (case 14, gaia layer). Tests: EXEC validator w/ invalid-case fixtures; CHK for checklist-only cases (each names its checklist location).
- **Wave-1 addendum: measurement baseline** (see Measurement spine) + **dispatch-preflight writeability gate** (case 19): before any implementation dispatch or commit promise, probe git writeability + temp-dir writability in the target runtime; EXEC, part of R12's contract but shipped early since implementation starts at Wave 1.

### Wave 2 — governance first, then subtraction

- **Wave-2 entry block (ordering rule — judgment #6): R7 then R6 land BEFORE any dedup/retire/unify. No deletion before its canonical home AND the precedence/ladder exist.**
- **R7. Ladder + precedence + tier audit** per Governance section. Tests: FIX — contradiction fixtures for resolved pairs B1/B3/B10 + two-router B2 (each fixture: the old contradictory pair, expected single answer); tier-audit fixtures (2 known-bad under-tiered receipts must bounce).
- **R6. Thin ubergoal + tiered plan templates.** ubergoal ≤800 words (routing table, tier table, scope gate, completion rule, pointers); `templates/plan-tier1.md` (~10 sections); 54-section contract → `plan-tier3.md`, reserved. Tests: FIX — **routing answer key** (10 prompts, checked in): (1) typo fix in one script → Tier 0, no artifacts; (2) add a CLI flag w/ test → Tier 1 micro-intent; (3) refactor Slack lifecycle plugin → Tier 3 + live gate; (4) new vendor integration → Tier 2 + canary per GAIA_TESTING; (5) "keep fixing flaky test until green" → loop_mode + Loop Contract; (6) reword doctrine rule in 2 repos → Tier 2 + drift-registry update; (7) delete dead module → Tier 1 + deletion receipt; (8) prompt-only skill tweak → Tier 2 (behavior surface); (9) research "should we adopt X" → uberassess, no goal; (10) production launchd service edit → Tier 3 + Gaia child-plan rules. Fresh-agent smoke: each prompt routed by a fresh subagent reading only the new ubergoal; grade vs key.
- **R5. One home per rule.** As v2, corrected: thread-cap 4→1; adversary block 5→1 (subject to Wave-2 entry gate below); TUR 2→1; blocked-state machine 4→1; Gall's-Law 4→1; cross-repo: affordance-proof 3→1 (guide owns), opus-lane 5→1 (spine owns per Governance), test-trigger 4→1 (GAIA_TESTING owns), coordination-roles 4→1, memory-split 4→1. Every deduped rule → fingerprint registry. Tests: EXEC drift check (now blocking); deletion receipt (old text → new home, per P1) validated by `check_scope_fidelity_artifacts.py` extension; pack tests green.
  - **Wave-2 entry gate (V3/judgment #17)**: fresh unattended `codex exec` subprocess probe — a task requiring content that exists only in `references/claude-adversary.md`; if the subprocess doesn't read it, each skill keeps a 2-line essential summary + pointer (round-1 evidence: session-level Codex reference-following CONFIRMED; subprocess case unproven).
- **R8. Retire-or-prove + compress (evidence-corrected).** uberarchitect: evaluation runs with its two real stepback packets as keep-side evidence (likely outcome: keep, possibly slimmed). ubersimplify + ubershow: ROADMAP retirement evaluations with pass/fail contract = "a named owner + a real triggering task class observed in coordination history + an eval that would exercise it within one month"; fail ⇒ archive (uninstall both roots, tombstone in README, restore = symlink; **operator approves final archive decisions in the wave acceptance** — recorded as operator decision). openclaw-agentic-skill-creator 5,034 → ≤1,500 (guide repo; outside pack word target — counted separately in receipt). uberskillevolver fossils → 4 catalog cases + one reference. Tests: CHK per-skill decision receipts; FIX — archived-skill resurrection check (symlink restore documented + tested once).
- **R9a. Cold-start slim, coding-process content (Tier 2).** Workspace CLAUDE.md coding-process sections → ≤~250 lines routing+pointers; INIT.md = single unconditional read; remaining mandates annotated (size + trigger). Tests: FIX — fresh-session orientation smoke (agent given only INIT.md finds spine, testing doctrine, review ladder in ≤3 hops); no-deletion-without-pointer receipt.
- **R9b. Runtime-persona relocation (GAIA_TESTING live-proof gate — judgment #1).** Persona content (Slack etiquette, heartbeats, group-chat rules, live-lane inventory) moves ONLY after: (a) verified statement of how OpenClaw context assembly loads the destination (config/code citation, not assumption); (b) before/after Slack-behavior probe in `#gaia-testing-alpha` (same prompt, same channel, pre/post move; response posture unchanged); (c) rollback = single-commit revert restoring the section. Tests: LIVE probe receipts; Tier 3 treatment if any ambiguity about context assembly remains.
- **Wave-2 standing tests (judgment #14)**: per-skill word budgets in pack lint (ubergoal 800; each other skill: its post-Wave-2 count +10% headroom; budgets in the lint config, updated only with a receipt).

### Wave 3 — capability (each independently shippable)

- **R10. Fast path = refactor of ubergoal's EXISTING micro-intent section** (it already contains the exact artifact — the failure was non-enforced de-escalation + 2,755 words of router around it, which R6 fixes). New content: hard de-escalation rule (Tier 0/1 defaults to micro-intent unless a named risk triggers escalation; never for runtime/provider/security/data-subject surfaces) + the de-escalation evals. Section, not new skill (Q1 unanimous). Tests: FIX — routing answer key extension (5 small-task prompts → exactly one artifact; 5 risky prompts → still escalate); known-bad: a "quick fix" prompt touching provider routing must escalate.
- **R11. Debug/verify loop (form evidence-contingent — judgment #15).** Content: reproduce → hypothesize → bisect → fix → verify; **reproduced-red receipt defined**: failing command/output captured pre-fix on the real failure path (or explicit `no_repro_reason`), referenced in the acceptance artifact — validator-checked (case 4); repeat-same-class ⇒ uberrca with class-invariant + surface enumeration (case 3). Form: separate skill ONLY if R6/R10 smoke evals show distinct trigger value vs uberrca (uberrca is deliberately heavyweight/never-auto — a lightweight loop folded into it inherits the wrong trigger surface); else reference + ubergoal routing row. Its exit is a validated intake chokepoint EITHER WAY (P4). Tests: FIX — 2 catalog-case evals (3, 4) bound to its exit validator.
- **R12. Dispatch + parallel-session contract.** `references/dispatch-and-sessions.md` (single home): direct codex exec, duplicate cull, checkpoint-commit before dispatch, orchestrator owns git+DB, disjoint write scopes, live-verify sandbox-blind claims + **interface-shape receipt** when fakes stand in for external interfaces/DB (case 10, acceptance-validator-checked), session claim/handoff rules, **dispatch ledger + claim-before-launch + duplicate-cull check** (case 11), **writeability preflight** (case 19, shipped Wave 1). Tests: EXEC — dispatch-ledger validator + duplicate-cull fixture; FIX — fake-shape receipt fixture.
- **R13. Instrument replacement.** (a) `evaluate_skill_quality.py` → renamed lint, scores demoted from quality claims; (b) fresh-agent behavioral evals: routing answer key + under-tier fixtures + de-escalation prompts, run via subagent, transcript-graded vs key; (c) receipt cost fields per Measurement spine; (d) net-negative learning rule in uberskillevolver + **learning-promotion owner: operator; cadence: per-wave during this campaign, monthly after; Hermes surfaces the backlog** (judgment #18). Tests: EXEC — known-bad skill fixture MUST fail the new instrument (case 6); FIX — ≥12 behavioral prompts w/ expected routings including 2 under-tiered.
- **R14+R15 = Gaia child plan** (same campaign, own file `gaia-child-plan.md`, Tier 3 where services touched — judgment #12). Contents: lane inventory w/ per-lane liveness status asserting docs' "live" claims against artifacts (case 2 repair); TTL proof-of-life + loud freshness canary contract (GAIA_TESTING owns; new-lane checklist added to mandatory triggers); human-owned blocker classifier w/ **durable alert state** (alert once, exact human action, stop auto-repair — case 12); standing op-hang entrypoint check (case 13) + `--apply` run-twice idempotency trigger (case 14) into GAIA_TESTING; Hermes: diagnose launchd exit-78 (op-hang pattern is candidate cause), repair, proof-of-life on itself, weekly bundle gains 5 process-telemetry sections (skill counts, cost-per-run + deterministic cross-check, drift/install-sync output, failure-DB delta, learning backlog). **Access assumptions**: local machine, launchd user domain, `~/.hermes/`, provider gateway, secrets via cache-first+timeout pattern. **Rollback**: every service edit is a versioned plist/script pair, restore = previous file + `launchctl bootout/bootstrap`. **Fallback** if access blocked: land docs/contracts + canaries as far as testable, mark lane items `blocked_human_owned` with exact operator action. Tests: LIVE — one scheduled Hermes run producing report + proof-of-life; EXEC — lane-inventory validator; canary FIX per fixed lane.

## Cross-repo cutover ledger (judgment #7)

Per wave, ordered subcommits, each pushed state green: (1) canonical home lands (pack or spine or GAIA_TESTING); (2) pointers land in all other surfaces; (3) install-sync/stub commits. Drift check runs at every step (report-only in its first wave). No pushed state may contain a dangling pointer. The ledger (which commit did what, per rule) is appended to the wave receipt. Live-session cutover protocol: doctrine moves are single-commit-per-file-complete (old text deleted + pointer added atomically per file); waves announced in the coordination folder; other machines converge via push-per-wave.

## Effort (adopted from round-1 Codex, as planning input)

Wave 1: 2–4 Codex sessions (8–16h) · Wave 2: 4–7 (18–35h) · Wave 3: 5–10 (25–60h); R13/R14/R15 flagged >2× original guess. Orchestrator checkpoints between sessions; budget pressure NEVER waives intake/validator gates (that pressure is exactly how case-6-class rot started).

## Premortem (V1–V8 carried, amended; V9 new)

- V1 ACTIVE (CLAUDE.md drifted 782→790 mid-campaign): mitigated by cutover ledger + fingerprints.
- V2 deletion receipts now validator-checked (P1).
- V3 subprocess probe = Wave-2 entry gate (session-level evidence recorded).
- V4 routing regressions: answer key + under-tier fixtures.
- V5 Hermes scope: child plan boundaries + fallback.
- V6 archived-skill resurrection: tombstone + tested restore path; operator approves archives.
- V7 word-target Goodhart: target now conditional + receipts; standing budgets prevent regrowth instead of one-time counting.
- V8 cross-repo atomicity: cutover ledger.
- **V9 (new): the campaign's own machinery rots** — fingerprint registry stale, checks bypassed as noise, eval DB becomes a form. Mitigations: owners named (registry: pack maintainer; learning promotion: operator; drift check: runs in both repos' suites), seeded-failure self-tests, report-only adoption wave, Hermes weekly telemetry watches the watchers, and P4 intake applies to campaign failures too.

## Operator-decision register (explicit, not silent)

1. **Full security lane: OUT of campaign scope** (minimal secret-scan eval ships in R16a; a real security lane — threat-model, security-review integration — is a named follow-on for the operator to schedule).
2. R8 archive decisions: operator approves at Wave-2 acceptance.
3. Learning-promotion cadence: operator-facing, per-wave now, monthly after.
4. Coordination-artifact commit policy: campaign folder commits + pushes with waves (already in effect; contains no secrets by sanitization rule).

## Round-2 focus (for reviewers)

The 19 judgment changes above are claimed implemented in this document. Round 2 verifies: (a) each change is genuinely resolved, not renamed; (b) no new major issues introduced (especially: the Wave-2 entry block ordering, the R9b live gate, the conditional word target, P4-completeness); (c) the 20-case catalog mapping (final verdicts in `failure-catalog.md`) is correct; (d) the plan is implementable by Codex as specified with the resolved inputs (fingerprint registry, answer key, schema, install policy, cutover protocol, access assumptions).

## Round-2 amendments (plan v3.1 — binding; see round2-judgment.md for provenance)

Both round-2 reviews: MINOR_CHANGES_ONLY → implementation approved. Amendments A–L bind over the text above where they conflict:

A. Acceptance validator gains terminal-status mode (`accepted|rejected|blocked_with_failure_intake`); truthful failure reports MUST validate; fixtures both ways (Wave 1).
B. `references/drift-fingerprints.toml` schema: `id, owner, adoption_state, canonical_source, target_paths, match, normalization, allowed_absences, severity, blocking_wave` (Wave 1).
C. Catalog cases carry `plan_items/eval_type/status`; case 16's canary-mandate sentence in the INITIAL registry; case 17 eval → R3/R13; case 18 → child plan; case 20 standing via uberplan contract rule + R13 fixture.
D. Every new receipt/plan field gets a validator function + negative fixture as it lands (tier justification, reproduced-red, interface-shape, cost, intake).
E. ubergoal's condensed tier table fingerprinted IN FULL against the spine ladder.
F. Wave-2 entry rule scoped: applies to dedup/retire/unify deletions of rules surviving elsewhere; same-commit replacements + dead-content removals w/ P1 receipts exempt. R6 ubergoal content list gains "micro-intent fast path".
G. Tier-1 micro-intent artifact carries the intake field (validator named in R10/R11); Tier-0 = typo/cosmetic only, `tier0:` commit trailer, Hermes samples weekly.
H. Test-channel canonical = `#gaia-testing-alpha`, posture = posting pre-approved for test proofs (workspace CLAUDE.md sentence wins; GAIA_TESTING.md edited as owner). OPERATOR VETO POINT — logged in decision register as #5.
I. If Hermes/R15 is blocked, orchestrator publishes the first outcome comparison manually from R13c receipts.
J. Standing rule in pack AGENTS.md: new standalone CLIs only where fixtures prove separate need; default = aggregator module.
K. Wave 1 = 4 implementation dispatches.
L. Catalog case 21 (subprocess-dies-without-terminal-state, from this round's own failed Codex run): dispatch wrapper checks exit code + expected output; retry-once-then-ledger (R12).
