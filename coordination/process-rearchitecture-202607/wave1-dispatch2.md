# Wave 1 — Dispatch 2 of 4: R3 (drift check + fingerprint registry) + R4 (install-sync)

You are Codex, implementer for the process-rearchitecture campaign. Authority: `plan-v3.md` R3 (tool build only) + R4, amendments B, E (planned entry), H, J, and catalog case 16, all in this folder. Work ONLY inside this repo. Do NOT run git commands. Do NOT edit any file outside this repo — the drift checker READS cross-repo files but this dispatch changes nothing in agfunder-gaia or the guide repo. Slice 1 already landed: the portability oracle exists in `scripts/lint_pack_contract.py`; your new modules must pass it (no machine-specific literal paths — use `${VAR:-~/tilde}` parameterization in the registry).

## R3 — drift-check module + registry

1. New module `check_doctrine_drift` inside `scripts/lint_pack_contract.py` (amendment J: aggregator module; also add a thin `scripts/check_doctrine_drift.py` shim ONLY if the aggregator cannot take a subcommand cleanly — prefer `lint_pack_contract.py --drift [--strict]`).
2. New file `references/drift-fingerprints.toml`. Per-entry schema (amendment B, all fields required): `id, owner, adoption_state (report_only|blocking|planned), canonical_source (file+anchor), target_paths (list; parameterized like "${GAIA_ROOT:-~/repos/agfunder-gaia}/GAIA_TESTING.md"), match (literal|regex), pattern (the string/regex), normalization (none|whitespace), allowed_absences (list of target paths where absence is OK until blocking_wave), severity (error|warn), blocking_wave (int)`.
3. Initial entries (get exact current strings by reading the named files read-only):
   - `test-channel-posture` — canonical: `#gaia-testing-alpha` + the workspace CLAUDE.md pre-approved-posting posture sentence (amendment H); targets: `${GAIA_ROOT}/GAIA_TESTING.md`, `${GAIA_ROOT}/CLAUDE.md`, `${GAIA_ROOT}/AGENTS.md`, `${GAIA_ROOT}/skills/gaia-testing/SKILL.md`. adoption_state=report_only (gaia surfaces are KNOWN-divergent until Wave 2c — the report documents it), blocking_wave=2.
   - `canary-command` — canonical spelling `${GAIA_ROOT}/scripts/run_gateway_health_canary.sh` (repo-root form); targets: GAIA_TESTING.md, workspace CLAUDE.md, `${HOME}/CLAUDE.md`. report_only, blocking_wave=2.
   - `lane-policy-portable` — the exact AGENTS.md sentence now in this repo ("Review and acceptance lanes use the highest-capability available Claude lane; record `lane_used` in the receipt; never silently downgrade. In gaia contexts the spine's lane policy governs (`knowledge/coding-agent-operating-spine.md` in the gaia workspace repo).")— targets: AGENTS.md (+README.md first sentence half). blocking NOW (it exists and must not drift), blocking_wave=1.
   - `post-upgrade-canary-mandate` (case 16) — the GAIA_TESTING.md sentence mandating surface canary + integration suite after `openclaw upgrade`; target: `${GAIA_ROOT}/GAIA_TESTING.md`. report_only, blocking_wave=2.
   - `guide-version-line` — `Version: 1.5` line must match between `${GAIA_ROOT}/AGENTIC_ARCHITECTURE.md` and `${UBER_GUIDE_ROOT:-~/repos/agentic-architecture-guide}/agentic_architecture_singlefile.md` until R3a stubs the copy. report_only, blocking_wave=2.
   - `precedence-sentence` and `tier-ladder-table` — adoption_state=planned, empty pattern with a `pending: Wave 2 R7/R6` note field, allowed_absences=all targets, blocking_wave=2 (amendment E: the ubergoal condensed tier table will be fingerprinted IN FULL against the spine ladder when both exist).
4. Behavior: default run = report-only (always exit 0, print per-entry status: MATCH / DIVERGED(details) / ABSENT(allowed|not)); `--strict` = exit nonzero on any blocking-entry divergence. The aggregator's default invocation (as called by tests) runs drift in report-only and must NOT fail the suite on gaia-side divergence.
5. Tests: seeded-divergence self-test — fixture registry + fixture target files where one target diverges; assert the module reports it and `--strict` fails; assert report-only exits 0. Also: registry schema validation (missing field = error) with an invalid fixture.

## R4 — install-sync module

1. Module `check_skill_install_sync` in the aggregator (`--install-sync` flag or part of default report).
2. Checks: every skill dir in this repo has a symlink at `~/.claude/skills/<skill>` and `~/.codex/skills/<skill>` pointing at the repo dir (resolve realpath; symlink REQUIRED — a copy is a violation). Extra entries in those roots are OK if on the ignore list: `chronicle, harmonic, codex-primary-runtime, gaia-session-lane, build-agent-eval, design-agent-memory, design-context-engine, design-source-lane, openclaw-agentic-skill-creator, openclaw-agentic-tool-designer, review-agentic-architecture` (+ anything under a `plugins`/dot prefix); unknown extras = report-only warn. Missing/copy/wrong-target = violation. Roots overridable via env for tests.
3. Default report-only; `--strict` available; blocking_wave=2 noted in module docstring.
4. Tests: seeded-desync with temp roots (missing skill, copy-instead-of-symlink, wrong target, allowed extra, unknown extra); current real install must pass (assert in a test that tolerates CI absence of the roots by skipping when roots don't exist).

## Wrap-up

Run: pack lint (including your new modules), full `python3 -m pytest tests/ -q`, and print the drift report's CURRENT real output (the gaia divergences it finds today — that report is campaign evidence). Print a summary: files changed, registry entries with adoption states, test counts. FLAG any spec contradiction prominently instead of resolving it silently.
