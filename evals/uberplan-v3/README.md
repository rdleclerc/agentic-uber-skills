# UberPlan Behavioral Conformance Suite v1

Stable suite ID: `uberplan-behavioral-conformance-v1`

This is the durable, model-agnostic regression suite for UberPlan behavior. It
tests whether a planning agent reads decisive sources, finds the minimum
complete change, preserves every material causal and safety layer, stops
honestly when authority is missing, and avoids unrelated architecture or
process theater.

The `uberplan-v3` directory name records the candidate lineage. Use the stable
suite ID in new run receipts and cross-model comparisons.

## Corpus

- `working-inputs.json` and `working-rubric.hidden.json`: known cases used while
  improving the skill.
- `holdout-inputs.json` and `holdout-rubric.hidden.json`: promotion cases frozen
  before an iteration and run only after the working set is substantively
  green.
- `forward-inputs.json` and `forward-rubric.hidden.json`: retained safety cases
  for agent/model ownership, new unattended loops, and external writes.
- `fixtures/`: self-contained repositories for each user-style request.
- `baselines/`: compact, sanitized comparison receipts. Raw outputs and traces
  stay under `.uberlearn-local/` and are not committed.

`suite.json` is the machine-readable index.

## Run protocol

1. Record the candidate skill hash, model and exact version, reasoning effort,
   runtime/tool configuration, and date.
2. Build the subject bundle from the explicit `suite.json` allowlist. Give each
   subject a fresh context containing the governing pack files, candidate skill
   package, required shared references, one case's `user_prompt`, and a
   disposable copy of only that case's fixture.
3. Do not expose rubrics, sibling cases, earlier outputs, grader reports, or the
   champion diagnosis to the subject.
4. Save the final answer and process trace. The trace must reveal source reads,
   tool calls, failures, and stop behavior.
5. Grade in a separate fresh context using the case rubric, output, and trace.
6. Run holdouts only after the working cases pass every substantive gate.
7. Run the forward safety group before promotion.

This protocol is adapter-neutral. A GPT, Claude, or future-model runner may use
different commands, but it must preserve the isolation and receipt contract.

## Promotion contract

Every case must pass its substantive dimensions: decision quality, causal or
protection completeness, scope control, and source reading. Lower cost never
compensates for shallower reasoning.

Report output words, total tokens, and completed tool calls per case and in
aggregate when the runtime exposes them. `suite.json` defines the counting
method. Compare token and call counts only between runs with compatible
accounting. A focused per-case call increase is diagnostic, not independently
disqualifying; it becomes a blocker when it reflects broader, irrelevant, or
shallower behavior. Prefer material aggregate cost improvement.

Word targets are pressure against verbosity, not permission to omit a material
causal or safety layer.

## Extending the suite

Add a case only for a distinct recurring failure class. Keep fixtures small,
use positive and negative behavior, name forbidden shortcuts, and add the case
to the input file, hidden rubric, manifest, and boundary tests together. Do not
rewrite existing cases to make a favored model pass; create a new suite version
when the behavioral contract itself changes.
