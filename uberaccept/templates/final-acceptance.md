# Final Acceptance Report

## Implementation summary


## Files changed

-

## Scope fidelity verdict

This section must appear before any `SHIP`, completion, ready, or goal-complete language. Quote or link the durable scope artifact, not only the plan summary.

- Scope artifact: `coordination/<task-slug>/scope.md`
- Original scope: quote or link to `scope.md` Operator original instruction
- Implemented scope:
- Does implemented scope satisfy original scope? yes/no/partial
- Narrowing? yes/no
- Operator approved narrowing in: quote/link required if narrowed
- Approval evidence for narrowing/deferral: quote/link or n/a
- Explicit constraints and later user scope changes checked: yes/no
- Unapproved narrowing blocker? yes/no
- Scope fidelity verdict: pass / fail / uncertain

## Rubric scores

Use 0 = blocker, 1 = weak/unresolved, 2 = acceptable with named residual risk, 3 = strong evidence.

| Dimension | Score | Evidence | Residual gap |
|---|---:|---|---|
| Scope clarity |  |  |  |
| Scope fidelity against operator-original instruction |  | Operator original instruction, proposed scope, deferrals, approval evidence, and actual diff compared |  |
| Acceptance criteria verification |  | every micro-intent/work-contract/PRD/plan acceptance criterion mapped to pass/fail/partial with evidence |  |
| Spec fidelity vs repo standards |  | originating spec/PRD/issue/operator request checked separately from documented project standards and conventions |  |
| Requirement-to-evidence ledger |  | every material requirement mapped to proved/weak/missing/contradicted with evidence |  |
| Planning review board |  | board findings reconciled |  |
| User expectation / surprise delta |  | expected user outcome compared against actual implementation and gaps |  |
| Claim-language / operational outcome |  | implemented/operational/live/adopted/proof-only/blocked/shadow-only language checked against the Operational Outcome Contract |  |
| Production implementation blocker gate |  | active blockers vs hard-blocked-after-safe-action-exhaustion checked; no runnable safe next actions remain before parent completion |  |
| Safe-work exhaustion adversarial review |  | every blocked child inspected for plausible safe next actions; parent completion blocked if any runnable safe action remains |  |
| Runtime agent topology |  | max_threads/max_depth, role shape, depth-3 approval/restore, and child-agent depth policy checked for campaign/subagent work |  |
| Cost/complexity |  | smallest useful guardrail; deferred machinery named |  |
| Agent Advocate / Agent RCA |  | failed invariant, human counterfactual, human-parity fix, and recurrence evidence |  |
| Architecture Steward |  | planning/final steward report |  |
| Architecture |  |  |  |
| Repository topology |  | package/dependency gate evidence for new/moved code files |  |
| Ownership |  |  |  |
| Code quality |  |  |  |
| Dead code |  |  |  |
| Unit/regression tests |  |  |  |
| Integration tests |  |  |  |
| UI/browser tests |  |  |  |
| Evals |  |  |  |
| Safety |  |  |  |
| Observability |  |  |  |
| Rollback/adoption |  |  |  |
| Budget/backpressure/fallback |  |  |  |
| Acceptance evidence |  |  |  |

## Commands and artifacts

| Layer | Command/artifact | Result |
|---|---|---|
|  |  |  |

## Acceptance criteria verification

Required when the task used a micro-intent, work contract, PRD, ticket, or plan acceptance criteria. Otherwise state why not applicable.

- Acceptance criteria source:
- Any criteria omitted from verification? yes/no, explain:
- Any failed criteria? yes/no, explain:
- Any partial criteria? yes/no, residual risk and owner:
- Spec/intent review vs code review split checked? yes/no, explain:
- AC verification verdict:

| Acceptance criterion | Status: pass / fail / partial / n/a | Evidence: file path, command, artifact, or reason | Residual risk / follow-up owner |
|---|---|---|---|
|  |  |  |  |

## Spec fidelity and standards review

Required when implemented work had an originating spec, issue, PRD, work contract, or explicit user request. Keep these axes separate; do not collapse them into one generic review verdict.

- Spec source: path, issue, PRD, scope artifact, or none found:
- Standards sources inspected: paths or none found:
- Spec fidelity verdict: pass / fail / partial / skipped, why:
- Repo standards verdict: pass / fail / partial / skipped, why:
- If spec source missing, standards-only review not treated as product correctness? yes/no/n/a:
- Unapproved scope creep found? yes/no, explain:

