# Plan v2 — Process Rearchitecture (R1–R16)

Status: DRAFT for adversarial review round 1. Companion docs: `scope.md` (operator instructions + approvals), `failure-catalog.md` (14 seed cases = reviewer test set).

## Objective

Rearchitect the coding-process estate — `agentic-uber-skills` (10 skills), `agentic-architecture-guide/skills` (7 skills), gaia doctrine surfaces (workspace CLAUDE.md / AGENTS.md / INIT.md / GAIA_TESTING.md / spine), and home CLAUDE.md — so that:

1. **Rigor invariants are preserved** (scope fidelity, adversarial acceptance, class-level RCA, live-proof-before-done) — these demonstrably caught real failures.
2. **Cost becomes risk-proportional** (small tasks stop paying the ~28–33k-token, 4×opus-max-review toll).
3. **Every rule has exactly one home** (duplication is the proven drift mechanism — catalog case 9).
4. **Failures become evals automatically** (operator mandate: "every failure is an opportunity… enshrine that to be automatic").
5. **Nothing unattended can die silently again** (catalog cases 1, 2, 12).

### Definition of Done (campaign)

- All 16 items landed or explicitly re-scoped with operator approval; per-item DoD below met with receipts in this folder.
- Pack contract tests, per-skill tests, `quick_validate.py` green; new drift-check + install-sync + path-lint green across all surfaces.
- Wave 2 net SKILL.md word count strictly below baseline (baseline: 19,176 words across 10 uber skills; target ≤ 12,000) with behavior preserved per contract tests + fresh-agent smoke evals.
- Failure-eval DB live in both layers with ≥14 seed cases, validator-enforced intake rule, and ≥1 executable eval per Wave-1-buildable case.
- Every wave committed + pushed; every campaign-internal failure appended to the DB (dogfood proof).

## Baseline evidence (from the 2026-07-02 audit)

- Estate: 19,176 SKILL.md words (uber pack) / ~44,600 with templates+references; 47–55 mandated steps for a substantial gaia change; 4 opus-max reviews at 10–30 min each; ~28–33k tokens of process prose loaded on a typical ubergoal route.
- 10 contradictions across doctrine (worst: model pins vs "best available"; mandatory vs forbidden cross-model review; two routers, two acceptance authorities, no precedence; 2 diverged copies of the "required" 11.6k-line guide, both "Version 1.5").
- Duplication: adversary block ×5, blocked-state machine ×4, affordance-proof ×3, review-lane rule ×5, test-trigger rule ×4 (3 duplicated rules already drifted).
- Instrument saturation: evaluator scores 100/100 on everything; learning loop additive-only (`learning/processed/` empty since creation); 3 skills with ~zero usage in 7 weeks.
- Two weeks of work: gates used heavily WITH teeth (147 adversarial-review artifacts, 0 reverts); dominant failures were silent-lane deaths and automation grinding on human-owned blockers — not process-skip failures.

## Design principles (reviewers: challenge these first — everything downstream leans on them)

- P1. Subtraction with instrumentation: never delete a scar without moving its invariant to a named home (reference, eval case, or gate) — deletion receipts map old text → new home.
- P2. One canonical home per rule; every other surface gets a one-line pointer; a mechanical drift check replaces the manual "propagate everywhere" duty.
- P3. Risk-priced gates: gate cost scales with tier; a gate that always passes (or always runs at max) is miscalibrated by definition.
- P4. Failure→eval is a standing pipe, not a habit: intake enforced by validators at the two chokepoints every failure already passes through (uberrca, uberaccept surprises).
- P5. Liveness is a property of lanes, not of code: anything scheduled/unattended exposes TTL-bound proof of life.

## Items

### Wave 1 — mechanical (no design judgment; ~1 session)

