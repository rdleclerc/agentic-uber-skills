from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PackContractTests(unittest.TestCase):
    def test_pack_contract_lint_passes(self) -> None:
        proc = subprocess.run(
            [sys.executable, "scripts/lint_pack_contract.py", "--root", str(ROOT)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)

    def test_all_uber_skills_are_exposed_but_phase_skills_are_explicit(self) -> None:
        expected = {
            "ubergoal": "allow_implicit_invocation: true",
            "uberplan": "allow_implicit_invocation: true",
            "uberaccept": "allow_implicit_invocation: true",
            "uberskillevolver": "allow_implicit_invocation: true",
            "ubersimplify": "allow_implicit_invocation: true",
            "uberassess": "allow_implicit_invocation: true",
            "uberarchitect": "allow_implicit_invocation: true",
        }
        for skill, phrase in expected.items():
            text = (ROOT / skill / "agents" / "openai.yaml").read_text()
            self.assertIn(phrase, text, skill)
            if skill != "ubergoal":
                body = (ROOT / skill / "SKILL.md").read_text()
                meta = (ROOT / skill / "agents" / "openai.yaml").read_text()
                self.assertIn("Do not auto-trigger from task similarity", body, skill)
                self.assertIn("do not auto-trigger from task similarity", meta, skill)


    def test_optional_claude_adversary_contract_is_explicit_and_bounded(self) -> None:
        reference = (ROOT / "references" / "claude-adversary.md").read_text()
        for phrase in [
            "Do **not** invoke the Claude adversary from task similarity",
            "A prompt without an explicit Claude-adversary phrase should not mention adversary invocation",
            "Codex remains owner and reconciler",
            "Skill bodies intentionally inline the key rules",
            "Non-trigger example: `use uberassess on this plan` should run ordinary `uberassess` without Claude adversary language",
            "Default to one Claude challenge round",
            "first two challenges must name distinct layers",
            "No material impact",
            "must not count as independent acceptance evidence",
            "Scope-boundary rejections must state what evidence, approval, or changed scope would bring the challenge in scope",
            "Material edits to challenged sections make the relevant challenge stale",
            "Ship: yes/no, one sentence",
            "Scope Fidelity Packet",
            "Operator original instruction, verbatim",
            "Agent interpreted scope",
            "Proposed narrowed scope",
            "Explicit deferrals/non-goals",
            "Approval evidence",
            "Diff between original and proposed scope",
            "Scope fidelity verdict",
            "Do not let the reviewer assess only the agent's lossy restatement",
            "operator-approved plan",
            "modularity, thin harness / fat skills/tools, and agentic affordance",
            "Gall's Law / Basic Spine First adversary",
            "think bigger about the ultimate goal and first principles",
            "not bigger about the architecture or harness",
            "Basic working spine",
            "What would success NOT look like",
            "smallest next move",
            "Frame-independence / anti-roleplay check",
            "What role is Codex asking Claude to play",
            "accept, modify, or refuse that role",
            "Name three concrete outcomes that would make Claude reject",
            "highly one-sided reconciliation ledger",
            "rubber-stamp warning",
            "reduced-noise, not zero-noise",
            "operator-defined observable success criteria",
        ]:
            self.assertIn(phrase, reference)

        expected_questions = {
            "ubergoal": ["Load-bearing goal?", "Skip test.", "Testable decomposition."],
            "uberplan": ["Most likely execution failure.", "Missing affordance.", "Linear 80/50 alternative."],
            "uberassess": ["Source-lane sufficiency.", "Actionability boundary.", "90-day falsifier."],
            "uberrca": ["Falsification experiment.", "Competing cause.", "Model-blame audit."],
            "uberaccept": ["Receipt reproducibility.", "Scope/diff match.", "Inherited assumption."],
        }
        for skill, questions in expected_questions.items():
            body = (ROOT / skill / "SKILL.md").read_text()
            self.assertIn("## Optional Claude adversary", body, skill)
            self.assertIn("explicitly asks for Claude review", body, skill)
            self.assertIn("Do not invoke Claude from task similarity", body, skill)
            self.assertIn("../references/claude-adversary.md", body, skill)
            self.assertIn("references may not auto-load", body, skill)
            self.assertIn("Default to one Claude challenge round", body, skill)
            self.assertIn("first two challenges must use distinct causal layers", body, skill)
            self.assertIn("`No material impact` is non-evidence: it proves a review ran, not that the artifact is acceptable", body, skill)
            self.assertIn("Frame-independence / anti-roleplay check", body, skill)
            self.assertIn("Claude must stop and flag the review as invalid", body, skill)
            self.assertIn("accepts, modifies, or refuses that role", body, skill)
            self.assertIn("three concrete reject conditions", body, skill)
            self.assertIn("rubber-stamp warnings, not proof of quality", body, skill)
            self.assertIn("reduced-noise, not zero-noise", body, skill)
            self.assertEqual(body.count("## Optional Claude adversary"), 1, skill)
            for question in questions:
                self.assertIn(question, body, skill)
            if skill == "uberaccept":
                self.assertIn("Ship: yes/no, one sentence", body, skill)

    def test_scope_fidelity_contract_prevents_reviewer_scope_drift(self) -> None:
        required_skill_phrases = [
            "operator original instruction",
            "agent-interpreted scope",
            "proposed narrowed scope",
            "explicit deferrals/non-goals",
            "approval evidence",
            "Scope fidelity",
        ]
        for skill in ["ubergoal", "uberplan", "uberassess", "uberaccept"]:
            body = (ROOT / skill / "SKILL.md").read_text()
            for phrase in required_skill_phrases:
                self.assertIn(phrase, body, f"{skill}: {phrase}")
            self.assertIn("must not assess only Codex's summary", body, skill)
            self.assertIn("operator-approved plan", body, skill)
            self.assertIn("modularity, thin harness / fat skills/tools, and agentic affordance", body, skill)
            self.assertIn("Frame-independence / anti-roleplay check", body, skill)

        evolver = (ROOT / "uberskillevolver" / "SKILL.md").read_text()
        self.assertIn("Regression lessons from scope-fidelity failures", evolver)
        self.assertIn("operator original instruction", evolver)
        self.assertIn("hidden semantic judge", evolver)
        self.assertIn("frame-adhesion failures", evolver)
        self.assertIn("invited role named", evolver)

        templates = {
            "uberplan/templates/plan-contract.md": "Scope Fidelity Ledger",
            "uberaccept/templates/final-acceptance.md": "Scope fidelity against operator-original instruction",
            "uberassess/templates/assessment-packet.md": "Scope fidelity for plan/artifact assessments",
            "ubergoal/templates/uber-run-receipt.md": "Scope fidelity",
            "uberskillevolver/templates/post-run-learning.md": "Scope-fidelity regression check",
        }
        for rel, phrase in templates.items():
            text = (ROOT / rel).read_text()
            self.assertIn(phrase, text, rel)
            self.assertIn("Operator original instruction", text, rel)
            self.assertIn("Approval evidence", text, rel)

        plan_template = (ROOT / "uberplan" / "templates" / "plan-contract.md").read_text()
        self.assertIn("Frame-independence / anti-roleplay check", plan_template)
        self.assertIn("Reviewer prompt begins with Operator original instruction, verbatim", plan_template)
        self.assertIn("Three concrete reject conditions before any approval language", plan_template)
        self.assertIn("Rubber-stamp warning", plan_template)
        self.assertIn("Reduced-noise caveat", plan_template)

        learning_template = (ROOT / "uberskillevolver" / "templates" / "post-run-learning.md").read_text()
        self.assertIn("Frame-adhesion / anti-roleplay regression check", learning_template)
        self.assertIn("three concrete reject conditions", learning_template)


    def test_galls_law_basic_spine_adversary_is_packaged_for_plan_review(self) -> None:
        reference = (ROOT / "references" / "claude-adversary.md").read_text()
        for phrase in [
            "Gall's Law / Basic Spine First adversary",
            "think bigger about the ultimate goal and first principles",
            "not bigger about the architecture or harness",
            "simplest end-to-end version that would work now",
            "Is the harness thin and the skill/tool/agent fat",
            "What would success NOT look like",
            "eval proves the basic spine works now",
            "smallest next move",
        ]:
            self.assertIn(phrase, reference)

        plan = (ROOT / "uberplan" / "SKILL.md").read_text()
        self.assertIn("require a Gall's Law / Basic Spine First review before implementation", plan)
        self.assertIn("does not auto-invoke Claude by task similarity", plan)
        self.assertIn("Locally polished micro-feature progress is not a substitute for a basic working spine", plan)

        accept = (ROOT / "uberaccept" / "SKILL.md").read_text()
        self.assertIn("locally polished micro-feature success that did not advance the basic working spine is a soft rejection signal", accept)
        self.assertIn("complex top-down harness", accept)

        template = (ROOT / "uberplan" / "templates" / "plan-contract.md").read_text()
        self.assertIn("Gall's Law / Basic Spine First adversary", template)
        self.assertIn("What success is NOT", template)

    def test_ubergoal_owns_platform_goal_by_default(self) -> None:
        body = (ROOT / "ubergoal" / "SKILL.md").read_text()
        meta = (ROOT / "ubergoal" / "agents" / "openai.yaml").read_text()
        evals = (ROOT / "ubergoal" / "evals" / "golden_skill_invocations.json").read_text()
        combined = "\n".join([body, meta, evals])

        self.assertIn("`ubergoal` is a superset of the platform goal primitive", body)
        self.assertIn("If no goal exists and the user explicitly invoked `ubergoal`, call `create_goal`", body)
        self.assertIn("create or bind a Codex/platform goal", meta)

        obsolete_phrases = [
            "Do not create a platform goal merely because this skill is active",
            "do not call create_goal unless",
            "do not create a platform goal without explicit launch instruction",
            "avoid subagents and goal launch",
        ]
        for phrase in obsolete_phrases:
            self.assertNotIn(phrase, combined)

    def test_ubergoal_tier2_requires_specialist_review_board(self) -> None:
        body = (ROOT / "ubergoal" / "SKILL.md").read_text()
        meta = (ROOT / "ubergoal" / "agents" / "openai.yaml").read_text()
        evals = (ROOT / "ubergoal" / "evals" / "golden_skill_invocations.json").read_text()

        self.assertIn("bounded review-board coordinator", body)
        self.assertIn("Tier 2 is valuable because it changes the decision shape", body)
        self.assertIn("launch 2-3 bounded review lanes", body)
        self.assertIn("Codebase/State Scout, Architecture/Contract Steward, and Black-box Tester / Quality-Eval Auditor", body)
        self.assertIn("specialist review-board agents", meta)
        self.assertIn("run specialist review-board agents or lenses for Tier 2+ work", evals)
        self.assertIn("ubercampaign", body)

    def test_task_understanding_review_is_first_class(self) -> None:
        required = [
            "Task Understanding Review",
            "real problem the operator wants solved",
            "Which requirements are clear?",
            "ambiguous, underspecified",
            "most likely to misunderstand",
            "execution plan",
            "explicitly out of scope",
            "evidence will prove this worked",
            "misunderstanding-prevention step",
        ]
        for rel in ["ubergoal/SKILL.md", "uberplan/SKILL.md"]:
            body = (ROOT / rel).read_text()
            for phrase in required:
                self.assertIn(phrase, body, rel)

        template = (ROOT / "uberplan" / "templates" / "plan-contract.md").read_text()
        for phrase in [
            "Task Understanding Review required before implementation",
            "Real problem the operator wants solved",
            "Clear requirements",
            "Ambiguities / underspecified requirements",
            "Most likely misunderstanding if coding starts directly",
            "Evidence that will prove this worked",
        ]:
            self.assertIn(phrase, template)

    def test_utility_skills_have_task_specific_invocation_policy(self) -> None:
        text = (ROOT / "ubershow" / "agents" / "openai.yaml").read_text()
        self.assertIn("allow_implicit_invocation: true", text)
        self.assertIn("browser-first visual artifact", text)
        body = (ROOT / "ubershow" / "SKILL.md").read_text()
        self.assertIn("Do **not** turn every answer into HTML", body)
        self.assertIn("HTML artifacts are generated **views**, not canonical truth", body)

    def test_root_agent_contract_declares_rca_authority(self) -> None:
        text = (ROOT / "AGENTS.md").read_text()
        self.assertIn("uberrca` = general incident/root-cause authority", text)
        self.assertIn("Agent Advocate = agent-behavior-specific RCA lens", text)
        self.assertIn("use the `uberrca` ladder for depth", text)
        rca = (ROOT / "uberrca" / "SKILL.md").read_text()
        self.assertIn("## Architecture stepback route", rca)
        self.assertIn("$uberarchitect", rca)
        self.assertIn("gateway stalls", rca)

    def test_uber_rca_is_hardened_as_codex_utility_skill(self) -> None:
        self.assertFalse((ROOT / "uberrca" / "README.md").exists())
        self.assertTrue((ROOT / "uberrca" / "agents" / "openai.yaml").exists())
        self.assertTrue((ROOT / "uberrca" / "evals" / "golden_skill_invocations.json").exists())
        self.assertTrue((ROOT / "uberrca" / "scripts" / "lint_skill_package.py").exists())
        meta = (ROOT / "uberrca" / "agents" / "openai.yaml").read_text()
        self.assertIn("allow_implicit_invocation: true", meta)
        self.assertIn("$uberrca", meta)

    def test_uber_skill_creator_is_canonical_and_legacy_aliases_are_deprecated(self) -> None:
        body = (ROOT / "uber-skill-creator" / "SKILL.md").read_text()
        meta = (ROOT / "uber-skill-creator" / "agents" / "openai.yaml").read_text()
        agents = (ROOT / "AGENTS.md").read_text()
        docs = (ROOT / "README.md").read_text() + "\n" + (ROOT / "ROADMAP.md").read_text()

        self.assertIn("Portable Codex/Claude-compatible skill", body)
        self.assertIn("OpenClaw/Gaia/Type0/Soho-specific skill", body)
        self.assertIn("skill-creator-pro", body)
        self.assertIn("deprecation shim", body)
        self.assertIn("Legacy local installs named `skill-creator` or `skill-creator-pro`", agents)
        self.assertIn("Older local installs named `skill-creator` or `skill-creator-pro` should redirect", docs)
        self.assertIn("allow_implicit_invocation: true", meta)

    def test_install_docs_include_full_pack(self) -> None:
        text = (ROOT / "README.md").read_text()
        loop = "for s in uberrca uber-skill-creator ubergoal uberplan uberaccept uberskillevolver ubersimplify uberassess uberarchitect ubershow; do"
        self.assertEqual(text.count(loop), 3)

    def test_operational_outcome_completion_claim_contract_is_pack_wide(self) -> None:
        plan_template = (ROOT / "uberplan" / "templates" / "plan-contract.md").read_text()
        expensive_template = (ROOT / "uberplan" / "templates" / "tier3-expensive-proof-plan-tree.md").read_text()
        goal_receipt = (ROOT / "ubergoal" / "templates" / "uber-run-receipt.md").read_text()
        accept_template = (ROOT / "uberaccept" / "templates" / "final-acceptance.md").read_text()
        learning_template = (ROOT / "uberskillevolver" / "templates" / "post-run-learning.md").read_text()
        plan_tree_reference = (ROOT / "uberplan" / "references" / "plan-tree-artifact-layout.md").read_text()
        self.assertIn("Definition of Done / Operational Outcome Contract", plan_template)
        self.assertIn("Recursive / Hierarchical Execution Pseudocode", plan_template)
        self.assertIn("Plan Tree Artifact Layout", plan_template)
        self.assertIn("plans/<goal-slug>/", plan_tree_reference)
        self.assertIn("Operational outcome / terminal-state summary", goal_receipt)
        self.assertIn("Claim-state ledger", accept_template)
        self.assertIn("shared safe proof spine", learning_template)
        self.assertIn("Runtime agent topology / Codex depth-thread policy", plan_template)
        self.assertIn("Runtime agent topology", goal_receipt)
        self.assertIn("Runtime agent topology acceptance", accept_template)
        self.assertIn("Runtime topology lesson", learning_template)
        self.assertIn("max_threads=6", (ROOT / "ubergoal" / "references" / "campaign-profile.md").read_text())
        self.assertIn("Tier 3 expensive-proof plan-tree preflight", plan_template)
        self.assertIn("Phase-boundary / contract-fuzz preflight", expensive_template)
        self.assertIn("Burn-in proof plan", expensive_template)
        self.assertIn("Final-proof separation", expensive_template)
        self.assertIn("Tier 3 expensive-proof acceptance", accept_template)
        self.assertIn("Unattended production/runtime approval and safe-predecessor plan", plan_template)
        self.assertIn("Production implementation blocker gate", goal_receipt)
        self.assertIn("Production implementation blocker gate", accept_template)
        self.assertIn("Safe-work exhaustion adversarial review", accept_template)
        self.assertIn("active_blocked", (ROOT / "ubergoal" / "SKILL.md").read_text())
        self.assertIn("hard_blocked_after_safe_action_exhaustion", (ROOT / "uberaccept" / "SKILL.md").read_text())
        self.assertIn("plausible safe next actions", (ROOT / "uberaccept" / "SKILL.md").read_text())
        self.assertIn("runnable safe next actions", learning_template)
        self.assertIn("Red/green proof ledger", plan_template)
        self.assertIn("Black-box Tester / Quality-Eval Auditor", plan_template)
        self.assertIn("Red/green and black-box proof ledger audit", accept_template)
        self.assertIn("Red/green / false-green lesson check", learning_template)
        self.assertIn("false-green", (ROOT / "uberaccept" / "SKILL.md").read_text())
        self.assertIn("ubertesting", (ROOT / "ROADMAP.md").read_text())

    def test_intent_driven_verification_fast_path_is_pack_wide(self) -> None:
        goal = (ROOT / "ubergoal" / "SKILL.md").read_text()
        plan = (ROOT / "uberplan" / "SKILL.md").read_text()
        plan_template = (ROOT / "uberplan" / "templates" / "plan-contract.md").read_text()
        accept = (ROOT / "uberaccept" / "SKILL.md").read_text()
        accept_template = (ROOT / "uberaccept" / "templates" / "final-acceptance.md").read_text()
        learning = (ROOT / "uberskillevolver" / "SKILL.md").read_text()
        learning_template = (ROOT / "uberskillevolver" / "templates" / "post-run-learning.md").read_text()
        metadata = "\n".join(
            (ROOT / skill / "agents" / "openai.yaml").read_text()
            for skill in ["ubergoal", "uberplan", "uberaccept", "uberskillevolver"]
        )

        self.assertIn("Micro-intent fast path", goal)
        self.assertIn("2-3 sentences of scope / intent", goal)
        self.assertIn("Do not use the fast path to bypass tests", goal)
        self.assertIn("Micro-intent / spec-first fast path", plan)
        self.assertIn("spec review catches missing requirements", plan)
        self.assertIn("Micro-intent / Intent Review Fast Path", plan_template)
        self.assertIn("Spec review vs code review split", plan_template)
        self.assertIn("Acceptance-criteria verification", accept)
        self.assertIn("block completion on any `fail`", accept)
        self.assertIn("Acceptance criteria verification", accept_template)
        self.assertIn("Spec/intent review vs code review split checked?", accept_template)
        self.assertIn("Slop register", learning)
        self.assertIn("plausible-but-wrong logic", learning)
        self.assertIn("Slop register decision", learning_template)
        self.assertIn("Why this is not hidden semantic authority", learning_template)
        self.assertIn("micro-intent", metadata)
        self.assertIn("acceptance criterion", metadata)
        self.assertIn("slop register", metadata)

    def test_uberarchitect_stepback_gate_is_packaged(self) -> None:
        body = (ROOT / "uberarchitect" / "SKILL.md").read_text()
        meta = (ROOT / "uberarchitect" / "agents" / "openai.yaml").read_text()
        template = (ROOT / "uberarchitect" / "templates" / "architecture-stepback-packet.md").read_text()
        for phrase in [
            "Architecture Stepback Packet",
            "Plain-English diagnosis",
            "System class",
            "Normal industry architecture",
            "Fresh-start architecture",
            "Current mismatch",
            "Symptom patches demoted",
            "Smallest transition path",
            "Proof gate",
            "Human counterfactual",
        ]:
            self.assertIn(phrase, body)
            self.assertIn(phrase.replace("Plain-English diagnosis", "Plain-English diagnosis"), template)
        self.assertIn("Do not auto-trigger from task similarity", body)
        self.assertIn("only when explicitly invoked or routed by $ubergoal", meta)
        self.assertIn("producer → durable queue → bounded worker pool → durable state/results → backpressure", body)

    def test_architecture_stepback_routes_are_present(self) -> None:
        expected = {
            "uberassess": "route to `$uberarchitect`",
            "uberplan": "route to `$uberarchitect`",
            "ubergoal": "route to `$uberarchitect`",
            "uberaccept": "`$uberarchitect` Architecture Stepback Packet",
        }
        for skill, phrase in expected.items():
            body = (ROOT / skill / "SKILL.md").read_text()
            self.assertIn(phrase, body, skill)


if __name__ == "__main__":
    unittest.main()


class UberassessContractTests(unittest.TestCase):
    def test_uberassess_contract_declares_no_implementation_boundary(self) -> None:
        text = (ROOT / "uberassess" / "SKILL.md").read_text()
        self.assertIn("source-grounded recommendations", text)
        self.assertIn("It does not implement", text)
        self.assertIn("Implementation before approval: no", text)
        self.assertIn("benefit >> cost", text)
