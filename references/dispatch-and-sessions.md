# Dispatch And Sessions Reference

Single home for dispatch, implementer-session, and parallel-ref safety doctrine. Use this before launching implementation subprocesses or coordinating multiple sessions against shared repos.

## Dispatch mechanics

Use direct `codex exec`; do not wrap it in a companion process unless the orchestrator has a named reason and receipt. Always pin the working root with `-C <repo-root>`; never inherit the orchestrator cwd. Wave 1 had a near miss from cwd inheritance, so `-C` is not optional.

Always redirect stdin explicitly. Use `codex exec - < packet.md` for file prompts and `< /dev/null` for prompt arguments. The Wave 2 V3 probe showed Codex can block forever on open non-TTY stdin.

Checkpoint-commit before dispatch. Commit or stash the orchestrator tree before dispatching so implementer receipts reconcile against a known state. Before any implementation dispatch or commit promise, run `scripts/lint_pack_contract.py --dispatch-preflight <root>` or the equivalent repo preflight: writeability, repository status probe, and temp-dir write/delete. This is case 19.

Cull duplicates and claim before launch. One work item gets one dispatch, and the ledger row exists before launch. If a duplicate is discovered, cancel or merge ownership before work starts. This is case 11.

Pipeline assertions are on exit codes and required artifacts, not grepped failure text. The a8dd954e incident proved that grepping an error line while ignoring the command exit can ship invalid work.

## Orchestrator ownership

Git and DB side effects belong to the orchestrator. Implementers do not run git. The orchestrator reconciles implementer receipts against the actual tree before commit; case 20 had receipt/tree mismatches. Wave pushes must assert every landed SHA is an ancestor of the target branch tip before the wave is declared landed. That is case 22.

## Sandbox-blind claims

Implementers cite verified real interface shapes for any fake or stub that stands in for an external interface or DB row. A fake is not evidence unless its shape is traced to the real interface. This is case 10.

DB claims are live-verified by the orchestrator, not by an implementer sandbox. Injection claims cite the loader: any statement that a file is or is not live-injected into agent sessions must cite config or code evidence, such as OpenClaw `BOOTSTRAP_FILE_NAMES`. This is case 23.

## Parallel sessions

For cross-session repos, use worktrees off main and never another session's checkout. Put coordination notes and asks under repo-root `coordination/` so the next orchestrator can reconcile the queue without relying on chat memory.

Non-fast-forward push failures are a feature. Reconcile by rebasing or merging the other session's line; never force-push over another session's branch or shared ref without explicit operator authorization.

## Dispatch ledger

Minimal row:

`id | work_item | root | launched_at | exit | output_path | retry_count`

If a subprocess dies without a truthful terminal state, retry once. If it still has no terminal output, ledger the failure with exit code, missing artifact, retry count, and failure intake instead of silently relaunching. This is case 21.