| Axis | Status: pass / fail / partial / skipped | Evidence | Blocker or residual risk |
|---|---|---|---|
| Spec fidelity |  |  |  |
| Repo standards |  |  |  |

## Requirement-to-evidence ledger

Use this as the short truth table for the final claim. Include user instructions, plan/work-contract requirements, PRD/ticket requirements, review-board blockers, and material later corrections.

| Requirement | Evidence: command, artifact, diff, eval, replay, or reason n/a | Status: proved / weak / missing / contradicted | False-green risk checked? | Residual risk / owner |
|---|---|---|---|---|
|  |  |  |  |  |

## Red/green and black-box proof ledger audit

- Baseline command/result before change:
- Expected red/failing fixture or regression before fix, if applicable:
- First green proof after change:
- Black-box/user-visible proof:
- False-green risks checked:
- Skipped evidence layers and accepted/deferred rationale:
- Ledger verdict: pass / blocker / residual risk accepted by user

## Runtime agent topology acceptance

Required for campaign, multi-agent, subagent, or plan-tree work; otherwise state why it is not applicable.

- Config source / observed source:
- Topology mode:
- Current `max_threads`:
- Current `max_depth`:
- Role shape:
- Depth-3 escalation used? yes/no/n/a, why:
- User approval evidence for depth/thread escalation:
- Restore target:
- Restore proof / blocker:
- Child-agent depth policy:
- Topology acceptance verdict:

## Tier 3 expensive-proof acceptance

Required when the work involved Tier 3 agentic/runtime/production-replacement expensive proof, burn-in, soak, canary expansion, or final proof; otherwise state why it is not applicable.

- Expensive-proof scope applies? yes/no, why:
- Plan validator command/result:
- Risk/failure-class inventory inspected:
- Observability / telemetry preflight evidence:
- Phase-boundary / contract-fuzz preflight evidence:
- Burn-in vs final-proof separation evidence:
- Stop/replan evidence:
- Child-plan/status-ledger evidence:
- Flat-plan exception / bypass approval:
- Expensive-proof acceptance verdict:

## Production implementation blocker gate

Required when accepting a production/runtime implementation goal, long unattended production goal, or goal with external/irreversible stop points; otherwise state why it is not applicable. A child that is blocked but still has runnable safe next actions is active work, not completion.

- Production implementation goal? yes/no, why:
- Upfront approval packet status:
- Required child count:
- Operational or user-rescoped child count:
- Hard-blocked-after-safe-action-exhaustion child count:
- Active blocked child count:
- Runnable safe next action count:
- Safe autonomous predecessor work exhausted? yes/no/n/a, evidence:
- Parent completion allowed? yes/no, why:
- Next safe action if parent completion is not allowed:

| Child ID | Required? | Classification: operational / re_scoped_with_approval / hard_blocked_after_safe_action_exhaustion / active_blocked | Runnable safe next actions? | Safe predecessor exhaustion evidence | Exact external/unsafe blocker | Next unblock owner/action |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

## Safe-work exhaustion adversarial review

Required when accepting a production/runtime implementation goal, long unattended production goal, or goal with external/irreversible stop points. This is the semantic oversight pass: list every blocked child, enumerate plausible safe actions an autonomous agent could still take, and block parent completion if any safe action remains runnable.

- Review scope applies? yes/no, why:
- Blocked children inspected:
- Plausible safe next actions enumerated? yes/no, evidence:
- Any runnable safe next action found? yes/no, explain:
- If runnable safe action found, parent completion blocked? yes/no/n/a:
- Reviewer conclusion:

| Blocked child | Plausible safe next action considered | Evidence action is exhausted / not safe / not applicable | Reviewer verdict: exhausted / not safe / none / runnable_safe_action_remains | Follow-up / owner |
|---|---|---|---|---|
|  |  |  |  |  |

## Loop acceptance lens

Required for recurring, scheduled, watch-and-fix, event-triggered, queue-driven, or unattended work. Otherwise state why not applicable. Use `references/loop-engineering.md` for the shared lens.

