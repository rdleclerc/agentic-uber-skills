# AGENTS.md

Agent-facing contract for `agentic-uber-skills`.

## Canonical sources

Read in this order:

1. This `AGENTS.md` for repo-level routing, edit, sync, and anti-bloat rules.
2. `README.md` for human install/use docs.
3. `ROADMAP.md` for deferred modules, maturity gates, and cross-machine learning policy.
4. The relevant skill's `SKILL.md`.
5. That skill's local `templates/`, `references/`, `scripts/`, `tests/`, and `evals/` only as needed.

`CLAUDE.md` is an adapter note and must not contradict this file.

## Routing contract

- `$ubergoal` is the only default/implicit Uber lifecycle router.
- All skills in this pack must be installed and exposed to Codex sessions. Exposure is not trigger authority.
- Claude Code skill frontmatter for every pack skill must keep `model: claude-opus-4-8` and `effort: max` so Uber-skill invocations default to Opus 4.8 max in every session.
- Phase skills are explicit or wrapper-invoked: `$uberplan`, `$uberaccept`, `$uberskillevolver`, `$ubersimplify`, and `$uberassess` should not trigger merely because a task resembles their domain. Their descriptions and OpenAI adapter prompts should say "Do not auto-trigger from task similarity" so runtime skill routers do not confuse examples with permission.
- `$uberrca` is a utility skill, not an Uber lifecycle phase. Use it directly for general incidents, debugging, postmortems, repeated bugs, and class-level root-cause analysis.
- `ubershow` = visual communication utility, not an Uber lifecycle phase. Use it when a browser-first static artifact will materially improve decision speed or comprehension; generated HTML is a view, and copy/paste receipts are the decision registration path.
- `uber-skill-creator` = bundled utility for creating, updating, evaluating, and migrating portable SKILL.md skills. Legacy local installs named `skill-creator` or `skill-creator-pro` should redirect to `uber-skill-creator` for general portable skills, or to `openclaw-agentic-skill-creator` for OpenClaw/Gaia/Type0/Soho-specific skills.
- `uberassess` = source-to-recommendation due diligence. It assesses X/GitHub/arXiv/articles/videos/Hermes signals for adoption; it does not implement or mutate without approval, and approved build work routes to `ubergoal`/`uberplan`.
- If a user names a phase skill directly, use that phase skill. If the user asks which Uber skill to use, route through `$ubergoal`.
- Use the lightest tier that makes the work safe. Process is cost.
- Avoid duplicate planning artifacts: Tier 1 coding work can use the Coding Agent Work Contract as the plan; Tier 2/3 `uberplan` should extend that contract rather than create parallel objective/scope/evidence bureaucracy.
- `uberplan` produces a long-running goal execution plan, not an `uberslice` or default 20-minute slice. It may define checkpoints, phases, or bounded work packages, but those serve the larger goal. Return thread highlights and a durable `.md` plan file.
- `uberplan` and `ubergoal` must include a user expectation / surprise assessment for Tier 1+ or otherwise material work: infer likely expectations from the explicit request, known preferences, repo instructions, and evidence; name planned or actual choices that may surprise the user; ask or flag before proceeding when a mismatch could matter.
- For OpenClaw/agentic-system plans, use the proof ladder: first prove a Codex subagent with the right skills/tools/context can execute the activity; if it cannot, improve the skill/tool/context contract. Then prove the OpenClaw or target runtime reaches parity; if it fails, iterate the same contracts until parity is proven twice.
- During testing, do not push through systematic failures or material unexpected failures that invalidate the plan. Stop before or at five consecutive clear failures of the same command/failure family, run `uberrca`, and if the RCA changes scope, create a focused child/sub-`uberplan` appendix. Append or merge that child plan into the parent `uberplan` as a `scope expansion`, `scope correction`, or `blocker`, update the ledger/receipt, then continue under the same `ubergoal` only after the merged plan names the new hypothesis and evidence gate.

## RCA source authority

- `uberrca` = general incident/root-cause authority. It supplies the RCA ladder, self-challenge loop, depth floor, and class-level invariant discipline.
- Agent Advocate = agent-behavior-specific RCA lens inside `uberplan`, `uberaccept`, and `ubersimplify`. It asks what the agent saw, whether a competent human would have made the same error, and which context/tool/source/memory/feedback/affordance gap caused the human-parity failure.
- If both apply, use the `uberrca` ladder for depth and the Agent Advocate lens for agent-specific evidence. Neither can waive the other's required evidence when both scopes are active.
- Never accept “the model made a bad judgment” as root cause until the failed deterministic guard, context/source authority, tool contract, eval, memory, or feedback loop is named.

## Edit rules

- Keep `ubergoal` thin. It routes; it does not absorb planning, acceptance, simplification, or learning machinery.
- Add durable machinery only when benefit is clearly **much greater than** implementation, maintenance, context, coordination, eval, rollback, latency, and operator-attention cost.
- Prefer small validators/tests over prose-only policy when a failure class can drift.
- Do not create another new `uber*` skill until repeated real-project use proves extraction makes the common path smaller, faster, or safer; `uberassess` is admitted because source-to-recommendation assessment is a repeated cross-project workflow with clear no-implementation safety boundaries, and `ubershow` is admitted because repeated coding sessions needed high-bandwidth visual decision surfaces without adding a server or UI framework.
- Do not silently self-modify skills from learning records; learning packets are evidence, not authority.

## Test commands

Run the pack contract first after routing/docs changes:

```bash
python3 scripts/lint_pack_contract.py
python3 -m unittest discover -s tests -v
```

For touched skills, run their local lint/tests:

```bash
python3 <skill>/scripts/lint_skill_package.py "$PWD/<skill>"
python3 -B -m unittest discover -s <skill>/tests -v
```

For skill shape changes, also run the Codex skill validator when available:

```bash
uv run --with pyyaml python uber-skill-creator/scripts/quick_validate.py <skill>
```

## Install and sync policy

- Source repo: `/Users/claw1/agentic-uber-skills`.
- Local Codex install target: `/Users/claw1/.codex/skills/<skill>`.
- After changing a skill that local Codex should use, sync that skill directory to `/Users/claw1/.codex/skills/<skill>` and validate the installed copy.
- Generic/Codex/Claude install docs should list the same pack directories unless a directory is explicitly labelled optional.
- Codex adapter metadata should expose every pack skill; direct-use/phase gating belongs in the skill descriptions and prompts, not in hiding the skill from session context.
- Do not commit, tag, push, or publish without explicit user authorization.

## Release checklist

Before claiming ready:

- Pack contract lint/tests pass.
- Each touched skill lint/tests pass.
- Installed Codex copies are synced and validated when local use is expected.
- README/ROADMAP/AGENTS agree on routing, source authority, install policy, and maturity state.
- Residual gaps are named, especially fresh-agent behavioral eval gaps.