- **R1. Unpin models.** Remove `model: claude-opus-4-8` / `effort: max` from all 10 uber SKILL.md frontmatters; delete the AGENTS.md clause enforcing the pin; replace with policy prose: "review/acceptance lanes use the highest-capability available Claude lane; record the lane used in the receipt; never silently downgrade." DoD: zero hardcoded model ids in pack frontmatter; policy stated once (in pack AGENTS.md); receipts template gains a `lane_used` field.
- **R2. Fix portability rot.** Parameterize/correct all 12 `/Users/claw1/` references (env var `UBER_GUIDE_ROOT` or repo-relative discovery with documented fallback); point ubergoal's work-contract references at the real guide path; delete Type0-specific spine paragraphs from uberplan/uberaccept; remove dead storage paths (`~/.agentic-uber-learnings/`, ubershow's claw1 runtime dir) in favor of the actual convention (task coordination folders). DoD: path-lint (new, part of R16 tooling) green: every absolute path in skill text exists or is parameterized.
- **R3. Kill version-skew hotspots.** (a) Re-stub `agfunder-gaia/AGENTIC_ARCHITECTURE.md` → pointer at `~/repos/agentic-architecture-guide/agentic_architecture_singlefile.md` (canonical), preserving the startup-canary line contract; (b) fix home CLAUDE.md stale model-lane section (pre-06-30 policy); (c) unify test-channel name + approval posture and canary-command spelling across GAIA_TESTING.md / workspace CLAUDE.md / AGENTS.md / gaia-testing SKILL.md; (d) ship `scripts/check_doctrine_drift.py` — greps configurable fingerprints (channel, canary command, lane policy, review-gate wording, guide version) across all doctrine surfaces, exits nonzero on divergence. DoD: drift check green; runs in pack tests and is invocable from gaia repo.
- **R4. Install-sync check.** `scripts/check_skill_install_sync.py`: repo skill dirs ↔ `~/.claude/skills` ↔ `~/.codex/skills` (symlink targets or content hash); reports missing/extra/diverged. Wired into pack tests + documented in install flow. DoD: catches a seeded desync in test; current install passes.
- **R16a. Failure-eval DB scaffold + seed.** Two-layer per approval: `agentic-uber-skills/evals/failures/` (portable/process) + `agfunder-gaia/evals/failures/` (runtime), shared case schema (YAML frontmatter + md body), cross-index file in each, `scripts/validate_failure_case.py`, and the 14 seed cases from `failure-catalog.md` split by layer. Executable evals built now for the mechanically checkable cases (7 path-lint, 8 install-sync, 9 drift, 14 run-twice-idempotency harness pattern doc); checklist-evals for the rest. DoD: validator green on all seeds; both indexes list all cases with layer + status.

### Wave 2 — subtraction (the core refactor; net word count must go DOWN)

- **R5. One home per rule (pack-internal + cross-repo).** Adversary block: 5 inlined copies → each skill keeps its ≤3 unique questions + 1 Trigger/Do pointer line to `references/claude-adversary.md` (verify both runtimes read references on demand — see risk V3). Blocked-state machine 4→1 (new `references/operational-states.md`); Task Understanding Review 2→1 (uberplan owns it; ubergoal points); thread-cap policy 2→1; Gall's-Law/Basic-Spine 4→1. Cross-repo: affordance-proof block 3→1 (guide owns; gaia docs point), opus-lane rule 5→1 (spine owns), test-trigger rule 4→1 (GAIA_TESTING owns), coordination-roles 4→1 (AGENT_COORDINATION owns), memory-split rule 4→1 (workspace CLAUDE.md owns). Every deduped rule's fingerprint goes into the R3 drift check so pointer rot is caught mechanically. DoD: deletion receipt mapping every removed block → canonical home; drift check extended; pack + gaia doc tests green.
- **R6. Thin ubergoal + tiered plan templates.** ubergoal → ~600–800 words: routing table, tier table, scope-artifact gate, completion rule, pointers. uberplan gains `templates/plan-tier1.md` (~10 sections: objective, scope-fidelity, acceptance criteria, proof plan, risks, out-of-scope, verification commands, rollback, receipts, open questions); the 54-section contract becomes `plan-tier3.md`, explicitly reserved. DoD: word counts (ubergoal ≤800); fresh-agent smoke: 5 canned prompts (tiny fix / medium feature / risky runtime change / research ask / loop ask) route to correct tier + template.
- **R7. Risk-tiered review ladder + precedence.** One written ladder, stated once (spine owns; pack points): Tier 0 none / Tier 1 one review pass (any capable lane, exact-diff) / Tier 2 exact-diff + adversarial (independent lane) / Tier 3 full 4-phase opus-family ladder + review-board lanes. Precedence paragraph (new, in gaia AGENTS.md + pack AGENTS.md, identical fingerprint): ubergoal wraps the spine lifecycle for gaia work; the uber run receipt satisfies the spine receipt contract; uberaccept IS the acceptance review; claude-adversary is the required Tier-2+ independent lane and stays opt-in below Tier 2. Non-negotiable preserved: no implementing agent self-approves at any tier ≥1 (catalog case 5). DoD: contradiction pairs B1/B3/B10 + two-router B2 (from the 07-02 audit) each resolve to a single unambiguous instruction; drift-check fingerprints added.
- **R8. Retire-or-prove + compress.** ubersimplify + uberarchitect + ubershow: run their ROADMAP retirement evaluations now — each either shows a real usage plan (owner + trigger + eval) or folds its checklist into uberplan/uberaccept as a section/reference and the skill is archived (kept in git, removed from install). openclaw-agentic-skill-creator 5,034 → ≤1,500 words (strip forked banter, stacked preamble, duplicate loop recap, disowned scripts) while keeping the eval-driven methodology sections uber-skill-creator lacks. uberskillevolver's 4 fossilized incident sections → failure-eval cases + one reference. DoD: decisions receipted per skill; word deltas recorded; pack tests green.
- **R9. Slim the cold-start.** Workspace CLAUDE.md (782 lines): runtime-persona content (Slack etiquette, heartbeats, group-chat rules, live-lane inventory) moves to gaia runtime skills/lane docs; coding-agent process content stays ≤~250 lines of routing + pointers; INIT.md becomes the single unconditional read; every remaining "read before X" mandate annotated with size + trigger condition. Home CLAUDE.md gets the same pointer treatment (already partially true). DoD: line counts; a fresh-session orientation smoke test (agent given only INIT.md finds spine, testing doctrine, and review ladder in ≤3 hops); no doctrine deleted without a pointer home (P1).

