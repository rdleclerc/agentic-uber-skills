Implemented the additive R15 heartbeat + process telemetry work in the Gaia worktree. I did not run launchd or live sends.

**Diff Summary**
- [scripts/run_hermes_overseer.sh](/Users/rob/repos/worktrees/gaia-childB/scripts/run_hermes_overseer.sh:15): added atomic heartbeat writes, `blocked_auth` classification for the requested Hermes/Codex auth markers, process telemetry compilation, `process.md` prompt inclusion, and non-production proof hooks.
- [scripts/compile_overseer_process.py](/Users/rob/repos/worktrees/gaia-childB/scripts/compile_overseer_process.py:1): new five-section `process.md` compiler.
- [knowledge/hermes-overseer.md](/Users/rob/repos/worktrees/gaia-childB/knowledge/hermes-overseer.md:6): documented current auth blocker, heartbeat, process telemetry, and dry-run behavior.
- [evals/failures/cases/hermes-overseer-dead-9w.md](/Users/rob/repos/worktrees/gaia-childB/evals/failures/cases/hermes-overseer-dead-9w.md:11): moved case to `eval_built`.
- [evals/failures/INDEX.md](/Users/rob/repos/worktrees/gaia-childB/evals/failures/INDEX.md:6): mirrored `eval_built`.

**Heartbeat JSON**
```json
{
  "started_at": "2026-07-03T18:56:24Z",
  "finished_at": "2026-07-03T18:56:33Z",
  "outcome": "blocked_auth",
  "report_path": null,
  "error_summary": "Hermes Codex auth missing; human action required: run `hermes auth` (openai-codex)"
}
```

**process.md First 40 Lines**
````text
# Process Telemetry

Generated: 2026-07-03T18:56:24Z
Lookback: 7 days

## Uber-Run Cost Receipts

| receipt | tokens | minutes | lane_used |
|---|---:|---:|---|
| `wave1-receipt.md` | unknown | 210 | orchestrator/exact-diff = claude-fable-5; implementer = openai-codex/gpt-5.5 xhigh (6 dispatches); independent adversarial lane = claude-fable-5 fresh subagent |
| `wave2-receipt.md` | unknown | 480 | orchestrator/exact-diff = claude-fable-5; implementer = openai-codex/gpt-5.5 xhigh (7 dispatches); independent adversarial lane = claude-fable-5 fresh subagent; routing smokes = claude-sonnet fresh subagents |

- Known current-wave minutes recorded: 690
- Receipts with unknown tokens: 2/2
- Skipped receipts without Run metadata: `wave2-d2-deletion-receipt.md`, `wave2-d3-deletion-receipt.md`, `wave2-d4-deletion-receipt.md`, `wave2-d6-deletion-receipt.md`, `wave3-posture-probe-receipt.md`

Baseline comparison caveat, quoted verbatim:

> - Tokens essentially unrecorded: ONE hard number across all four tasks (Codex terminal output). Post-change token comparison requires the per-dispatch usage receipt convention (R13c) first; until then only that lane is comparable.

Comparison: current receipts now expose minutes and lane_used, but token comparison is still mostly blocked by unknown token fields and the baseline caveat above.

## Doctrine Drift And Install Sync

### Doctrine drift

- command: `python3 /Users/rob/repos/agentic-uber-skills/scripts/lint_pack_contract.py --drift`
- exit_code: 0

stdout:
```text
DOCTRINE DRIFT REPORT registry=/Users/rob/repos/agentic-uber-skills/references/drift-fingerprints.toml
MATCH id=dispatch-mechanics-header target=references/dispatch-and-sessions.md adoption_state=report_only severity=warn blocking_wave=3 source=working_tree
MATCH id=test-channel-posture target=${GAIA_ROOT:-~/repos/agfunder-gaia}/GAIA_TESTING.md adoption_state=blocking severity=warn blocking_wave=2 source=git_ref(origin/main)
MATCH id=test-channel-posture target=${GAIA_ROOT:-~/repos/agfunder-gaia}/CLAUDE.md adoption_state=blocking severity=warn blocking_wave=2 source=git_ref(origin/main)
MATCH id=test-channel-posture target=${GAIA_ROOT:-~/repos/agfunder-gaia}/AGENTS.md adoption_state=blocking severity=warn blocking_wave=2 source=git_ref(origin/main)
MATCH id=test-channel-posture target=${GAIA_ROOT:-~/repos/agfunder-gaia}/skills/gaia-testing/SKILL.md adoption_state=blocking severity=warn blocking_wave=2 source=git_ref(origin/main)
MATCH id=canary-command target=${GAIA_ROOT:-~/repos/agfunder-gaia}/GAIA_TESTING.md adoption_state=blocking severity=warn blocking_wave=2 source=git_ref(origin/main)
MATCH id=canary-command target=${GAIA_ROOT:-~/repos/agfunder-gaia}/CLAUDE.md adoption_state=blocking severity=warn blocking_wave=2 source=git_ref(origin/main)
MATCH id=canary-command target=${HOME}/CLAUDE.md adoption_state=blocking severity=warn blocking_wave=2 source=working_tree
````

**Checks**
- `bash -n scripts/run_hermes_overseer.sh`: pass, no output.
- `python3 -m py_compile scripts/compile_overseer_process.py`: pass, no output.
- `scripts/run_hermes_overseer.sh` no-send auth-marker proof: exit `1` as expected, heartbeat `blocked_auth`, process telemetry built.
- `process.md` section check: exactly five `##` sections.
- `python3 /Users/rob/repos/agentic-uber-skills/scripts/validate_failure_case.py evals/failures/cases/`: `PASS: validated 10 failure case file(s)`.
- `node --test tests/integration/failure_evals.test.mjs`: 2/2 pass.
- Process-pack `--index`: pass.
- Gaia local `--index`: fails because the pack validator only accepts `canonical: evals/failures/cases/<id>.md`, while the Gaia mirror currently uses `canonical: agfunder-gaia/evals/failures/`. I left that broader index-format decision untouched.

**Flags**
- I did not run the full `OVERSEER_DRY_RUN=1 scripts/run_hermes_overseer.sh` because the existing export script invokes git metadata/log commands, conflicting with the “NO git commands” dispatch constraint.
- Current dry-run behavior skips Hermes unless `OVERSEER_DRY_RUN_HERMES=1`; I documented that instead of changing the restored pipeline semantics.
- A real Hermes attempt in this sandbox hit `PermissionError` on `~/.hermes/auth.lock`, so the `blocked_auth` proof used a local Hermes shim emitting the documented auth marker.
- High-tier Claude review was not reachable: local Claude is not logged in, and `type0`/`agclaw` hostnames were not resolvable from this runtime. This is locally verified only, not independently Claude-accepted.