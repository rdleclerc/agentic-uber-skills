# Wave 2 — Dispatch 1: R7 canonical tier ladder + precedence (gaia spine side)

You are Codex, implementer. You are in a clean WORKTREE of agfunder-gaia on `main`. NO git commands. Touch ONLY: `knowledge/coding-agent-operating-spine.md` and `AGENTS.md`. This is Tier-2 cross-repo doctrine work; your diff gets an exact-diff review + the wave's independent adversarial lane.

Authority: plan-v3.1 §Governance (in `${UBER_SKILLS_ROOT:-~/repos/agentic-uber-skills}/coordination/process-rearchitecture-202607/plan-v3.md`) + round1-judgment #2/#4. Read the CURRENT spine fully first — you are REPLACING its one-size review rule with the risk-tiered ladder while preserving every non-negotiable.

## 1. knowledge/coding-agent-operating-spine.md

Locate the current review-gate section (the one mandating the 4 review phases — orchestration/plan review, exact-diff review, adversarial review, acceptance review — for everything beyond minor edits). Replace it with the canonical risk-tiered ladder, preserving these invariants VERBATIM-in-spirit: no implementing agent self-approves at Tier ≥1; review receipts record command/model/diff-identity/verdict; stop-if-no-Claude-lane-reachable rule; the existing lane policy (spine owns it) stays.

The canonical ladder (this exact table + riders; it will be drift-fingerprinted, so keep the wording tight):

```
## Review ladder (canonical — pack skills and all coding agents point here)

| Tier | Work class | Required review |
|---|---|---|
| 0 | typo/cosmetic only — nothing that fixes observed misbehavior | none; commit carries a `tier0:` trailer |
| 1 | contained single-surface change, clear tests | one exact-diff review pass by a capable lane, including a one-line scope echo against the operator-original ask |
| 2 | cross-repo doctrine/pointer edits; behavior surfaces (prompts/skills/evals); medium-risk code | exact-diff review + independent adversarial lane (different vendor or fresh context) + scope-fidelity verdict |
| 3 | production/runtime services; live-injected context surfaces; provider routing; security/data-subject surfaces; major refactor/deletion | full 4-phase ladder (plan review, exact-diff, adversarial, acceptance) on the highest-capability Claude lane + review-board lanes |

Riders: any surface injected into live OpenClaw session context additionally takes the GAIA_TESTING live-proof gate (those are runtime behavior changes, not doc edits). Tier assignment is auditable: every receipt records `tier` + a one-line justification; a reviewer's FIRST check is tier correctness, with bounce authority. If uncertain between tiers, take the higher.
```

Then add the precedence paragraph (drift-fingerprinted; identical sentence lands in the pack's AGENTS.md):

```
Precedence with the Uber skill pack: `ubergoal` wraps this spine's lifecycle for gaia work; the uber run receipt satisfies the spine receipt contract; `uberaccept` is the acceptance review; the claude-adversary lane is the required Tier-2+ independent lane and stays opt-in below Tier 2.
```

Integrate cleanly: delete the superseded 4-phases-for-everything wording (the ladder's Tier 3 row now carries it), keep the receipt/waiver/no-self-approval prose, and do NOT expand the document — target net word growth ≤ +60 words (you are replacing, not appending). Report exact before/after word counts.

## 2. AGENTS.md (gaia repo)

In its review-timing/lane section, replace any restatement of the old 4-phase-for-everything rule with: one pointer line to the spine ladder + the SAME precedence paragraph verbatim. Net delta should be negative or ~zero. Do not touch the Host Capability Map or other unique content.

## Wrap-up

Print: unified diffs of both files, before/after word counts, and confirmation that the strings "Review ladder (canonical" and "Precedence with the Uber skill pack:" appear exactly once each per file where required. FLAG (do not resolve) anything in the spine that contradicts the ladder and isn't covered by the instructions above.