### Wave 3 — capability (new powers; each item independently shippable)

- **R10. Fast path (`ubertask`).** New ~300-word skill (or ubergoal section — decide by R6 outcome; default: section, not new skill, to avoid estate growth): micro-intent artifact = scope sentence + checkable acceptance criteria + verify command + out-of-scope note, one file, no ledger/receipt; hard de-escalation rule (Tier 0/1 defaults here unless named risk triggers escalation); explicit non-goals (never for runtime/provider/security/data-subject surfaces). DoD: de-escalation eval — the 5 R6 smoke prompts + 5 new small-task prompts; small tasks produce exactly one artifact; risky prompts still escalate.
- **R11. Debug/verify loop.** New skill `uberdebug` (name TBD): reproduce → hypothesize → bisect → fix → verify loop for everyday defects; composes with Claude Code's `verify`/`run`/`code-review`; hard rules from catalog: fix ships only with reproduced-red on the real failure path (case 4), repeated same-class failure escalates to uberrca with a class-invariant statement (case 3). DoD: skill ≤600 words; 2 catalog cases (3, 4) have executable/checklist evals bound to it; uberrca boundary stated in both skills once each.
- **R12. Parallel-session + dispatch contract.** Promote the dispatch-ops doctrine from memory notes into `references/dispatch-and-sessions.md` (single home): direct `codex exec`, duplicate cull, checkpoint-commit before dispatch, orchestrator owns git+DB, disjoint write scopes, live-verify sandbox-blind claims (case 10), session claim/handoff rules for ~10 parallel operator sessions (branch/worktree claims, coordination-folder locks). ubergoal/uberplan point to it. DoD: single home; catalog cases 10, 11 get evals; drift fingerprint added.
- **R13. Replace the saturated evaluator.** Demote `evaluate_skill_quality.py` to lint (rename `lint_skill_shape.py`, keep in tests, stop reporting scores as quality). New instrument: (a) fresh-agent behavioral evals — routing/tier/de-escalation prompts run via subagent with transcript-graded outcomes (methodology already in openclaw-agentic-skill-creator; port the harness, not the prose); (b) known-bad fixtures that MUST fail (catalog case 6's eval); (c) cost accounting — run receipt gains tokens/minutes/lane fields so "benefit >> cost" is computed per run; (d) net-negative learning rule in uberskillevolver: any promoted lesson adding words names the words removed. DoD: known-bad fixture fails; ≥8 behavioral eval prompts checked in with expected routings; receipt template + validator updated.
- **R14. Liveness doctrine.** One canonical statement (GAIA_TESTING.md owns, spine points): every scheduled/unattended lane ships (a) TTL-bound proof-of-life artifact, (b) freshness canary that fails loudly past threshold, (c) human-owned-blocker classification — credential/config drift alerts ONCE with the exact human action and stops auto-repair (cases 1, 2, 12). Applies to: launchd jobs, openclaw cron, watch bridges, the health-RCA loop itself. Implementation in gaia repo: inventory of existing lanes + liveness gap table + fixes for the top gaps (Hermes handled in R15; gmail freshness already shipped 07-01 — generalize its pattern). DoD: lane inventory receipted; each lane has liveness status; new-lane checklist added to GAIA_TESTING mandatory triggers; drift fingerprint.
- **R15. Revive Hermes as the estate's grader.** Fix the launchd exit-78 (diagnose: likely env/config — EX_CONFIG; apply op-hangs-under-launchd pattern, case 13); add its own proof-of-life per R14; extend the weekly bundle with process telemetry: skill-invocation counts, tokens/minutes per uber run (from R13 receipts), drift-check + install-sync output, failure-eval DB delta (cases added/aged), learning-inbox backlog. Weekly report = the automatic outside critic that keeps subtraction honest. DoD: one live scheduled run producing a report + proof-of-life artifact; report includes all 5 telemetry sections; failure case 2 gets its executable eval (liveness probe on the overseer itself).

## Dependencies / ordering

- R16a before R5/R8 (deletion receipts reference eval-case homes).
- R3 drift check before R5 (dedup adds fingerprints to it).
- R6 before R10 (fast path lands in whatever ubergoal becomes).
- R13 receipts before R15 telemetry (Hermes reads them).
- R14 before R15 (Hermes gets the liveness contract it enforces).
- Gaia-repo edits (R3b/c, R9, R14) follow GAIA_TESTING mandatory triggers + spine review gates; they are Tier 2 under the new ladder (doctrine surfaces, no runtime code) except R14 lane fixes (Tier 3 if they touch runtime services).

## Failure-catalog mapping (reviewers: attack completeness)

Case→items: 1→R14,R16 · 2→R14,R15,R3 · 3→R11,R16 · 4→R11,R16 · 5→R7(preserve),R16 · 6→R13 · 7→R2,R16 · 8→R4 · 9→R3,R5 · 10→R12,R16 · 11→R12 · 12→R14,R16 · 13→R16(+R15 applies pattern) · 14→R16. Every case maps to ≥1 item; reviewers verify each mapping would actually have prevented or materially shortened the failure.

## Premortem (V0) — known risks, reviewer challenges welcome

- V1. **Live-doctrine edits under ~10 concurrent sessions**: a session cold-starting mid-refactor reads half-moved doctrine. Mitigation: wave-atomic commits; R9/R5 land file-complete (old text deleted + pointer added in the same commit); push per wave so other machines converge.
- V2. **Deleting scar tissue loses a lesson**: some "bloat" paragraphs encode real incidents. Mitigation: P1 deletion receipts (every removed block → named home); adversaries specifically check the receipt for lost invariants.
- V3. **"References load on demand" assumption wrong for Codex**: the 5-way inlining was justified by "references may not auto-load." Verified false for Claude Code; MUST be verified for Codex CLI before R5 deletes the copies (cheap probe: codex exec run that requires reference content; if Codex doesn't follow references, keep a 2-line essential-summary in each skill per the existing convention). This probe is a Wave-2 entry gate.
- V4. **Thinning ubergoal breaks routing**: fresh agents may under-escalate. Mitigation: R6/R10 smoke evals with expected routings; R13 known-bad fixtures.
- V5. **Hermes revival scope creep into runtime work**: R15 is repair + telemetry, not redesign. Out-of-scope: new compilers beyond the listed telemetry sections.
- V6. **Retiring skills someone quietly uses**: usage evidence is from coordination artifacts only. Mitigation: archive (uninstall, keep in git, one-line tombstone in README), not delete; restore is a symlink.
- V7. **Word-count target becomes its own Goodhart**: ≤12,000 is a budget, not a score; contract tests + behavioral evals are the quality floor; nothing gets deleted purely to hit the number (P1 receipts prove it).
- V8. **Cross-repo atomicity**: pack and gaia repos can't commit atomically together. Mitigation: pointers land after their canonical home exists (order within waves); drift check runs across both repos and gates the wave.

## Open design questions for reviewers

- Q1. R10 fast path: separate skill vs ubergoal section? (Default: section — avoid estate growth; challenge if a separate trigger surface is genuinely better for de-escalation.)
- Q2. R7 ladder: is Tier-1 "one review pass on any capable lane" too weak for gaia-repo doctrine edits, given every doc edit propagates to ~10 sessions? (Default: doctrine-surface edits are Tier 2 minimum.)
- Q3. R16 intake chokepoints: are uberrca + uberaccept-surprises sufficient, or does the Slack/health alert-RCA loop need its own automatic intake into the runtime layer? (Default: yes, add it in the gaia layer — but implemented as part of R14's lane inventory, not a new lane.)
- Q4. R13 cost accounting: receipts self-reported by agents vs measured externally (wrapper timing + token logs)? (Default: self-reported now, external measurement noted as follow-on — challenge if self-reporting is too gameable to bother.)