- Loop scope applies? yes/no, why:
- Loop Contract source:
- Per-iteration receipts or sampled receipt set inspected:
- Independent verifier / gate, not maker-only self-review:
- Correct-stop proof for complete / no-work / blocked / exhausted / approval-needed:
- Durable state replay proof:
- No-progress detection evidence:
- Budget/time/retry kill-switch evidence:
- Idempotent side effects and duplicate suppression evidence:
- Human approval before irreversible actions:
- Attention/noise policy followed:
- Comprehension-debt spot-check performed or deferred with owner:
- Loop acceptance verdict: pass / fail / residual risk accepted:

| Iteration / sample | Trigger | Work discovered | Verification evidence | State written | Stop/continue decision | Gap |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

## Claim-state ledger

Check that the final report does not blur `implemented`, `operational`, `live`, `adopted`, `tested`, `ready`, `wired`, `proof-only`, `blocked`, or `shadow-only`.

- Operational Outcome Contract source:
- Highest state claimed in final handoff:
- Highest state actually proven:
- Any lower-state child limiting parent completion:
- Wording that must be avoided in final handoff:
- Proof-only / shadow-only / local-safe-proof / shared-spine evidence claimed as operational? yes/no, explain:
- Multi-child goal? yes/no, child rows below or not applicable because:
- Plan tree artifacts inspected, if applicable: root index, status ledger, child plans, receipts, final acceptance receipt:

| Workstream/child | Target state | Accepted state | Evidence / proof | Gap / blocker / re-scope approval |
|---|---|---|---|---|
|  |  |  |  |  |

## Review independence ledger

Same-agent review can be useful, but it is not independent evidence. Record every review lane before acceptance.

| Round | Artifact reviewed | Author identity/model/runtime | Reviewer identity/model/runtime | Fresh context? | Cross-model? | independent_review true/false | Material edits after review? | Receipt path |
|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |  |

- Any same-agent review counted as independent evidence? yes/no; if yes, blocker.
- Any requested reviewer unavailable or waived by operator? yes/no; evidence:
- Review independence verdict: pass / fail / residual risk accepted

## Planning review reconciliation

Confirm every material planning-board blocker was resolved, explicitly deferred with user acceptance, or converted into a known residual risk.

## User expectation / surprise delta

Compare what the user likely expected against what was actually implemented or accepted. Ground this in the request, known preferences, plan, and evidence; do not claim to read the user's mind.

- Expected outcome inferred before/during plan:
- Evidence for expectation:
- Actual implementation/result:
- Differences or surprises:
- Material mismatch requiring user approval:
- Final handoff wording:

## Agent Advocate final check

For agent behavior or multi-agent changes, confirm the final implementation fixes the upstream reason the agent erred: context, tool affordance/output, source authority, memory, feedback, state/admission, handoff, stop condition, eval, or guard. Confirm the human counterfactual was answered and any human-parity gap was fixed or explicitly accepted. State why this is not just a symptom patch.

## Agent Boundary Contract final check

For agentic/tool/memory/subagent/external-action changes, confirm every model-output boundary has shape, authority, isolation, failure semantics, observability, and replay/eval evidence. Name only relevant sentinel probes: wrong-shaped identifiers, swallowed errors, ambiguity/no ask path, shared mutable state, untrusted memory/context, unbounded loop, privileged action, parent-context dump, or missing trace propagation.

## Regex / keyword semantic gate final check

For agentic-system changes and any changed regex/keyword/string-matcher logic, confirm every use was classified as mechanical syntax, candidate signal, or semantic authority. Confirm no regex/keyword/string matcher has unapproved semantic authority over natural language. If there is an exception, name the approval, eval/replay coverage, observability, and rollback.

## Architecture Steward final check

Confirm the implementation still matches the architecture plan, relevant guide sections, and harness/policy split. List blocker and non-blocker findings.

## Adversarial acceptance check

Try to prove this work is not ready. List every material issue found.

## Post-run learning / Uberskillevolver

For Tier 2/3 skill, prompt, workflow, multi-agent protocol, or agentic-system changes, record whether `uberskillevolver` was used or why it was not needed. Link the post-run learning record and list promoted/deferred/no-change lessons.

## Confidence verdict

```text
Final confidence verdict:
- 100% confident within scope? yes/no
- Scope accepted:
- Material blockers:
- Non-blocking residual risks:
- Explicitly accepted gaps:
- Goal completion recommendation:
```
