# agentic-uber-skills

A platform-neutral skill pack for agentic coding workflows. These are portable `SKILL.md` protocols: use them with any agent runner that supports local skills or can be instructed to load a `SKILL.md` file.

The pack is not tied to Claude or Codex. Some skills include optional adapter notes for specific runtimes, such as Codex goals, but the core workflows are general agentic engineering protocols.

## Skills

| Skill | What it does |
|-------|-------------|
| [deep-rca](deep-rca/) | Forces class-level root cause analysis before patches — prevents agents from stopping at proximate causes |
| [ubergoal](ubergoal/) | Thin lifecycle wrapper for substantial agentic coding workflows: classify, route, launch goals, accept, learn |
| [uberplan](uberplan/) | Rigorous lean planning with review lanes, exploration trails, confidence gates, and benefit >> cost pressure |
| [uberaccept](uberaccept/) | Adversarial final acceptance with evidence audits, architecture drift checks, and completion proof |
| [uberskillevolver](uberskillevolver/) | Captures post-run skill lessons and promotes only evidence-backed evals, validators, templates, or deletions |

## Install

Clone the pack:

```bash
git clone https://github.com/rdleclerc/agentic-uber-skills.git
cd agentic-uber-skills
```

### Generic install

Copy or symlink the skill directories into your agent runtime's local skill directory:

```bash
# Example: install the Uber family into a generic local skill dir
mkdir -p ~/.agent/skills
for s in ubergoal uberplan uberaccept uberskillevolver; do
  rm -rf "$HOME/.agent/skills/$s"
  ln -s "$PWD/$s" "$HOME/.agent/skills/$s"
done
```

### Codex-compatible install

```bash
mkdir -p ~/.codex/skills
for s in ubergoal uberplan uberaccept uberskillevolver; do
  rm -rf "$HOME/.codex/skills/$s"
  ln -s "$PWD/$s" "$HOME/.codex/skills/$s"
done
```

Invoke the wrapper with `$ubergoal`, or call phase skills directly with `$uberplan`, `$uberaccept`, and `$uberskillevolver`.

### Claude Code-compatible install

```bash
mkdir -p ~/.claude/skills
for s in deep-rca ubergoal uberplan uberaccept uberskillevolver; do
  rm -rf "$HOME/.claude/skills/$s"
  cp -R "$PWD/$s" "$HOME/.claude/skills/$s"
done
```

Use whatever invocation form your runtime supports. If the runtime does not have native skill discovery, paste or reference the relevant `SKILL.md` file explicitly.

## What is a SKILL.md skill?

A `SKILL.md` skill is a portable Markdown protocol that gives an agent specialized operating instructions: workflows, constraints, templates, validation scripts, and references for a recurring class of work.

The goal is progressive disclosure: load the skill metadata first, then the `SKILL.md` body when needed, and only open bundled templates/scripts/references when the task requires them.

## Update

```bash
cd ~/path/to/agentic-uber-skills
git pull --ff-only
```

If you installed with symlinks, updates apply immediately. If you copied directories, copy them again after pulling.

## License

MIT
