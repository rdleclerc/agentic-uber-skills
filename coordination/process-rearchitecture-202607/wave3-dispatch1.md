# Wave 3 — Dispatch 1: R12 dispatch-and-sessions contract + R11 debug loop (pack)

You are Codex, implementer. Pack repo only; NO git commands. Operator decisions recorded 2026-07-03: ubershow = keep-slimmed; posture probe = orchestrator runs it (in progress in parallel — do not touch gaia).

## 1. R12 — `references/dispatch-and-sessions.md` (NEW, single home, ≤700 words)

The dispatch + parallel-session contract, consolidating standing doctrine + this campaign's receipted lessons. Sections:
- **Dispatch mechanics**: direct `codex exec` (no companion); ALWAYS pin working root with `-C` (never inherit cwd — near-miss receipted in wave1-receipt.md); ALWAYS redirect stdin (`- < packet.md` for file prompts, `< /dev/null` for arg prompts — codex blocks forever on open non-TTY stdin, see wave2-v3-probe.md); checkpoint-commit before dispatch; run `--dispatch-preflight` (writeability, case 19) before any implementation dispatch or commit promise; duplicate cull + claim-before-launch (one dispatch per work item, ledger row before launch — case 11); pipelines assert on EXIT CODES, never grep failure text (a8dd954e incident, case 21 family).
- **Orchestrator ownership**: git + DB belong to the orchestrator; implementers never run git; orchestrator reconciles implementer result receipts AGAINST THE TREE before commit (case 20 instances); wave pushes assert each landed SHA is-ancestor of the target branch tip (case 22).
- **Sandbox-blind claims**: implementers cite verified real interface shapes for any fake/stub (interface-shape receipt, case 10); DB claims live-verified by the orchestrator; **injection claims cite the loader** — any statement that a file is/isn't live-injected into agent sessions must cite config/code evidence (e.g. OpenClaw `BOOTSTRAP_FILE_NAMES`), case 23.
- **Parallel sessions**: shared-ref safety = worktrees off main for cross-session repos, never the other session's checkout; coordination notes at repo root coordination/ for cross-session asks; non-fast-forward push failures are a feature — reconcile via rebase, never force-push over another session's line.
- **Dispatch ledger**: minimal row format (id, work item, root, launched_at, exit, output_path, retry_count); retry-once-then-ledger on subprocess death without terminal state (case 21).

Add: one ubergoal routing-table row pointing at it (mind the 800 budget — trim elsewhere if needed and report); a drift fingerprint for its dispatch-mechanics header line (report_only, blocking_wave 3); update case files 10/11/21/22/23 `eval_check`/body to cite this reference + set case 11 + 21 status to eval_built if their checks are now named executables/checklists here (be honest: ledger validation is a checklist until a validator exists — keep status seed if so).

## 2. R11 — `references/debug-loop.md` (NEW, ≤350 words) — reference form per plan default

Everyday defect loop: reproduce (capture the failing command/output = the reproduced-red receipt, already validator-defined) → hypothesize → bisect → fix → verify (rerun the red, now green) → intake field on exit (P4). Escalation rule: repeated same-class failure (2nd occurrence) or architecture-shaped symptoms → `$uberrca` with class_invariant + surface_enumeration. Boundary line: uberrca = class-level/incident authority (never auto-triggers); this loop = the default for ordinary defects. Add ubergoal routing row ("everyday defect / bug fix → references/debug-loop.md; repeats or incidents → $uberrca") and one boundary line in uberrca/SKILL.md (budget 1,500 — fits). Bind catalog cases 3/4 eval_check text to this reference where they currently name only validators.

## 3. Verify + report

Full pack tests + lint --strict (drift now gates it); quick_validate + per-skill tests for ubergoal/uberrca; validate_failure_case (cases + --index); word deltas (ubergoal MUST stay ≤800; report exactly). Print receipts inline; FLAG contradictions rather than resolving silently.
