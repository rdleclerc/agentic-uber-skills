# Wave 2 — Dispatch 5: gaia doctrine bundle (R3a re-stub, R3c unifications, R5-gaia dedup, R9a slim)

You are Codex, implementer, in a clean WORKTREE of agfunder-gaia on `main`. NO git commands. Tier 2 (cross-repo doctrine). P1 receipts for every deletion. Touchable files ONLY: `AGENTIC_ARCHITECTURE.md`, `CLAUDE.md`, `AGENTS.md`, `INIT.md`, `GAIA_TESTING.md`, `knowledge/coding-agent-operating-spine.md` (pointer touch-ups only), `skills/gaia-testing/SKILL.md`, plus a new receipt file. The E6 session works elsewhere in this repo — do not touch anything else. IMPORTANT: runtime-persona content in CLAUDE.md (Slack etiquette, heartbeats, group-chat rules, live-lane inventory, "What Is Live") is R9b's business and MUST NOT move or change in this dispatch — a live-Slack-proof gate protects it.

Read first: all touchable files; the drift registry at `${UBER_SKILLS_ROOT:-~/repos/agentic-uber-skills}/references/drift-fingerprints.toml` (the canonical strings you must land); plan-v3.md R3/R5/R9a + amendment H in the same campaign folder.

## 1. R3a — re-stub AGENTIC_ARCHITECTURE.md

First grep the repo (scripts/, lib/, plugins/, tests/, knowledge/, skills/) for consumers of `AGENTIC_ARCHITECTURE.md` and report them. Then replace the 11.6k-line drifted copy with a ≤25-line stub: states the canonical home (`${UBER_GUIDE_ROOT:-~/repos/agentic-architecture-guide}/agentic_architecture_singlefile.md`), clone instructions if absent, the rule that edits happen ONLY in the canonical repo, and preserves the startup-canary contract — the stub explicitly says: read the canonical singlefile, then emit `Architecture guide loaded: AGENTIC_ARCHITECTURE.md`. If any consumer you found asserts on file SIZE or specific content (not just existence), FLAG it and leave the file untouched pending orchestrator decision.

## 2. R3c — unifications (amendment H executed)

- Canonical test-channel sentence: `#gaia-testing-alpha` with the pre-approved-posting posture (the exact sentence currently in CLAUDE.md, fingerprinted in the registry). GAIA_TESTING.md becomes the OWNER: carry the sentence verbatim there (replacing its `#gaia-test-alpha` read-only-default text at ~lines 151 and 443); `skills/gaia-testing/SKILL.md` replaces its user-approval requirement with the same sentence or a one-line pointer to GAIA_TESTING.md; AGENTS.md gets sentence-or-pointer; CLAUDE.md KEEPS its copy for now (it is inside persona-adjacent testing text — if its copy is in the coding-process half, replace with a pointer; if entangled with persona content, leave and note).
- Canary command: unify every spelling in GAIA_TESTING.md and CLAUDE.md to the repo-root form `/Users/rob/repos/agfunder-gaia/scripts/run_gateway_health_canary.sh` (kill the `~/.openclaw/workspace/...` symlink spellings — they violate the repo's own worktree rule).

## 3. R5-gaia — one home per rule (dedup restatements)

For each rule below: the named owner keeps the full statement; every other listed surface gets a ONE-LINE pointer (file + section). Delete the duplicate prose (receipt row each):
- Review-lane/ladder rule → spine owns (done in W2-D1). Remove remaining full restatements in CLAUDE.md and INIT.md if present (pointer: spine §Review ladder).
- Test triggers / mandatory suites → GAIA_TESTING.md owns. CLAUDE.md's "Testing Doctrine" restatement + INIT.md's + gaia-testing SKILL.md's overlapping trigger lists → pointers (SKILL.md may keep its 3-command quickstart).
- Live-Slack-proof gate → GAIA_TESTING.md owns it now (same move as the channel sentence). CLAUDE.md + AGENTS.md restatements → pointer lines (CLAUDE.md persona-half caveat applies).
- Coordination roles / integrator-contributor → AGENT_COORDINATION.md owns (do not edit it); CLAUDE.md's 17-bullet restatement → 2-3 lines + pointer.
- Memory-split rule (PG=truth/Qdrant=retrieval/wiki=synthesis/QMD=recall) → CLAUDE.md owns (keep ONE compact statement in its architecture section); INIT.md + GAIA_TESTING.md restatements → pointers.
- Affordance-before-harness Required Proof block (~450 words, near-verbatim in CLAUDE.md and AGENTS.md) → canonical lives in the guide repo (docs/00-agentic-change-protocol.md); BOTH gaia copies become a 3-line summary + pointer. FLAG if the guide path cannot be verified from this worktree.

## 4. R9a — slim the coding-process half of CLAUDE.md + INIT.md as sole unconditional read

- CLAUDE.md coding-process content (everything that is NOT runtime persona): reduce to routing + pointers per the dedups above; target: the coding-process half ≤ ~150 lines. Persona half untouched.
- INIT.md becomes the single unconditional cold-start read: tighten to orientation + routing (repo root rule, worktree rule, where each doctrine lives with one-line size/trigger annotations: "read X (N lines) when Y"). Every remaining "read before X" mandate in CLAUDE.md/AGENTS.md gains its size + trigger annotation or becomes conditional.
- Line-count report: CLAUDE.md before/after (total + coding-process-half estimate), INIT.md before/after, GAIA_TESTING.md delta.

## 5. Receipt + verification

- Receipt: `coordination/process-rearchitecture-202607-gaia-w2d5-receipt.md` (in THIS repo): deletion table (block | words | new home | verified) + consumer-grep results for R3a + the fingerprinted sentences' final locations.
- Run: `node --test tests/integration/failure_evals.test.mjs` (must stay green); `python3 scripts/check_coding_agent_spine.py --json` if present; grep-verify each registry fingerprint's canonical string exists at its new owner file. Print everything. FLAG all uncertainties — especially anything where persona vs coding-process classification was ambiguous (leave ambiguous content UNMOVED and flagged).
