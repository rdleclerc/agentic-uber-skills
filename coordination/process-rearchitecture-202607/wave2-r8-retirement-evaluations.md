# Wave 2 R8 Retirement Evaluations

Scope: evidence and recommendation only. No skills were uninstalled, archived, or edited as part of this evaluation. Operator decides any archive action at Wave 2 acceptance.

Contract for staying installed: (a) named owner, (b) a real triggering task class observed in coordination history, and (c) an eval that would exercise it within a month.

Archiving means: uninstall the skill from both `~/.codex/skills/<skill>` and `~/.claude/skills/<skill>`, add a README tombstone that says the skill is archived and why, and restore by recreating the symlink from this git checkout. The skill directory stays in git.

## Summary

| Skill | Owner | Observed task class | Within-month eval | Recommendation |
|---|---|---|---|---|
| `ubersimplify` | pass: pack maintainer/operator via `AGENTS.md` and ROADMAP dogfooding lane | pass: Gaia dirty-tree simplification audit trail | pass: local golden invocations and report validator can exercise Audit/Plan/Patch guards | keep-slimmed |
| `ubershow` | pass: pack maintainer/operator via `AGENTS.md` and ROADMAP dogfooding lane | pass: real decision board plus sibling operator-registered receipt found by content marker | pass: local golden invocations and pattern-kit tests can exercise it | keep-slimmed |
| `uberarchitect` | pass: pack maintainer/operator via `AGENTS.md` and ROADMAP dogfooding lane | pass: two recent Gaia Architecture Stepback Packets | pass: golden routing examples and packet-template tests can exercise it | keep |

## Ubersimplify

Evidence found:

- `/Users/rob/repos/agfunder-gaia/coordination/gaia-architecture-quality-audit/ubersimplify-runs/20260511T154528Z-gaia-dirty-tree-convergence/final-simplification-report.md`
- `/Users/rob/repos/agfunder-gaia/coordination/gaia-architecture-quality-audit/ubersimplify-runs/20260511T154528Z-gaia-dirty-tree-convergence/simplification-candidates.md`
- `/Users/rob/repos/agfunder-gaia/coordination/gaia-architecture-quality-audit/ubersimplify-runs/20260511T154528Z-gaia-dirty-tree-convergence/simplify-plan.md`
- `/Users/rob/repos/agfunder-gaia/coordination/gaia-architecture-quality-audit/ubersimplify-runs/20260511T154528Z-gaia-dirty-tree-convergence/complexity-inventory.md`
- `/Users/rob/repos/agfunder-gaia/coordination/gaia-architecture-quality-audit/ubersimplify-runs/20260511T154528Z-gaia-dirty-tree-convergence/modularity-audit.md`
- `/Users/rob/repos/agfunder-gaia/coordination/gaia-architecture-quality-audit/ubersimplify-runs/20260511T154528Z-gaia-dirty-tree-convergence/dead-code-audit.md`
- `/Users/rob/repos/agfunder-gaia/coordination/gaia-architecture-quality-audit/ubersimplify-runs/20260511T154528Z-gaia-dirty-tree-convergence/test-confidence.md`
- `/Users/rob/repos/agfunder-gaia/coordination/gaia-architecture-quality-audit/ubersimplify-runs/20260511T154528Z-gaia-dirty-tree-convergence/patch-log.md`
- `ROADMAP.md#ubersimplify-dogfooding`: Audit mode first; Patch mode remains conservative/experimental; retire/demote if it adds ceremony without safe net-deletion/refactor wins.
- `ubersimplify/evals/golden_skill_invocations.json`: Audit default, weak-test deletion block, agentic complexity, patch authorization, and lossless skill-plan compression cases.

Contract verdict:

| Requirement | Verdict | Evidence |
|---|---|---|
| named owner | pass | Pack maintainer/operator ownership is implied by `AGENTS.md` install policy and ROADMAP dogfooding lane. No separate named human owner is encoded. |
| observed task class | pass | Gaia dirty-tree convergence and refactor/deletion candidate ranking produced a full ubersimplify audit trail. |
| eval within a month | pass | Existing golden examples plus `validate_simplify_report.py` and ubersimplify tests can exercise the same Audit/Plan/Patch guardrails within a month. |

Recommendation: keep-slimmed.

Rationale: plan-v3 said ubersimplify had no real-usage artifacts, but the evidence sweep found a full Gaia audit trail. It also found that the useful observed mode was Audit/Plan, not broad Patch autonomy. Keep the skill, but slim the active SKILL.md by moving the detailed gate explanations and test-confidence table into references while preserving the trigger, Audit default, Patch authorization boundary, and output contract.

Specific sections to cut or move if slimmed: `Required gates` detailed bullets to references; `Modularity stance` examples to `references/modularity-principles.md`; `Test-confidence policy` table to `references/test-confidence.md`; `Parallel simplification` into a short pointer. Keep `Core rule`, `Modes`, `Output contract`, and the relationship/resource list.

Archiving would mean removing symlinks from both runtime roots, tombstoning README, and restoring by symlink. I do not recommend archiving in this wave unless the operator rejects the 2026-05-11 audit as insufficiently current for the contract.

