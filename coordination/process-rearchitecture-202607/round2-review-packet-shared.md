# Round 2 Adversarial Review Packet — shared core

Round 2 of 2 (operator-budgeted). Round 1: both adversaries returned MAJOR_CHANGES_REQUIRED; the judge merged 18 raw challenges into 19 ordered changes (`round1-judgment.md`); the orchestrator accepted all 19 and produced `plan-v3.md` + `failure-catalog.md` v2 (20 cases). Round 2 reviews THE REVISION, not the history.

## Frame

Same adversarial discipline as round 1: operator-original instructions (in `scope.md`) are the supreme authority; state role acceptance + 3 reject conditions before assessing; an all-clear review with no genuine attempt to break the revision is review failure. **Do NOT re-litigate round-1 grades or rulings the judge settled** — challenge a ruling only if (a) plan-v3 implements it incorrectly or nominally ("renamed, not resolved"), or (b) the implementation of one ruling creates a new problem elsewhere.

## Artifacts

Read in order:
1. `scope.md` — operator instructions + approvals (supreme authority)
2. `plan-v3.md` — THE ARTIFACT UNDER REVIEW
3. `round1-judgment.md` — the 19 changes v3 claims to implement (sections A and E)
4. `failure-catalog.md` — v2, 20 cases with judge-final verdicts
5. For context/diff only: `plan-v2.md`, `round1-fable-review.md`, `round1-codex-review.md`

Verify claims against the repos where a quick check settles them (same roots as round 1). Do not modify anything (Fable reviewer: except writing your own review file).

## Required output (markdown, ≤2,000 words)

1. **Role statement** — acceptance + 3 reject conditions for THIS round (revision-specific).
2. **Resolution audit** — a 19-row table: judgment change # · RESOLVED / PARTIAL / NOT-RESOLVED / RESOLVED-BUT-BREAKS-X · one-line evidence citation from plan-v3 (section/quote). Be strict: a change is RESOLVED only if v3 binds it (names the mechanism/fixture/owner), not if it re-states the intent.
3. **New challenges (max 5, same format as round 1: Claim / Causal layer / Why / Evidence / Minimum impact)** — genuinely new issues introduced or exposed by v3. Quality over quantity; zero is acceptable ONLY with a stated search path (what you looked for and didn't find).
4. **Catalog v2 check** — schema v2 sound? canonical_layer + shared-id fingerprint coherent? any of the 20 cases mis-mapped to plan items? case-20 dogfood legitimate?
5. **Final line:** `VERDICT: MAJOR_CHANGES_REQUIRED` | `VERDICT: MINOR_CHANGES_ONLY` | `VERDICT: ACCEPT` + one line. MAJOR = structural/sequencing/scope/safety change still required before implementation. MINOR = implementation may start; listed fixes fold into Wave-1 execution. ACCEPT = proceed as written.
