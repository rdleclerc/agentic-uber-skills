# claude-code-skills

A collection of skills for [Claude Code](https://claude.ai/code) — behavioral protocols that teach coding agents to do harder things correctly.

## Skills

| Skill | What it does |
|-------|-------------|
| [deep-rca](deep-rca/) | Forces class-level root cause analysis before patches — prevents agents from stopping at proximate causes |

## Install

Copy any skill directory into `~/.claude/skills/`:

```bash
# Clone the repo
git clone https://github.com/rdleclerc/claude-code-skills.git

# Install a skill
cp -r claude-code-skills/deep-rca ~/.claude/skills/deep-rca
```

The skill is then available as `/deep-rca` in Claude Code.

## What is a Claude Code skill?

A skill is a `SKILL.md` file that gives Claude Code a behavioral protocol — a set of rules, steps, and constraints that override its defaults for a specific kind of task. Skills are invoked via slash commands (`/deep-rca`) or referenced in a project's `CLAUDE.md` to apply them automatically.

See the [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) for more on skills.

## License

MIT