## Ubershow

Evidence found:

- `/Users/rob/repos/agfunder-gaia/coordination/gaia-brain-wisdom-event-graph-activegraph/p0-wisdom-grading-board-2026-05-31.html`: read-only verified content marker `data-artifact-kind="ubershow-decision-board"`.
- `/Users/rob/repos/agfunder-gaia/coordination/gaia-brain-wisdom-event-graph-activegraph/p0-wisdom-grading-board-2026-05-31-receipt.md`: read-only verified sibling receipt with `registration_status: registered_from_user_paste_2026-05-31` and `selected_decision: proceed_to_p1_minimal_candidate_design`.
- Earlier directory-convention sweep found no files under `/Users/rob/repos/agfunder-gaia/coordination/**/ubershow/`, but that absence is not decisive because the real board lived beside its task artifacts.
- Pack-side evidence is limited to templates, tests, and quality-review artifacts: `ubershow/templates/*.html`, `ubershow/evals/golden_skill_invocations.json`, `reviews/uberskills-20260620/*`, and `coordination/integration-uberskills-20260620/*`.
- `ROADMAP.md#ubershow-dogfooding`: use only when it materially increases decision speed or comprehension; retire if visual artifacts become decorative ceremony.

Contract verdict:

| Requirement | Verdict | Evidence |
|---|---|---|
| named owner | pass | Pack maintainer/operator ownership is implied by `AGENTS.md` install policy and ROADMAP dogfooding lane. No separate named human owner is encoded. |
| observed task class | pass | The Gaia wisdom grading board is a real ubershow decision board with a sibling receipt registered from operator paste. |
| eval within a month | pass | Existing golden invocation and pattern-kit tests can exercise trigger/de-escalation and receipt shape. |

Recommendation: keep-slimmed.

Rationale: ubershow has a coherent local package, eval shape, and at least one real operator-registered decision artifact. It should stay installed, but the active skill can still be slimmer: move pattern-kit walkthrough details into references, preserve the core rule, receipt contract, source-authority rule, and trigger/de-escalation guidance.

Candidate cuts if slimmed: move pattern-kit walkthroughs and template-selection examples to references; keep `Core rule`, `Decision registration`, `Source authority`, trigger/skip lists, output-mode table, and quality-check/receipt requirements.

Correction history: the original sweep searched by directory convention and was falsified by content-marker search; this is case-20's third observed unverified-baseline instance.

## Uberarchitect

Evidence found:

- `/Users/rob/repos/agfunder-gaia/coordination/codex-native-tool-recovery-2026-06-30/architecture-stepback.md`
- `/Users/rob/repos/agfunder-gaia/coordination/gaia-gmail-nonresponse-uberrca-2026-07-02/architecture-stepback.md`
- `coordination/process-rearchitecture-202607/round1-judgment.md`: confirms both packets as genuine Architecture Stepback Packets and corrects the prior zero-usage assumption.
- `coordination/process-rearchitecture-202607/round1-fable-review.md`: cites the same two packets as counter-evidence against retirement-by-word-count.
- `ROADMAP.md#uberarchitect-dogfooding`: admitted only if tests and fresh-agent fixtures prove it catches system-scale queue/worker/backpressure failures without turning ordinary edits into process theater.
- `uberarchitect/evals/golden_skill_invocations.json`: triggers for gateway concurrency and repeated blocked-pipeline timeouts; non-triggers for typo fixes and settled local bugs.

Contract verdict:

| Requirement | Verdict | Evidence |
|---|---|---|
| named owner | pass | Pack maintainer/operator ownership is implied by `AGENTS.md` install policy and ROADMAP dogfooding lane. No separate named human owner is encoded. |
| observed task class | pass | Two recent Gaia architecture-shaped incidents produced durable stepback packets. |
| eval within a month | pass | Golden routing examples and `uberarchitect/tests/test_uberarchitect_contract.py` exercise trigger/non-trigger and packet shape. |

Recommendation: keep.

Rationale: uberarchitect is the cleanest keep case: it has two recent real packets, a narrowly described trigger, and package tests/evals that can exercise the gate soon. Its current SKILL.md is already small enough that slimming would risk deleting useful packet shape more than reducing ceremony.

Archiving would mean removing symlinks from both runtime roots, tombstoning README, and restoring by symlink. I do not recommend archiving or slimming in this wave.

## Contradictions Flagged

- plan-v3 says `ubersimplify` and `ubershow` remain without real-usage artifacts. The sweep contradicts that for `ubersimplify`, and the content-marker correction contradicts it for `ubershow`.
- `AGENTS.md` says all pack skills must be installed and exposed, while R8 allows archiving skills after operator approval. This is not an implementation blocker because this dispatch is evidence/recommendation only; if the operator accepts an archive, `AGENTS.md`/README install policy must be updated in that same archive wave.
- Each evaluated skill passes "named owner" only by pack-maintainer/operator convention, not by an explicit owner field inside the skill. If R8 requires a named individual or role per skill, add an owner field or owner table before accepting any keep decision.
