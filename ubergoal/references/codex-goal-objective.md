# Codex Goal Objective Guidance

Use this when converting a hardened plan into a Codex goal objective.

## Principle

The goal objective is an operating contract, not the whole plan. Keep the detailed plan in an artifact or in the thread, and make the goal compact enough for Codex continuations to preserve.

## Compact shape

Use this shape by default:

- Destination: what must be true at the end.
- Starting point: repo, branch, artifact, known state, or plan path.
- Objective/scope: concrete work and boundaries.
- Preserve: constraints, non-regression behavior, approval boundaries.
- Verification: commands, tests, evals, screenshots, reviews, or artifacts.
- Done/stop: completion criteria and reasons to pause/ask.
- Success metric: observable result that proves completion.

## Length and budget

- Hard limit: 3,999 objective characters after stripping a leading `/goal`.
- Target: 3,400 objective characters or fewer.
- Treat 3,800+ as a failed draft and compress.
- Do not put token-budget flags inside slash text; pass budgets only through a supported separate field/tool when the user explicitly gave one.

## Compression rules

- Merge deliverables into Objective/scope.
- Merge must-not-regress into Preserve.
- Merge checkpoint rhythm and autonomy rules into Done/stop.
- Keep examples and candidate lists outside the goal unless they are essential constraints.
- Include exact commands only when known from the repo or the user.
