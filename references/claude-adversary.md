# Claude adversary opt-in contract

Use this reference when an Uber skill invocation explicitly asks for Claude review, for example: `with Claude`, `Claude review`, `Claude debate`, `Claude adversarial review`, or `Claude for 2 rounds`.

Do **not** invoke the Claude adversary from task similarity, from a generic need for quality, or from ordinary use of an Uber skill. A prompt without an explicit Claude-adversary phrase should not mention adversary invocation. Skill bodies intentionally inline the key rules from this reference because runtime skill readers may not auto-load shared references.

## Trigger examples

- Trigger: `use uberplan with Claude to review this plan`.
- Trigger: `use uberaccept with Claude for 2 rounds`.
- Non-trigger example: `use uberassess on this plan` should run ordinary `uberassess` without Claude adversary language.

## Role contract

- Codex remains owner and reconciler. Claude is an adversarial reviewer, not a co-author, final authority, integrator, or acceptance substitute.
- Default to one Claude challenge round. Run two or three rounds only when the user requests them or when material unresolved risk remains in a high-stakes plan/RCA/acceptance artifact.
- If Claude is unavailable, continue without inventing a fake review and record the missing proof as a gap.
- Do not add a hidden reviewer loop, cron, persistent debate state, semantic judge, or orchestration harness.

## Challenge format

Each Claude challenge should include:

1. **Claim** — the specific artifact claim, assumption, or omission being challenged.
2. **Causal layer** — one of: proximal/direct cause, structural/systemic cause, modularity/seam, evidence/receipt, agent-affordance, operator/approval boundary.
3. **Why it matters** — the failure this could create.
4. **Falsifying/satisfying evidence** — what would prove or disprove the challenge.
5. **Minimum impact threshold** — what must change, be risk-tagged, or be explicitly rejected for the challenge to matter.

A review round that raises more than one challenge must cover at least two causal layers. The first two challenges must name distinct layers. A single-challenge round must explicitly state why only one challenge is material.

Layer tags must not be gamed: two differently tagged challenges that name the same underlying factor count as one layer. A structural/systemic challenge must identify a different structural incentive, constraint, missing affordance, or seam than the direct/proximal challenge.

## Codex reconciliation

For every Claude challenge, Codex must classify it as:

- **Accepted** — name the exact artifact section/file changed.
- **Risk added** — name the specific risk, assumption, test, or proof gap added.
- **Rejected** — cite evidence or a scope boundary. Scope-boundary rejections must state what evidence, approval, or changed scope would bring the challenge in scope.
- **Uncertain** — carry it into Known Risks, Acceptance Gaps, or RCA alternatives.
- **No material impact** — state that Claude found no actionable issue and that the round must not count as independent acceptance evidence.

`No material impact` / no-impact Claude review is non-evidence: it is a receipt that a review ran, not proof that the artifact is acceptable.

When a Claude round is itself used as proof that the adversary workflow works, an all-`No material impact` round is non-evidence and cannot satisfy the proof gate. The proof must show a specific artifact change, risk/test added, or challenge rejected with evidence.

## Staleness and receipts

- Bind each ledger to the artifact path, version, commit, section, or timestamp reviewed.
- A material edit is any edit that changes meaning, scope, or constraint of a named section. Whitespace, formatting, and comment-only edits are non-material.
- Material edits to challenged sections make the relevant challenge stale; rerun Claude or mark the stale challenge explicitly.
- A receipt is reproducible only if a skeptic can inspect deterministic command output, logs, diffs, or saved Claude prompt/output without trusting model prose alone.

## Exact skill questions

Use the skill-specific questions below as the hot path. Each answer must include causal layer, evidence, and minimum impact.

### ubergoal

1. **Load-bearing goal?** Is this goal actually load-bearing, or a routing artifact?
2. **Skip test.** What is lost if we skip the goal wrapper and execute directly?
3. **Testable decomposition.** Does this decompose into three or fewer testable sub-outcomes?

### uberplan

1. **Most likely execution failure.** Name the single most likely execution failure and its mitigation, not just acknowledgment.
2. **Missing affordance.** What skill, tool, source, or context does this plan depend on that does not exist or is unproven?
3. **Linear 80/50 alternative.** Is there a linear no-branch version that gets at least 80% of the value with at most 50% of the surface?

### uberrca

1. **Falsification experiment.** What experiment would falsify the identified root cause, and has it been run?
2. **Competing cause.** Name one alternative cause with equal explanatory power and state why it was ruled out.
3. **Model-blame audit.** Is “the model just failed” anywhere in the causal chain? If yes, replace it with the missing context/tool/feedback/source/invariant or mark mitigation-only.

### uberassess

1. **Source-lane sufficiency.** Did assessment consult the relevant source lane, or stop at the first confirming source?
2. **Actionability boundary.** Is the recommendation directly actionable by the agent, or does it require human escalation?
3. **90-day falsifier.** What would change this recommendation in 90 days?

### uberaccept

1. **Receipt reproducibility.** Are receipts reproducible by deterministic tool output, or are they model summaries?
2. **Scope/diff match.** Does the diff match stated scope? Name any out-of-scope change.
3. **Inherited assumption.** What assumption does the next task inherit that could be wrong?

`uberaccept` also has a separate final gate: **Ship: yes/no, one sentence.** That gate is not one of the three questions.
