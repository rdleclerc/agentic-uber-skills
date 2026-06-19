from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "scripts" / "validate_plan_contract.py"
LINT = ROOT / "scripts" / "lint_skill_package.py"
FIX = ROOT / "tests" / "fixtures"


def run_cmd(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=ROOT, text=True, capture_output=True)


class PlanValidatorTests(unittest.TestCase):
    def assertPasses(self, *args: str) -> None:
        result = run_cmd(*args)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def assertFails(self, *args: str) -> None:
        result = run_cmd(*args)
        self.assertNotEqual(result.returncode, 0, "unexpected pass\n" + result.stdout)

    def test_tier0_plan_stays_lightweight(self) -> None:
        self.assertPasses(str(PLAN), str(FIX / "valid" / "tier0_plan.md"), "--tier", "0")

    def test_tier2_agent_plan_passes_with_agent_behavior(self) -> None:
        self.assertPasses(str(PLAN), str(FIX / "valid" / "tier2_agent_plan.md"), "--tier", "2", "--agent-behavior")

    def test_hollow_tier3_plan_fails(self) -> None:
        self.assertFails(str(PLAN), str(FIX / "invalid" / "hollow_tier3_plan.md"), "--tier", "3", "--agent-behavior")

    def test_agent_behavior_requires_advocate(self) -> None:
        self.assertFails(str(PLAN), str(FIX / "invalid" / "no_agent_advocate_plan.md"), "--tier", "2", "--agent-behavior")

    def test_agent_behavior_requires_boundary_contract(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Agent Boundary Contract")
        end = text.index("## Source authority and truth boundaries")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_boundary_contract.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_agent_behavior_requires_regex_keyword_semantic_gate(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Regex / keyword semantic gate")
        end = text.index("## Source authority and truth boundaries")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_regex_keyword_gate.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_tier2_requires_prd_checklist(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Product / PRD checklist")
        end = text.index("## Task map / implementation graph")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_prd_checklist.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_tier2_requires_task_map_mermaid(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Task map / implementation graph")
        end = text.index("## Tier decision")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_task_map.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_tier2_requires_v0_plan_premortem(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## V0 plan premortem")
        end = text.index("## Verifiable subgoals and metrics")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_v0_plan_premortem.md"
            plan.write_text(text[:start] + text[end:])
            result = run_cmd(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")
            self.assertNotEqual(result.returncode, 0, "unexpected pass\n" + result.stdout)
            self.assertIn("v0 plan premortem", result.stderr.lower())

    def test_tier2_v0_plan_premortem_requires_failure_dispositions(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("| ownership ceremony ignored |")
        end = text.index("## Verifiable subgoals and metrics")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_failure_dispositions.md"
            plan.write_text(text[:start] + "\n" + text[end:])
            result = run_cmd(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")
            self.assertNotEqual(result.returncode, 0, "unexpected pass\n" + result.stdout)
            self.assertIn("failure-disposition", result.stderr.lower())

    def test_tier2_v0_plan_premortem_allows_replan_verdict_structurally(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        text = text.replace(
            "Premortem gate verdict: pass; material blockers were converted into plan revision or accepted risk rows.",
            "Premortem gate verdict: replan; V0 issues were converted into the revised final contract and disposition rows.",
        )
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "replan_premortem_verdict.md"
            plan.write_text(text)
            self.assertPasses(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_tier2_v0_plan_premortem_allows_accepted_risk_only_dispositions(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        text = text.replace("plan revision / accepted risk", "accepted risk")
        text = text.replace("plan revision |", "accepted risk |")
        text = text.replace("plan revision or accepted risk rows", "accepted risk rows")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "accepted_risk_only_premortem.md"
            plan.write_text(text)
            self.assertPasses(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_tier2_requires_verifiable_subgoals(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Verifiable subgoals and metrics")
        end = text.index("## Parallelization plan")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_subgoals.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_tier2_requires_parallelization_plan(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Parallelization plan")
        end = text.index("## Testing adaptation gate")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_parallelization.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_agentic_plan_requires_runtime_agent_topology(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Runtime agent topology / Codex depth-thread policy")
        end = text.index("## Testing adaptation gate")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_runtime_agent_topology.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_tier3_expensive_proof_rejects_flat_plan(self) -> None:
        result = run_cmd(str(PLAN), str(FIX / "invalid" / "tier3_expensive_proof_flat_plan.md"), "--tier", "3", "--agent-behavior")
        self.assertNotEqual(result.returncode, 0, "unexpected pass\n" + result.stdout)
        self.assertIn("expensive-proof", result.stderr)

    def test_tier3_expensive_proof_plan_tree_passes(self) -> None:
        self.assertPasses(
            str(PLAN),
            str(FIX / "valid" / "tier3_expensive_proof_plan_tree.md"),
            "--tier",
            "3",
            "--agent-behavior",
        )

    def test_production_runtime_goal_requires_upfront_approval_and_safe_predecessors(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        text = text.replace(
            "Improve a multi-agent handoff prompt",
            "Improve a production implementation goal with external/irreversible stop points",
            1,
        )
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "production_missing_approval_packet.md"
            plan.write_text(text)
            result = run_cmd(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")
            self.assertNotEqual(result.returncode, 0, "unexpected pass\n" + result.stdout)
            self.assertIn("safe-predecessor", result.stderr)

            section = """## Unattended production/runtime approval and safe-predecessor plan

- Production/runtime implementation goal? yes, this is a long-running production implementation goal with external/irreversible stop points.
- Expected unattended window / operator absence: one unattended work session before operator review.
- Upfront approval packet path/status: `approvals/packet.md` records allowed external/irreversible actions and stop points.
- External/irreversible action categories considered: external approvals, unsafe irreversible migration, credential owner approval, spend/destructive boundaries.
- Safe autonomous predecessor work decomposition: do safe predecessor validation, dry-run, rollback rehearsal, and local evidence collection before external stop.
- Exact stop-before-external-action rule: stop and ask before any external, unsafe, or irreversible action.
- Active blocker definition: active_blocked means a blocked child still has runnable safe next action work.
- Hard blocker after exhaustion definition: hard blocker requires safe predecessor work exhausted and exact external/unsafe approval blocker remains.
- Parent completion rule: parent completion requires runnable safe next action count = 0, active blocked count = 0, and all children operational, user-rescoped, or hard-blocked-after-exhaustion.
- If no upfront approval needed, why: not applicable; upfront approval packet is required and recorded.

| Child / phase | Safe predecessor work to do before stop | Exact external/unsafe/irreversible boundary | Approval or owner needed | Status |
|---|---|---|---|---|
| C1 | safe predecessor validation and dry-run | external irreversible cutover | operator approval | planned |

"""
            insertion = text.index("## Product / PRD checklist")
            valid = text[:insertion] + section + text[insertion:]
            valid = valid.replace(
                "| Operational outcome | Definition of done, non-implementation examples, terminal states, and proof requirements are explicit | Definition of Done / Operational Outcome Contract | 3 |",
                "| Operational outcome | Definition of done, non-implementation examples, terminal states, and proof requirements are explicit | Definition of Done / Operational Outcome Contract | 3 |\n| Production implementation blocker gate | Long unattended production/runtime goals include upfront approvals, safe-predecessor work, active-vs-hard blockers, and no runnable safe next actions at completion | Unattended production/runtime approval and safe-predecessor plan | 3 |",
            )
            valid_plan = Path(tmp) / "production_with_approval_packet.md"
            valid_plan.write_text(valid)
            self.assertPasses(str(PLAN), str(valid_plan), "--tier", "2", "--agent-behavior")

    def test_tier2_requires_testing_adaptation_gate(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Testing adaptation gate")
        end = text.index("## Tier decision")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_testing_adaptation.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_tier2_requires_scope_fidelity(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Scope fidelity")
        end = text.index("## Scope\n", start + 1)
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_scope_fidelity.md"
            plan.write_text(text[:start] + text[end:])
            result = run_cmd(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")
            self.assertNotEqual(result.returncode, 0, "unexpected pass\n" + result.stdout)
            self.assertIn("scope fidelity", result.stderr)

    def test_tier2_requires_goal_execution_posture(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Goal execution posture and delivery")
        end = text.index("## Product / PRD checklist")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_goal_execution_posture.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_tier2_requires_user_expectation_surprise_assessment(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## User expectation / surprise assessment")
        end = text.index("## Product / PRD checklist")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_user_expectation.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_tier2_requires_operational_outcome_contract(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Definition of Done / Operational Outcome Contract")
        end = text.index("## Product / PRD checklist")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_operational_outcome.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_hierarchical_plan_requires_recursive_pseudocode(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        text = text.replace(
            "Improve a multi-agent handoff prompt",
            "Improve a multi-agent handoff prompt and execute all child plans in a parent goal",
            1,
        )
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "hierarchical_missing_pseudocode.md"
            plan.write_text(text)
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

            recursive = """## Recursive / Hierarchical Execution Pseudocode

```text
for each child_plan in parent.children:
  execute child_plan until terminal_state is operational, blocked, or re_scoped_with_approval
  reject shared_parent_spine proof as operational unless the child explicitly scoped it as the final outcome
  record child proof, blocker, or re-scope evidence before parent completion
```

- Hierarchy applies? yes, because this parent goal executes all child plans.
- Max depth / child-count budget before asking or blocking: one parent level and ten child plans before asking.
- Child status table required? yes, because parent completion depends on child terminal_state evidence.

| Child plan ID | Intended outcome | Terminal state: operational / blocked / re_scoped_with_approval | Evidence / blocker / re-scope approval |
|---|---|---|---|
| C1 | prompt contract operational | operational | validator and acceptance evidence |

## Plan Tree Artifact Layout

- Plan tree required? yes, because this parent goal executes all child plans.
- Root index path: plans/parent-goal/index.md
- Status ledger path: plans/parent-goal/status-ledger.md
- Child plans directory: plans/parent-goal/children/
- Receipts directory: plans/parent-goal/receipts/
- Final acceptance receipt path: plans/parent-goal/receipts/final-acceptance.md
- Split trigger met? yes, because child operational outcomes need separate proof.
- Parent/shared proof cannot substitute for child proof? yes, child receipts are required.

| Child ID | Child plan path | Intended operational outcome | Dependency / owner | Receipt path |
|---|---|---|---|---|
| C1 | plans/parent-goal/children/C1-prompt-contract.md | prompt contract operational | parent / prompt owner | plans/parent-goal/receipts/C1-acceptance.md |

"""
            insertion = text.index("## Product / PRD checklist")
            text_with_recursive = text[:insertion] + recursive + text[insertion:]
            text_with_recursive = text_with_recursive.replace(
                "| Operational outcome | Definition of done, non-implementation examples, terminal states, and proof requirements are explicit | Definition of Done / Operational Outcome Contract | 3 |",
                "| Operational outcome | Definition of done, non-implementation examples, terminal states, and proof requirements are explicit | Definition of Done / Operational Outcome Contract | 3 |\n| Recursive pseudocode | Hierarchical child plans include loop pseudocode, terminal-state rules, and parent completion criteria | Recursive / Hierarchical Execution Pseudocode | 3 |\n| Plan tree artifact layout | Hierarchical plans split root index, child files, status ledger, receipts, and final acceptance | Plan Tree Artifact Layout | 3 |",
            )
            valid_plan = Path(tmp) / "hierarchical_with_pseudocode.md"
            valid_plan.write_text(text_with_recursive)
            self.assertPasses(str(PLAN), str(valid_plan), "--tier", "2", "--agent-behavior")

    def test_hierarchical_plan_requires_plan_tree_layout(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        text = text.replace(
            "Improve a multi-agent handoff prompt",
            "Improve a multi-agent handoff prompt and execute all child plans in a parent goal",
            1,
        )
        recursive = """## Recursive / Hierarchical Execution Pseudocode

```text
for each child_plan in parent.children:
  execute child_plan until terminal_state is operational, blocked, or re_scoped_with_approval
  reject shared_parent_spine proof as operational unless the child explicitly scoped it as the final outcome
  record child proof, blocker, or re-scope evidence before parent completion
```

- Hierarchy applies? yes, because this parent goal executes all child plans.
- Max depth / child-count budget before asking or blocking: one parent level and ten child plans before asking.
- Child status table required? yes, because parent completion depends on child terminal_state evidence.

| Child plan ID | Intended outcome | Terminal state: operational / blocked / re_scoped_with_approval | Evidence / blocker / re-scope approval |
|---|---|---|---|
| C1 | prompt contract operational | operational | validator and acceptance evidence |

"""
        insertion = text.index("## Product / PRD checklist")
        text = text[:insertion] + recursive + text[insertion:]
        text = text.replace(
            "| Operational outcome | Definition of done, non-implementation examples, terminal states, and proof requirements are explicit | Definition of Done / Operational Outcome Contract | 3 |",
            "| Operational outcome | Definition of done, non-implementation examples, terminal states, and proof requirements are explicit | Definition of Done / Operational Outcome Contract | 3 |\n| Recursive pseudocode | Hierarchical child plans include loop pseudocode, terminal-state rules, and parent completion criteria | Recursive / Hierarchical Execution Pseudocode | 3 |",
        )
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "hierarchical_missing_plan_tree.md"
            plan.write_text(text)
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_operational_contract_rejects_proof_only_as_done(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        text = text.replace(
            "- What counts as implemented/operational for this plan: source files are changed in the intended package, validator tests pass, and the final acceptance report names residual fresh-agent replay gaps.",
            "- What counts as implemented/operational for this plan: a shared spine local proof and eval fixture are enough to call the parent operational.",
        ).replace(
            "- What does NOT count as implementation: readiness gate / safe adoption spine / registry / plan / eval fixture / local proof / shadow-only proof / shared parent proof unless explicitly scoped as final outcome: a plan-only note or eval seed without validator/template changes does not satisfy this plan.",
            "- What does NOT count as implementation: unrelated prose-only wishes.",
        )
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "proof_only_operational_outcome.md"
            plan.write_text(text)
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_hierarchical_pseudocode_requires_child_terminal_table(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        text = text.replace(
            "Improve a multi-agent handoff prompt",
            "Improve a multi-agent handoff prompt and execute all child plans in a parent goal",
            1,
        )
        recursive = """## Recursive / Hierarchical Execution Pseudocode

```text
for each child_plan in parent.children:
  execute child_plan until terminal_state is operational, blocked, or re_scoped_with_approval
  reject shared_parent_spine proof as operational unless the child explicitly scoped it as the final outcome
  record child proof, blocker, or re-scope evidence before parent completion
```

- Hierarchy applies? yes, because this parent goal executes all child plans.
- Max depth / child-count budget before asking or blocking: one parent level and ten child plans before asking.
- Child status table required? yes, because parent completion depends on child terminal_state evidence.

"""
        insertion = text.index("## Product / PRD checklist")
        text = text[:insertion] + recursive + text[insertion:]
        text = text.replace(
            "| Operational outcome | Definition of done, non-implementation examples, terminal states, and proof requirements are explicit | Definition of Done / Operational Outcome Contract | 3 |",
            "| Operational outcome | Definition of done, non-implementation examples, terminal states, and proof requirements are explicit | Definition of Done / Operational Outcome Contract | 3 |\n| Recursive pseudocode | Hierarchical child plans include loop pseudocode, terminal-state rules, and parent completion criteria | Recursive / Hierarchical Execution Pseudocode | 3 |",
        )
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "hierarchical_missing_child_table.md"
            plan.write_text(text)
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_code_plan_requires_target_file_tree(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Target architecture / file tree")
        end = text.index("## Repository topology / package seam")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_target_file_tree.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_code_plan_requires_dead_code_tool_plan(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Code-health / dead-code tool plan")
        end = text.index("## Risk-to-evidence map")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_dead_code_plan.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_tier2_requires_decision_tradeoff_register(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Decision / tradeoff / surprise register")
        end = text.index("## Pre-presentation over-orchestration review")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_decision_register.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_tier2_requires_over_orchestration_review(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Pre-presentation over-orchestration review")
        end = text.index("## Plan acceptance gate")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_over_orchestration_review.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_tier2_requires_plan_acceptance_gate(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Plan acceptance gate")
        end = text.index("## Pre-launch confidence gate")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_plan_acceptance.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_agentic_plan_requires_thin_harness_rubric(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Thin harness / fat agent design rubric")
        end = text.index("## Source-convention check")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_thin_harness.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_agentic_plan_requires_agent_execution_proof_ladder(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Agent execution proof ladder")
        end = text.index("## Source-convention check")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_agent_execution_proof_ladder.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_agentic_plan_requires_source_convention_check(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        start = text.index("## Source-convention check")
        end = text.index("## Agent Boundary Contract")
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "missing_source_convention.md"
            plan.write_text(text[:start] + text[end:])
            self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_code_plan_requires_repository_topology(self) -> None:
        self.assertFails(str(PLAN), str(FIX / "invalid" / "no_repository_topology_plan.md"), "--tier", "2", "--agent-behavior")

    def test_existing_file_plan_can_mark_topology_not_applicable(self) -> None:
        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
        text = text.replace("the added validator fixture", "the validator fixture")
        text = text.replace("one small validator fixture", "the small validator fixture")
        text = text.replace("adding validator fixture coverage", "updating validator fixture coverage")
        text = text.replace("New validator/test files stay inside the existing skill package", "Existing validator/test files stay inside the existing skill package")
        text = text.replace("Add validator and fixture coverage", "Update validator and fixture coverage")
        text = text.replace("Add deterministic harness validation", "Update deterministic harness validation")
        text = text.replace("root-level", "top-level")
        text = text.replace("refactor", "cleanup")
        text = text.replace("Refactor", "Cleanup")
        start = text.index("## Target architecture / file tree")
        end = text.index("## Architecture classification")
        replacement = """## Target architecture / file tree

Not applicable because this plan only edits existing files inside their current owning package and does not add or relocate files, create root-level modules, restructure package boundaries, or change import/dependency seams.

## Repository topology / package seam

Not applicable because this plan only edits existing files inside their current owning package and does not add or relocate files, create root-level modules, restructure package boundaries, or change import/dependency seams.

"""
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "existing_file_plan.md"
            plan.write_text(text[:start] + replacement + text[end:])
            self.assertPasses(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")

    def test_templates_need_allow_template_mode(self) -> None:
        self.assertFails(str(PLAN), str(ROOT / "templates" / "plan-contract.md"), "--tier", "2")
        self.assertPasses(str(PLAN), str(ROOT / "templates" / "plan-contract.md"), "--tier", "2", "--allow-template")


class PackageTests(unittest.TestCase):
    def test_package_lint_passes(self) -> None:
        for cache in ROOT.rglob("__pycache__"):
            shutil.rmtree(cache)
        result = run_cmd(str(LINT), str(ROOT))
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_golden_eval_schema(self) -> None:
        cases = json.loads((ROOT / "evals" / "golden_skill_invocations.json").read_text())
        ids = {case["id"] for case in cases}
        self.assertIn("agent_error_triggers_advocate", ids)
        self.assertIn("complex_codebase_exploration_trail", ids)
        self.assertIn("complexity_blocked_without_benefit_gap", ids)
        self.assertIn("agent_boundary_contract_blocks_generic_reliability_plan", ids)
        self.assertIn("semantic_regex_gate_blocks_keyword_router_plan", ids)
        self.assertIn("agentic_system_plan_requires_prd_task_map_and_thin_harness", ids)
        self.assertIn("long_running_goal_not_uberslice", ids)
        self.assertIn("agentic_plan_requires_codex_to_openclaw_proof_ladder", ids)
        self.assertIn("plan_self_reviews_over_orchestration_before_presentation", ids)
        self.assertIn("repeated_testing_failures_require_rca_replan", ids)
        self.assertIn("unexpected_testing_failure_requires_child_plan_append", ids)
        self.assertIn("plan_requires_user_expectation_surprise_assessment", ids)
        self.assertIn("plan_requires_operational_outcome_contract", ids)
        self.assertIn("hierarchical_plan_requires_recursive_pseudocode", ids)
        self.assertIn("hierarchical_plan_requires_plan_tree_artifact_layout", ids)
        self.assertIn("plan_records_runtime_agent_topology", ids)
        self.assertIn("tier3_expensive_proof_requires_plan_tree_preflight", ids)
        self.assertIn("production_runtime_goal_requires_approval_packet_and_safe_predecessors", ids)
        for case in cases:
            self.assertIn("user_prompt", case)
            self.assertIn("expected_tier", case)
            self.assertTrue(case.get("required_behavior") or case.get("required_lanes"))

    def test_key_templates_exist(self) -> None:
        for rel in [
            "templates/plan-contract.md",
            "templates/confidence-gate.md",
            "templates/exploration-trail.md",
            "templates/first-principles-simplifier-report.md",
            "templates/plan-contract.md",
            "templates/tier3-expensive-proof-plan-tree.md",
            "references/plan-tree-artifact-layout.md",
        ]:
            self.assertTrue((ROOT / rel).exists(), rel)


if __name__ == "__main__":
    unittest.main()
