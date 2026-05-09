# claude-code-skills

A collection of portable `SKILL.md` skills for Claude Code and Codex — behavioral protocols that teach coding agents to do harder things correctly.

## Skills

| Skill | What it does |
|-------|-------------|
| [deep-rca](deep-rca/) | Forces class-level root cause analysis before patches — prevents agents from stopping at proximate causes |
| [ubergoal](ubergoal/) | Thin lifecycle wrapper for substantial coding workflows: classify, route, launch goals, accept, learn |
| [uberplan](uberplan/) | Rigorous lean planning with review lanes, exploration trails, confidence gates, and benefit >> cost pressure |
| [uberaccept](uberaccept/) | Adversarial final acceptance with evidence audits, architecture drift checks, and completion proof |
| [uberskillevolver](uberskillevolver/) | Captures post-run skill lessons and promotes only evidence-backed evals, validators, templates, or deletions |

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
# Install the Uber skill family for Codex
ln -s "$(pwd)/ubergoal" ~/.codex/skills/ubergoal
ln -s "$(pwd)/uberplan" ~/.codex/skills/uberplan
ln -s "$(pwd)/uberaccept" ~/.codex/skills/uberaccept
ln -s "$(pwd)/uberskillevolver" ~/.codex/skills/uberskillevolver
```

Then invoke the wrapper with `$ubergoal`, or call phase skills directly with `$uberplan`, `$uberaccept`, and `$uberskillevolver`.

## What is a SKILL.md skill?

A skill is a `SKILL.md` file that gives a coding agent a behavioral protocol — a set of rules, steps, and constraints that override its defaults for a specific kind of task. In Claude Code, skills are invoked via slash commands or referenced in a project's `CLAUDE.md`; in Codex, installed skills are invoked with `$skill-name`, for example `$ubergoal`.

See the [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) for more on skills.

## License

MIT
