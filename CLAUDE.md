# CLAUDE.md

Claude agents working in this repo must follow `AGENTS.md` as the canonical agent contract.

Adapter notes:

- Treat this as a platform-neutral skill pack, not a Claude-only pack.
- `$ubergoal` is the default router; invoke phase skills directly only when explicitly named or when `$ubergoal` routes to them.
- Keep edits small and evidence-backed. Run the pack contract tests plus touched skill tests before claiming completion.
