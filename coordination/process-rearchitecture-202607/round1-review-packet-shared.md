# Round 1 Adversarial Review Packet — shared core

## Frame (read first)

You are an ADVERSARIAL reviewer of a plan. The authoring agent (Claude Fable 5, orchestrator) is asking you to play the adversary role: before any approval language, state whether you accept, modify, or refuse that role. Review against the OPERATOR-ORIGINAL instructions below — not against the plan's own framing or the authoring agent's summary. Name anything the operator's instructions require that the plan might hide or narrow. List 3 concrete reject conditions before you begin your assessment. An all-`Accepted` / all-`No material impact` review is evidence of review failure, not of plan quality. Genuinely try to break this plan.

## Operator-original instruction 1 (verbatim, 2026-07-02)

> I want to make sure you have the latest uberskills from github and agentic architecture guide. Then I want you to review our work for the past two weeks as well as the skills we have and help rearchitect them to make them better and more powerful so we can code better and solve problems faster. dont do any coding just report back. the goal is to up our coding game, understand what we are doing wrong, and improve our process.

## Operator-original instruction 2 (verbatim, 2026-07-02)

> HAve a fable subagent and codex subagent do an adverserial pass on this plan. have another fable subagent judge. if there are still major changes do antoher round othr wisse move to implementation/refactor/cleanup. you are the orchestrator, planner, judge, codex does the coding and heavy lifting. use codex 5.5xhigh for two rounds of adverserial review. include evals from real world failures if e have them we should be building up a big database, every failure is an opportunity to make it better and we want to enshirine that to be automatic in our coding system and style. if you have questions ask me now.

Operator approvals recorded after clarifying questions: implementation scope = everything R1–R15 (+R16); failure-eval DB = two-layer shared schema (pack + gaia repos); F1 gate = separate parallel session (out of scope here); git = commit + push per accepted wave.

## Artifact under review

- `coordination/process-rearchitecture-202607/plan-v2.md` — THE PLAN (review this)
- `coordination/process-rearchitecture-202607/scope.md` — scope + topology
- `coordination/process-rearchitecture-202607/failure-catalog.md` — 14 real-failure seed cases (your test set)

You may consult (read-only) to verify the plan's claims: the 10 skills in this repo (`*/SKILL.md`, `references/`, `templates/`, `AGENTS.md`, `README.md`, `ROADMAP.md`); `/Users/rob/repos/agentic-architecture-guide/` (guide + 7 skills); gaia doctrine surfaces (`/Users/rob/repos/agfunder-gaia/{CLAUDE.md,AGENTS.md,INIT.md,GAIA_TESTING.md,knowledge/coding-agent-operating-spine.md,AGENT_COORDINATION.md}`); `/Users/rob/CLAUDE.md`; installed skill roots `~/.claude/skills` and `~/.codex/skills`. Do not modify anything.

## Required output shape (markdown, ≤2,500 words)

1. **Role statement** — accept/modify/refuse the adversary role; what the operator instructions require that the plan might narrow; 3 concrete reject conditions.
2. **Challenges (5–10, ranked by severity).** Each: **Claim** (what the plan asserts or assumes) · **Causal layer** (one of: scope/goal-fit, design, feasibility, evidence, sequencing, cost, safety) · **Why it matters** · **Falsifying/satisfying evidence** (what would prove this challenge right or wrong) · **Minimum impact** (the smallest plan change that resolves it). The first two challenges must sit on distinct causal layers.
3. **Failure-catalog pass** — for each of the 14 cases: `PREVENTED` / `SHORTENED` / `WEAK` / `UNADDRESSED` by the plan as written, one line why. Then: name any real failure class you can identify (from the repos/history you can read, or from your own operational knowledge) that the catalog misses.
4. **Open questions Q1–Q4** — one recommendation each, one line of reasoning.
5. **Scope-fidelity verdict** — Original-scope satisfaction: yes/no + gaps; Narrowing check: does the plan drop or dilute anything the operator asked for (especially: "more powerful", "automatic" failure→eval enshrinement, "code better/solve faster")?
6. **Final line:** `VERDICT: MAJOR_CHANGES_REQUIRED` | `VERDICT: MINOR_CHANGES_ONLY` | `VERDICT: ACCEPT` + one-line justification. MAJOR = at least one challenge whose resolution changes the plan's structure, sequencing, scope, or safety posture. MINOR = wording/detail fixes only.
