Implemented the R14 slice in the child worktree with no git commands and no live service changes.

Changed files:
- [GAIA_TESTING.md](/Users/rob/repos/worktrees/gaia-childA/GAIA_TESTING.md)
- [knowledge/gaia-scheduler-ownership.md](/Users/rob/repos/worktrees/gaia-childA/knowledge/gaia-scheduler-ownership.md)
- [coordination/process-rearchitecture-202607-lane-inventory.md](/Users/rob/repos/worktrees/gaia-childA/coordination/process-rearchitecture-202607-lane-inventory.md)
- [scripts/check_lane_liveness.py](/Users/rob/repos/worktrees/gaia-childA/scripts/check_lane_liveness.py)
- [op-hang-under-launchd.md](/Users/rob/repos/worktrees/gaia-childA/evals/failures/cases/op-hang-under-launchd.md)
- [pg-null-upsert-dup.md](/Users/rob/repos/worktrees/gaia-childA/evals/failures/cases/pg-null-upsert-dup.md)
- [INDEX.md](/Users/rob/repos/worktrees/gaia-childA/evals/failures/INDEX.md)

Verification:
- `node --test tests/integration/failure_evals.test.mjs`: pass, 2 tests.
- `python3 scripts/check_lane_liveness.py --report-only`: ran; 7 PASS, `hermes-overseer` MISSING as expected.
- `python3 -m py_compile scripts/check_lane_liveness.py`: pass; generated pyc removed.
- Failure case validator over cases: pass.
- Failure case validator `--index`: fails on an existing schema mismatch. The pack validator expects local canonical paths like `evals/failures/cases/<id>.md` and no `date:` segment; the repo’s Node test expects runtime rows to include `canonical: agfunder-gaia/evals/failures/`. I left the repo-tested INDEX format intact.

Claude review gate: unavailable. Local `claude` is logged out, and `type0` / `agclaw` SSH hostnames do not resolve, so this is locally verified only.

Inventory table inline:

| lane | scheduler / cadence | proof | canary | class |
|---|---|---|---|---|
| brain-health-snapshot | launchd daily 08:55 | health snapshot age 2.9h | `brain_health_snapshot` | healthy |
| brain-refresh | launchd hourly | state age 0.3h, ok | `brain_refresh`, `brain_refresh_contract` | healthy |
| dream-sanitize | launchd 4x/day | state age 5.4h, ok | none | unknown |
| gmail-dealflow-digest | launchd daily 08:30 | digest age 3.0h; ingest age 0.3h | `gmail_dealflow_digest`, `gmail_dealflow_ingest` | healthy |
| hermes-overseer | launchd weekly | heartbeat missing; last success 2026-04-29 | no heartbeat canary yet | dead |
| gaia-mcp | launchd keepalive | no state/DB proof; stale logs | none | unknown |
| slack-live-sync | launchd 30m | state fresh, ok; `last_sync_at` old | `slack_live_sync` | healthy, with ambiguity |
| standup-poll | launchd 15m | external state age 1.6h | none | unknown |
| standup-post | launchd daily 08:15 | external state age 1.6h; post recorded | none | unknown |
| qdrant | launchd keepalive | log-only age 0.2h | no daemon canary | unknown |
| openclaw-gateway | launchd keepalive | gateway canary state fresh | gateway/provider probes | healthy |
| gbrain-read-mirror-compare | launchd daily 09:05 | state age 2.7h, ok | `gbrain_read_mirror_compare` | healthy |
| gbrain-shadow-bakeoff | launchd daily 08:47 | state age 3.0h, ok | none | unknown |
| gbrain-sidecar-quality | launchd daily 08:17 | state age 3.5h, ok | none | unknown |
| gmail-pubsub-bridge | launchd keepalive | success log age 1.8h | `gmail_push_freshness` | healthy |
| openclaw-node | launchd keepalive | log-only age 1.9h | indirect only | unknown |
| OpenClaw cron jobs | `~/.openclaw/cron/jobs.json` | file missing | none | unknown |
| formal live-proof ledger | proof tooling | stale 761h | `check_gaia_alpha_liveness` blocker | stale |
| eval cadence | eval tooling | stale 402h, sparse 15<50 | `check_gaia_alpha_liveness` blocker | stale |

Flags: `memory/live-context.md` is absent in this detached worktree, so I did not create or append it. I also briefly ran the launchd-overseer canary by mistake; it only generated `memory/gateway-canary-state.json` inside the child worktree, and I removed that file plus the empty directory.

