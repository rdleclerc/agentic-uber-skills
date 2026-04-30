# deep-rca — Claude Code skill

A Claude Code skill that forces coding agents to find class-level root causes instead of patching proximate symptoms.

## The problem it solves

When debugging, agents (and humans) naturally stop at the first explanation that fits — the proximate cause. They identify what happened and propose a fix for that specific instance. The fix works once, then the same failure recurs through a different trigger, because the underlying invariant was never enforced.

This skill gives the agent three mechanisms to break that pattern:

1. **Self-challenge loop** — before surfacing any RCA, the agent must challenge its own answer: *"This is still proximate because ___."* If it can fill in that blank, it keeps going. The loop replaces the human having to manually ask "but is that really the root cause?" on every turn.

2. **Convergence test** — the agent knows it's at root cause when it can write: *"If [single gate/policy/constraint] had been enforced, this entire failure class would have been impossible."* Not just this instance — the class.

3. **Depth floor** — the agent knows it's gone too far when the answer becomes a full system redesign or a language-level complaint. When that happens, it backs up 1–2 rungs and presents the deepest *actionable* cause.

## Install

```bash
# From the Claude Code skill registry (if published)
claude skill install deep-rca

# Or manually: copy SKILL.md into your skills directory
cp SKILL.md ~/.claude/skills/deep-rca/SKILL.md
```

## Usage

Invoke via the `/deep-rca` slash command in Claude Code, or reference it in your `CLAUDE.md`:

```markdown
For any incident investigation or bug report, invoke the `deep-rca` skill before proposing a patch.
```

The skill activates automatically when Claude Code detects you're asking about root causes, postmortems, debugging, stuck loops, or production failures — or when you challenge whether a proposed patch addresses the underlying issue.

## What it produces

- An 8-rung RCA ladder (symptom → class-level cause)
- Self-challenge result proving the agent went deep enough
- Depth floor check explaining where it stopped and why
- Durable fix plan mapped to the lowest enforceable layer
- Tests/evals/monitors that would have caught the issue earlier

## Design notes

The patch selection preference order (state machine → admission policy → tool enforcement → autonomous resolver → prompt alignment → observability) reflects a key principle: the lower in the stack you enforce an invariant, the more durable the fix. A state machine that makes invalid transitions unrepresentable is more reliable than a prompt that tells an agent not to make them.

The skill is written for agentic/autonomous systems but applies equally to conventional software bugs. The self-challenge loop and convergence test are domain-agnostic.

## License

MIT
