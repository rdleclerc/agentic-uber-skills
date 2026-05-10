# agentic-uber-skills

A platform-neutral skill pack for agentic coding workflows. These are portable `SKILL.md` protocols: use them with any agent runner that supports local skills or can be instructed to load a `SKILL.md` file.

The pack is not tied to Claude or Codex. Some skills include optional adapter notes for specific runtimes, such as Codex goals, but the core workflows are general agentic engineering protocols.

Agent-facing source authority lives in [AGENTS.md](AGENTS.md). The default routing rule is: invoke `$ubergoal` as the implicit lifecycle router; invoke phase skills directly only when explicitly named or when `$ubergoal` routes to them. Phase-skill metadata intentionally says not to auto-trigger from task similarity; this prevents ceremony creep from broad descriptions.

## Skills

| Skill | What it does |
|-------|-------------|
| [deep-rca](deep-rca/) | Utility skill for general class-level root cause analysis before patches; Agent Advocate remains the agent-behavior RCA lens inside Uber planning/acceptance |
| [ubergoal](ubergoal/) | Thin lifecycle wrapper for substantial agentic coding workflows: classify, route, launch goals, accept, learn |
| [uberplan](uberplan/) | Rigorous lean planning with review lanes, exploration trails, confidence gates, and benefit >> cost pressure |
| [uberaccept](uberaccept/) | Adversarial final acceptance with evidence audits, architecture drift checks, and completion proof |
| [uberskillevolver](uberskillevolver/) | Captures post-run skill lessons and promotes only evidence-backed evals, validators, templates, or deletions |
| [ubersimplify](ubersimplify/) | Opt-in complexity/modularity/dead-code audits with timestamped trails; Patch mode is conservative/experimental until dogfooded |
| [uberassess](uberassess/) | Explicit source-to-recommendation assessment for X/GitHub/arXiv/articles/videos before adoption; preserves source authority and approval boundaries |

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
for s in deep-rca ubergoal uberplan uberaccept uberskillevolver ubersimplify uberassess; do
  rm -rf "$HOME/.agent/skills/$s"
  ln -s "$PWD/$s" "$HOME/.agent/skills/$s"
done
```

### Codex-compatible install

```bash
mkdir -p ~/.codex/skills
for s in deep-rca ubergoal uberplan uberaccept uberskillevolver ubersimplify uberassess; do
  rm -rf "$HOME/.codex/skills/$s"
  ln -s "$PWD/$s" "$HOME/.codex/skills/$s"
done
```

Invoke the wrapper with `$ubergoal` by default. Call `$deep-rca` for general RCA, and call phase skills directly only when you explicitly want `$uberplan`, `$uberaccept`, `$uberskillevolver`, `$ubersimplify`, or `$uberassess`.

### Claude Code-compatible install

```bash
mkdir -p ~/.claude/skills
for s in deep-rca ubergoal uberplan uberaccept uberskillevolver ubersimplify uberassess; do
  rm -rf "$HOME/.claude/skills/$s"
  cp -R "$PWD/$s" "$HOME/.claude/skills/$s"
done
```

Use whatever invocation form your runtime supports. If the runtime does not have native skill discovery, paste or reference the relevant `SKILL.md` file explicitly.

## What is a SKILL.md skill?

A `SKILL.md` skill is a portable Markdown protocol that gives an agent specialized operating instructions: workflows, constraints, templates, validation scripts, and references for a recurring class of work.

The goal is progressive disclosure: load the skill metadata first, then the `SKILL.md` body when needed, and only open bundled templates/scripts/references when the task requires them.


## RCA authority

- `$deep-rca` is the general incident/debugging/root-cause utility.
- Agent Advocate is the agent-behavior-specific RCA lens inside `$uberplan`, `$uberaccept`, and `$ubersimplify`.
- If both apply, use the `deep-rca` ladder for depth and the Agent Advocate human-counterfactual lens for agent-specific context/tool/source/feedback failures.

## Roadmap and cross-machine learning

- Roadmap: [ROADMAP.md](ROADMAP.md)
- Shared sanitized learning inbox: [learning/](learning/)
- Cross-machine learning guide: [uberskillevolver/references/cross-machine-learning.md](uberskillevolver/references/cross-machine-learning.md)

Keep raw learning records local/private. Commit only sanitized learning packets under `learning/inbox/<machine-id>/...` after `uberskillevolver` validation and privacy review.

## Update

```bash
cd ~/path/to/agentic-uber-skills
git pull --ff-only
```

If you installed with symlinks, updates apply immediately. If you copied directories, copy them again after pulling.

## License

MIT
