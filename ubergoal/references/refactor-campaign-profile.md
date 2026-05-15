# Refactor Campaign Profile

Use this profile when the user asks for a refactor campaign, codebase health campaign, HOT-file audit, nightly refactor, or similar. The user should not have to paste the detailed checklist.

## Default prompt expansion

Treat the request as:

```text
Use $ubergoal to run a Tier 2 codebase health/refactor campaign on this repo.

Goal: identify and safely reduce coding-agent drift: HOT/blob files, overengineering, ad hoc regex over structured data, dead code, weak tests/evals, missing code review coverage, and poor module seams.

Start in audit/plan mode. Do not patch unless patch mode is explicitly authorized. Produce:
1. HOT files ranked by risk and why
2. code review findings ordered by severity
3. simplification/dead-code/modularity candidates
4. regex/structured-data misuse findings
5. missing tests/evals and which ones should be written first
6. the smallest safe patch batches with proof requirements
7. a tight generated HTML refactor report for human review
8. an updated project-local refactor history

Route simplification analysis through $ubersimplify and final readiness through $uberaccept.
```

## Required lanes

- **Codebase/State Scout:** branch, dirty state, generated/vendor noise, recent churn, high-collision files.
- **Architecture/Seam Steward:** blob files, module seams, ownership, public/private boundaries.
- **KISS/Simplifier:** overengineering, wrapper chains, duplicate policy, dead code, simpler alternatives.
- **Code Review/Loophole Hunter:** likely bugs, silent fallbacks, error handling, security/privacy, concurrency, rollback risk.
- **Quality/Eval Auditor:** tests/evals present, tests/evals missing, commands run, proof gaps.
- **Regex/Structured-Data Auditor:** regex/manual parsing where parser/schema/API should own the format.

Use subagents for Tier 2+ when available; if not, run the lanes sequentially and say the review-board mode was degraded.

## Output contract

Lead with the verdict and findings:

1. overall risk verdict and recommended next batch
2. HOT files table: file, evidence, risk, recommended action, proof needed
3. findings ordered by severity with file/line evidence where possible
4. simplification/dead-code/modularity candidates
5. regex/structured-data findings
6. missing tests/evals and commands to run
7. patch batches: smallest safe edit, required proof, rollback
8. HTML report path and refactor-history path
9. residual risks and what should become learning/evals

## HTML report

Produce a tight generated HTML report for each durable run unless the user explicitly says no artifacts. Prefer `$ubershow` when available; otherwise create a self-contained static HTML file in a generated-report location.

The report should be decision-oriented, not a transcript. Include:

- one-screen executive verdict
- attention map: HOT files, risky seams, brittle regex/parsing, weak tests/evals
- key things changed in this run, if patch mode was authorized
- key things deliberately not changed and why
- next patch batch recommendation
- links/paths to the markdown findings, tests, evals, and refactor history

Default target path:

```text
<repo>/runtime/reports/refactor-campaign/YYYY-MM-DD-refactor-report.html
```

If the repo has an established generated-report directory, use that instead. Do not put generated HTML in canonical docs unless the repo convention says to.

## Refactor history

Maintain a small project-local history so repeat campaigns every few days do not start cold. Read it at the beginning of each run and update it at the end when artifacts are allowed.

Default target path:

```text
<repo>/coordination/refactor-history.md
```

If the project already has a coordination/status area, place it there. If not, create the default path only when writing artifacts is allowed.

History entries should be compact:

- date, agent/session, branch/commit range, and mode
- HTML report path
- HOT files still hot, newly hot, and cooled down
- key refactors/tests/evals added
- decisions and no-change rationale
- deferred candidates and proof needed
- hazards for the next run: fragile tests, dynamic references, local dirty-state notes

Do not let history become a second source of truth for code behavior. It is a navigation aid and decision log; current code, tests, and docs remain authoritative.

## Patch policy

Default is audit/plan only. Patch only when the user or automation profile explicitly authorizes patch mode.

Before patching:

- repo state is understood and unrelated dirty changes are protected
- baseline checks are run or explicitly recorded as too expensive/unavailable
- behavior-changing refactors have characterization tests or strong existing coverage
- grep-only dead-code evidence is not enough for deletion
- structured formats use parsers/schemas/APIs where available
- each batch has rollback and post-patch checks

After patching, use `$uberaccept` before claiming completion.
