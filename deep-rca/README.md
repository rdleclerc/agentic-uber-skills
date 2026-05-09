# deep-rca — portable agent skill

A portable agent skill that forces coding agents to find class-level root causes instead of patching proximate symptoms.

## The problem it solves

When debugging, agents and humans naturally stop at the first explanation that fits — the proximate cause. They identify what happened and propose a fix for that specific instance. The fix works once, then the same failure recurs through a different trigger, because the underlying invariant was never enforced.

This skill gives the agent three mechanisms to break that pattern:

1. **Self-challenge loop** — before surfacing any RCA, the agent must challenge its own answer: *"This is still proximate because ___."* If it can fill in that blank, it keeps going. The loop replaces the human having to manually ask "but is that really the root cause?" on every turn.

2. **Convergence test** — the agent knows it's at root cause when it can write: *"If [single gate/policy/constraint] had been enforced, this entire failure class would have been impossible."* Not just this instance — the class.

3. **Depth floor** — the agent knows it's gone too far when the answer becomes a full system redesign or a language-level complaint. When that happens, it backs up 1–2 rungs and presents the deepest *actionable* cause.

## Install

Copy or symlink this directory into your agent runtime's local skills directory. Examples:

```bash
# Generic
mkdir -p ~/.agent/skills
ln -s "$PWD/deep-rca" ~/.agent/skills/deep-rca

# Codex-compatible
mkdir -p ~/.codex/skills
ln -s "$PWD/deep-rca" ~/.codex/skills/deep-rca

# Claude Code-compatible
mkdir -p ~/.claude/skills
cp -R "$PWD/deep-rca" ~/.claude/skills/deep-rca
```

## Usage

Invoke the skill using your runtime's skill syntax, or explicitly ask the agent to use `deep-rca` before proposing a patch.

```markdown
For any incident investigation or bug report, use the `deep-rca` skill before proposing a patch.
```

The skill should activate when you ask about root causes, postmortems, debugging, stuck loops, production failures, repeated bugs, or whether a proposed patch addresses the underlying issue.

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
