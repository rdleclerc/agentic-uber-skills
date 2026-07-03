# Gaia child plan — R14 liveness doctrine + R15 Hermes revival (Tier 3)

Child of plan-v3.1 (judgment #12). Tier 3: touches launchd services + the live oversight lane. NO service is modified without: this plan, the access assumptions verified, a rollback pair prepared, and per-change live proof. Operator sees this plan before implementation dispatches run (surfaced in the Wave-3 status of 2026-07-03).

## Objective

Every scheduled/unattended gaia lane exposes TTL-bound proof of life with a loud freshness canary and a human-owned-blocker classification; the Hermes weekly overseer is repaired, self-monitoring, and extended with process telemetry so the estate's subtraction stays honest without anyone remembering to check.

## Access assumptions (verify before dispatch; FLAG any miss)

- launchd user domain `gui/$(id -u)` reachable via `launchctl print/bootstrap/bootout` (local machine, operator logged in).
- `~/.hermes/` install intact (binary `~/.local/bin/hermes`, config `~/.hermes/config.yaml`, provider = local gateway `127.0.0.1:9999/openai/v1`).
- Provider gateway live (`curl -sS 127.0.0.1:18789/health` + gateway 9999).
- Secrets via cache-first + kill-timer pattern ONLY (op hangs under launchd — catalog case op-hang-under-launchd; worked example `scripts/run_gmail_pubsub_bridge.sh`).
- gaia repo main writable via worktree; the OTHER SESSIONS' checkout is never touched.
- Email send path: guarded `send-email` helper (hard-blocks non-@agfunder.com); OVERSEER_DRY_RUN=1 exists for non-sending proofs.

## R14 — liveness doctrine + lane inventory

1. **Canonical statement** (GAIA_TESTING.md owns; spine + CLAUDE.md point): every scheduled/unattended lane ships (a) a TTL-bound proof-of-life artifact (state file/DB row with `last_success_at` + expected cadence), (b) a freshness canary that FAILS LOUDLY past threshold, (c) a durable human-owned-blocker classification — credential/config drift alerts ONCE with the exact human action and stops auto-repair. New-lane checklist added to GAIA_TESTING mandatory triggers.
2. **Lane inventory** (receipted table): every launchd `ai.agfunder.*`/`ai.openclaw.*` plist + every `~/.openclaw/cron/jobs.json` job → lane name, owner doc, proof-of-life artifact (exists? fresh?), canary (exists?), docs-vs-reality check (docs claiming "live" must cite a liveness artifact — case 2). Known intake already: Hermes dead since 05-04; formal live-proof ledger stale 761h; eval cadence stale 402h + sparse (probe receipt side-findings); gmail-push freshness check EXISTS (07-01) = the pattern to generalize.
3. **Top-gap fixes only** (this campaign): Hermes (R15), + wire the run-twice idempotency helper + op-hang entrypoint grep into GAIA_TESTING triggers (cases 13/14 → eval_built). Other gaps land as classified followups in knowledge/agent-followups.md, NOT silent scope growth.

## R15 — Hermes revival + process telemetry

1. **Diagnose exit 78** (EX_CONFIG): read `~/.openclaw/logs/hermes-overseer.launchd.err` + `launchctl print gui/$(id -u)/ai.agfunder.gaia-hermes-overseer`. Prime suspects: op:// resolution under launchd (case 13 pattern — the orchestrator sources secrets at top), stale paths after the guide-repo move, or PyYAML/venv drift. Fix = smallest change + the cache-first/kill-timer pattern where secrets are fetched.
2. **Proof of life on the watcher itself**: run writes `state/hermes-overseer-heartbeat.json` (start, end, outcome, report path); a freshness check (runtime-health integration or standalone canary) fails loudly if >8 days old (weekly cadence + 1-day grace). Case 2 → eval_built.
3. **Process telemetry sections** in the weekly bundle (new `compile_overseer_process.py` or extension): (a) skill-invocation counts (existing heuristic compiler), (b) uber-run cost receipts (tokens/minutes/lane_used from coordination receipts; deterministic cross-check vs transcript sizes — measurement spine comparison vs baseline-cost.md), (c) drift-check + install-sync output (run in report-only, include verbatim), (d) failure-DB delta (cases added/status changes/aging seeds), (e) learning backlog (learning/inbox count + age; per-skill word-budget deltas per the net-negative rule).
4. **Proof**: ONE live scheduled-run-equivalent execution end-to-end (launchd `kickstart`), OVERSEER_DRY_RUN=1 first, then one real send (email lands) with operator visibility; heartbeat artifact + report + all 5 sections present. The FIRST outcome comparison vs baseline-cost.md publishes in that report (campaign DoD).

## Rollback

Every plist/script change = versioned pair (`<name>.plist.bak-<date>`, script via git); restore = `launchctl bootout` + previous file + `bootstrap`. Hermes changes are git-tracked in gaia repo scripts/; config.yaml backed up alongside. No change to the OpenClaw vendor runtime.

## Fallback (if access blocked)

Land docs/contracts/canaries as far as testable; mark the lane item `hard_blocked_after_safe_action_exhaustion` ONLY after the safe-action list is exhausted; otherwise `active_blocked` with the exact human action (per operational-states.md). No silent deferral.

## Execution shape

2 dispatches: D-A (R14: doctrine + inventory + trigger wiring — gaia worktree, doc/script-level, Tier 2 edits inside a Tier-3 child) then D-B (R15: Hermes repair + telemetry + live proof — Tier 3, live services; orchestrator runs the launchd/live steps itself, Codex writes the compilers/scripts). Wave-3 acceptance lane reviews the whole wave including this child; receipt carries the production blocker gate FULLY (first campaign use of its production mode).
