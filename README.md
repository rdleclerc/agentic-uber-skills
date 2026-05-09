# claude-code-skills

A collection of portable `SKILL.md` skills for Claude Code and Codex — behavioral protocols that teach coding agents to do harder things correctly.

## Skills

| Skill | What it does |
|-------|-------------|
| [deep-rca](deep-rca/) | Forces class-level root cause analysis before patches — prevents agents from stopping at proximate causes |
| [ubergoal](ubergoal/) | Turns substantial coding work into a lean plan, Codex goal objective, evidence rubric, and final acceptance proof without unnecessary process |

## Install

Copy any skill directory into `~/.claude/skills/`:

```bash
# Clone the repo
git clone https://github.com/rdleclerc/claude-code-skills.git

# Install a skill
cp -r claude-code-skills/deep-rca ~/.claude/skills/deep-rca
```

The skill is then available as `/deep-rca` in Claude Code.

### Codex install

Copy or symlink a skill directory into `~/.codex/skills/`:

```bash
# Install ubergoal for Codex
ln -s "$(pwd)/ubergoal" ~/.codex/skills/ubergoal
```

Then invoke it in Codex with `$ubergoal`.

## What is a SKILL.md skill?

A skill is a `SKILL.md` file that gives a coding agent a behavioral protocol — a set of rules, steps, and constraints that override its defaults for a specific kind of task. In Claude Code, skills are invoked via slash commands or referenced in a project's `CLAUDE.md`; in Codex, installed skills are invoked with `$skill-name`, for example `$ubergoal`.

See the [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) for more on skills.

## License

MIT
