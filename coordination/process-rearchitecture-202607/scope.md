# Scope — Process Rearchitecture Campaign (2026-07)

Campaign home: `agentic-uber-skills/coordination/process-rearchitecture-202607/`
Orchestrator session: Claude Fable 5 (Claude Code), started 2026-07-02.

## Operator-original instruction (verbatim, message 1, 2026-07-02)

> I want to make sure you have the latest uberskills from github and agentic architecture guide. Then I want you to review our work for the past two weeks as well as the skills we have and help rearchitect them to make them better and more powerful so we can code better and solve problems faster. dont do any coding just report back. the goal is to up our coding game, understand what we are doing wrong, and improve our process.

## Operator-original instruction (verbatim, message 2, 2026-07-02)

> HAve a fable subagent and codex subagent do an adverserial pass on this plan. have another fable subagent judge. if there are still major changes do antoher round othr wisse move to implementation/refactor/cleanup. you are the orchestrator, planner, judge, codex does the coding and heavy lifting. use codex 5.5xhigh for two rounds of adverserial review. include evals from real world failures if e have them we should be building up a big database, every failure is an opportunity to make it better and we want to enshirine that to be automatic in our coding system and style. if you have questions ask me now.

## Operator approvals (recorded 2026-07-02/03 via structured questions)

1. **Implementation scope: Everything R1–R15** (plus R16 failure→eval pipeline mandated in message 2).
2. **Failure-eval DB home: two-layer, shared schema** — portable process/skill failures → `agentic-uber-skills/evals/failures/`; Gaia runtime failures → `agfunder-gaia/evals/failures/`; one shared case schema + cross-index.
3. **F1 data-subject gate: parallel separate session** (chip spawned `task_4f683ae9`; NOT part of this campaign).
4. **Git: commit + push per accepted wave** for `agentic-uber-skills` and `agentic-architecture-guide`.

## Interpreted scope

Rearchitect the coding-process estate (uber pack + architecture-guide skills + gaia doctrine surfaces + home CLAUDE.md) per plan items R1–R16 in `plan-v2.md`, after two rounds of adversarial review (Fable subagent + Codex gpt-5.5 xhigh; Fable subagent judge; orchestrator rules). Codex implements; orchestrator plans, verifies, accepts; no self-approval.

## Non-goals / deferrals

- F1 data-subject gateway gate (separate parallel session).
- Any Gaia feature work beyond process/liveness items named in the plan.
- Platform 3-repo split (still deferred per standing decision).
- gaianews-web and unrelated repos.
- No changes to OpenClaw vendor runtime internals (`~/.local/lib/node_modules/openclaw/dist/`).

## Execution topology

- **Orchestrator / planner / final judge:** Claude Fable 5 (this session).
- **Adversarial review:** one Fable subagent + one Codex `gpt-5.5` `xhigh` run per round; two rounds budgeted; Fable subagent judge reconciles each round; orchestrator rules on every challenge. If major changes remain after round 2 → back to operator.
- **Implementation:** Codex `gpt-5.5` via direct `codex exec` (dispatch-ops doctrine: orchestrator owns git + DB, duplicate cull, checkpoint commits before dispatch).
- **Gates per wave:** pack contract tests + touched-skill tests + `quick_validate.py`; new drift-check + install-sync check once they exist (Wave 1); word-count deltas recorded (Wave 2 must be net-negative); fresh-agent smoke prompts for routing changes; GAIA_TESTING mandatory triggers for anything touching gaia repo surfaces; live launchd proofs for liveness/Hermes work; every campaign failure appended to the failure-eval DB as it happens.
- **Approval boundary:** waves commit + push on acceptance; anything destructive or outside the named repos returns to the operator first.

## Constraints

- ~10 parallel operator sessions read these doctrine files live; edits land wave-atomically with working-state committed, never mid-refactor.
- Sanitization: pack-layer artifacts (this repo, pushed to GitHub) carry no named individuals or credentials; person-level incident detail stays in `agfunder-gaia` layer.
- Preserve the pack's proven invariants: scope fidelity, adversarial acceptance, class-level RCA, live-proof-before-done. Rearchitecture changes their cost, not their existence.
