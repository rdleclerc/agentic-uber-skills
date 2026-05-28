# Claude adversarial review prompt — uberskills scope fidelity structural gate

You are reviewing Codex changes. Do not review a narrowed summary. Section 1 is the durable scope artifact with the operator original instruction. Section 2 is the actual artifact/diff under review.

## Section 1 — coordination/uberskills-merge-push-scope-fidelity/scope.md
# Scope Artifact

Task slug: `uberskills-merge-push-scope-fidelity`
Created: `2026-05-28T08:00:00-0700`
Owner/session: `uberskills-merge-push`

## Original operator instruction

```text
Update the Uber skills to prevent scope laundering and ignored skill directives.

Context:
A recent `ubergoal`/`uberplan`/`uberaccept` run violated scope fidelity. The operator asked for a codebase-wide OpenClaw ownership audit and implementation, but Codex narrowed the work to a Slack/transcript patch, asked Claude to review only that narrowed patch, then marked the goal complete. This violated the existing Uber skill requirements that Claude/adversary review be anchored to the operator-original instruction.

Goal:
Implement the smallest durable change that materially prevents this recurrence. Do not add another reminder line that can get lost. Make scope fidelity a required artifact and structural acceptance gate.

Required design:
1. `ubergoal` must create or update `coordination/<task-slug>/scope.md` for Tier 1+ or explicit `ubergoal` work.
   - It must contain the operator’s original instruction verbatim.
   - It must preserve explicit constraints and later user scope changes as dated entries.
   - Later entries append; they do not overwrite the original scope.

2. `uberplan` must require a `## Scope fidelity` block in durable plans.
   It must include:
   - `Original scope:` quote or link to `scope.md`
   - `Plan scope:`
   - `Narrowing? yes/no`
   - `Operator approved narrowing in:` quote/link, required if narrowed
   - If narrowing is unapproved, plan is invalid / cannot proceed as completion.

3. `uberaccept` must require a `## Scope fidelity verdict` before any `SHIP`, completion, or goal-complete language.
   It must:
   - Quote or link to `scope.md`, not only the plan summary.
   - Answer whether implemented scope satisfies original scope.
   - Cite approval for any narrowing.
   - Treat unapproved narrowing as a blocker.

4. Add a small structural validator, e.g. `scripts/check_scope_fidelity_artifacts.py`.
   Keep it presence-only and non-semantic. It should fail when:
   - `scope.md` is missing.
   - acceptance/final report lacks `## Scope fidelity verdict`.
   - `SHIP` appears before the scope-fidelity verdict.
   - `Narrowing? yes` appears without a non-empty approval citation.
   Do not attempt to semantically compare original vs implemented scope.

5. Add or update templates so agents do not have to remember the format:
   - scope artifact template if appropriate
   - plan contract scope block
   - final acceptance scope verdict block
   - Claude/adversary prompt template should load `scope.md` as section 1 and diff/artifact under review as section 2.
   - Save generated Claude/adversary prompts into the coordination folder when used.

6. Add focused tests or fixtures:
   - Regression: original scope says “codebase-wide OpenClaw ownership audit,” plan/acceptance narrows to Slack-only with no approval; validator fails.
   - Legitimate narrowing: operator explicitly approves narrowing to Slack; validator passes.
   - SHIP before scope verdict; validator fails.

Ownership constraints:
- Agent/reviewer owns semantic judgment about whether implemented scope truly satisfies original scope.
- Uber skill text owns workflow obligations.
- Durable artifacts own the preserved operator instruction and scope ledger.
- Validator owns structural presence/order checks only.
- Do not build a deterministic semantic judge.
- Do not create a new top-level `uberscope` skill unless unavoidable.
- Keep changes surgical and avoid broad skill bloat.

Use Claude adversarial review if available, but make sure Claude receives this prompt and the relevant skill files, not a narrowed summary. Final output should include changed files, tests run, and any residual risk.
```

## Explicit constraints and non-goals from original instruction

- Constraint: smallest durable structural artifact/gate; avoid reminder-only patch.
- Constraint: validator is structural/presence/order only, not semantic comparison.
- Constraint: no new top-level `uberscope` skill unless unavoidable.
- Constraint: keep changes surgical and avoid broad skill bloat.
- Non-goal: deterministic semantic scope judge.
- Non-goal: OpenClaw/Type0 runtime changes.

## Scope change ledger

### 2026-05-28T08:00:00-0700 — initial capture

- Source: original operator instruction
- Change type: initial
- User instruction or artifact path: this file, original instruction block above
- Effect on scope: implement structural scope artifact/gate in existing Uber skills and validator/tests
- Approval evidence for narrowing/deferral: n/a for initial capture

## Section 2 — git diff/artifact under review
diff --git a/references/claude-adversary.md b/references/claude-adversary.md
index 8e1d7fa..478f8c6 100644
--- a/references/claude-adversary.md
+++ b/references/claude-adversary.md
@@ -21,14 +21,17 @@ Do **not** invoke the Claude adversary from task similarity, from a generic need
 
 For any Claude/second-review round that judges a goal, plan, assessment, acceptance, or proposed scope, the reviewer prompt must include a **Scope Fidelity Packet** before the agent's summary. Do not let the reviewer assess only the agent's lossy restatement.
 
+Prompt artifact rule: save the exact generated Claude/adversary prompt under `coordination/<task-slug>/` before running it. Section 1 of that prompt must load or quote `coordination/<task-slug>/scope.md`. Section 2 must be the diff, plan, final report, or artifact under review.
+
 Required packet fields:
 
-1. **Operator original instruction, verbatim** — exact controlling prompt/instruction, or an exact artifact path when too long/sensitive. Do not replace it with an agent summary.
-2. **Agent interpreted scope** — what the agent believes the work means.
-3. **Proposed narrowed scope** — any smaller slice the agent proposes to do now.
-4. **Explicit deferrals/non-goals** — obligations not being done now.
-5. **Approval evidence** — whether the operator explicitly approved each narrowing or deferral.
-6. **Diff between original and proposed scope** — added, removed, narrowed, or deferred obligations.
+1. **Scope artifact** — `coordination/<task-slug>/scope.md`, loaded or quoted as prompt section 1.
+2. **Operator original instruction, verbatim** — from `scope.md`, or an exact artifact path when too long/sensitive. Do not replace it with an agent summary.
+3. **Agent interpreted scope** — what the agent believes the work means.
+4. **Proposed narrowed scope** — any smaller slice the agent proposes to do now.
+5. **Explicit deferrals/non-goals** — obligations not being done now.
+6. **Approval evidence** — whether the operator explicitly approved each narrowing or deferral.
+7. **Diff between original and proposed scope** — added, removed, narrowed, or deferred obligations.
 
 The reviewer must answer:
 
diff --git a/uberaccept/SKILL.md b/uberaccept/SKILL.md
index 1740ae2..06d81ba 100644
--- a/uberaccept/SKILL.md
+++ b/uberaccept/SKILL.md
@@ -55,6 +55,10 @@ When a task used a micro-intent, work contract, PRD, ticket, or `uberplan` with
 
 This is not a replacement for the Operational Outcome Contract. Acceptance criteria prove the stated intent was checked; the Operational Outcome Contract proves the final state being claimed. For AI-generated code, also check whether spec/intent review caught design and scope issues before code, and whether code review still covered repo conventions, naming, module seams, integration details, and maintainability.
 
+## Scope fidelity verdict gate
+
+Before any `SHIP`, completion, ready, or goal-complete language, final acceptance must include `## Scope fidelity verdict`. It must quote/link `coordination/<task-slug>/scope.md`, check the operator original instruction, agent-interpreted scope, proposed narrowed scope, explicit deferrals/non-goals, and approval evidence, answer whether implemented scope satisfies original scope, and block unapproved narrowing.
+
 ## Output contract
 
 Produce a final acceptance report that names every relevant layer explicitly:
@@ -69,7 +73,7 @@ Produce a final acceptance report that names every relevant layer explicitly:
 8. Tier 3 expensive-proof acceptance when the work involved burn-in, soak, canary expansion, replacement proof, or final proof
 9. planning-board reconciliation
 10. user expectation / surprise delta: what the user likely expected, what was actually implemented, what changed, what may surprise them, and whether any mismatch needs explicit approval
-11. scope fidelity: compare operator original instruction, agent-interpreted scope, proposed narrowed scope, explicit deferrals/non-goals, approval evidence, and actual diff/evidence; unapproved narrowing blocks completion
+11. scope fidelity verdict: quote/link `coordination/<task-slug>/scope.md`, compare original scope to implemented scope, cite approved narrowing, and block unapproved narrowing
 12. Agent Advocate final check for agentic work or agent failures
 13. Architecture Steward final check
 14. first-principles simplification and cost/complexity verdict, including any Basic Spine First veto
@@ -130,7 +134,7 @@ Use this only when the user explicitly asks for Claude review, e.g. `with Claude
 
 Default to one Claude challenge round; run two or three only when requested or when material unresolved risk remains. Each Claude challenge must name a claim, causal layer, why it matters, falsifying/satisfying evidence, and minimum impact threshold. If more than one challenge is raised, the first two challenges must use distinct causal layers; a single-challenge round must say why only one challenge is material. Codex reconciliation must classify each challenge as `Accepted`, `Risk added`, `Rejected`, `Uncertain`, or `No material impact`; `No material impact` is non-evidence: it proves a review ran, not that the artifact is acceptable. Bind the ledger to the artifact version/section reviewed.
 
-Before the skill-specific questions, include the Scope Fidelity Packet from `../references/claude-adversary.md` and require the reviewer to answer `Original-scope satisfaction`, `Narrowing approval`, and `Scope fidelity verdict` against the operator-original instruction. A reviewer must not assess only Codex's summary or proposed scope. Also require Claude to challenge whether Codex is sticking to the operator-approved plan and preserving modularity, thin harness / fat skills/tools, and agentic affordance unless the user explicitly overrides those defaults. For agentic-system or architecture-changing work, include the Gall's Law / Basic Spine First check: whether the accepted work evolved a basic working spine, avoided top-down harness drift, preserved the thin/fat split, and kept evals green while robustness improved.
+Before the skill-specific questions, include the Scope Fidelity Packet from `../references/claude-adversary.md`: section 1 must be `coordination/<task-slug>/scope.md`; section 2 must be the final diff/artifact under review; save the generated Claude prompt in that coordination folder. Require the reviewer to answer `Original-scope satisfaction`, `Narrowing approval`, and `Scope fidelity verdict` against the operator-original instruction. A reviewer must not assess only Codex's summary or proposed scope. Also require Claude to challenge whether Codex is sticking to the operator-approved plan and preserving modularity, thin harness / fat skills/tools, and agentic affordance unless the user explicitly overrides those defaults. For agentic-system or architecture-changing work, include the Gall's Law / Basic Spine First check: whether the accepted work evolved a basic working spine, avoided top-down harness drift, preserved the thin/fat split, and kept evals green while robustness improved.
 
 Also include the Frame-independence / anti-roleplay check from `../references/claude-adversary.md`. The reviewer prompt must put the operator-original instruction first; if it is missing, Claude must stop and flag the review as invalid. Before any approval language, require Claude to state what role Codex is asking it to play and whether it accepts, modifies, or refuses that role; name what the operator's original instruction requires that Codex's summary might hide or narrow; and list three concrete reject conditions. Treat highly one-sided `Accepted`/`No material impact` ledgers as rubber-stamp warnings, not proof of quality. Model adversary review is reduced-noise, not zero-noise, and does not replace operator-defined observable success criteria, direct prompt/diff spot-checks, deterministic tests, evals, or receipts.
 
diff --git a/uberaccept/scripts/validate_acceptance_report.py b/uberaccept/scripts/validate_acceptance_report.py
index 9da1fcf..d6189b3 100755
--- a/uberaccept/scripts/validate_acceptance_report.py
+++ b/uberaccept/scripts/validate_acceptance_report.py
@@ -14,6 +14,7 @@ from pathlib import Path
 REQUIRED_SECTIONS = [
     "implementation summary",
     "files changed",
+    "scope fidelity verdict",
     "rubric scores",
     "commands and artifacts",
     "claim-state ledger",
diff --git a/uberaccept/templates/final-acceptance.md b/uberaccept/templates/final-acceptance.md
index 66b4542..023ed35 100644
--- a/uberaccept/templates/final-acceptance.md
+++ b/uberaccept/templates/final-acceptance.md
@@ -7,16 +7,20 @@
 
 -
 
-## Scope fidelity
-
-- Operator original instruction, verbatim or exact artifact path:
-- Agent interpreted scope:
-- Proposed narrowed scope, if any:
-- Explicit deferrals / non-goals:
-- Approval evidence for each narrowing or deferral:
-- Diff between original and actual delivered scope:
-- Scope fidelity verdict: pass / fail / uncertain:
-- If narrowed, was it operator-approved? yes/no/n/a, evidence:
+## Scope fidelity verdict
+
+This section must appear before any `SHIP`, completion, ready, or goal-complete language. Quote or link the durable scope artifact, not only the plan summary.
+
+- Scope artifact: `coordination/<task-slug>/scope.md`
+- Original scope: quote or link to `scope.md` Operator original instruction
+- Implemented scope:
+- Does implemented scope satisfy original scope? yes/no/partial
+- Narrowing? yes/no
+- Operator approved narrowing in: quote/link required if narrowed
+- Approval evidence for narrowing/deferral: quote/link or n/a
+- Explicit constraints and later user scope changes checked: yes/no
+- Unapproved narrowing blocker? yes/no
+- Scope fidelity verdict: pass / fail / uncertain
 
 ## Rubric scores
 
diff --git a/uberaccept/tests/fixtures/valid/final_acceptance.md b/uberaccept/tests/fixtures/valid/final_acceptance.md
index 40a9cc9..80306a2 100644
--- a/uberaccept/tests/fixtures/valid/final_acceptance.md
+++ b/uberaccept/tests/fixtures/valid/final_acceptance.md
@@ -11,6 +11,19 @@ Hardened validators, metadata, templates, package lint, and golden eval fixtures
 - tests/test_validators.py
 - evals/golden_skill_invocations.json
 
+
+## Scope fidelity verdict
+
+- Scope artifact: `coordination/test-scope/scope.md`
+- Original scope: `coordination/test-scope/scope.md` original operator instruction.
+- Implemented scope: local skill-package hardening and deterministic tests.
+- Does implemented scope satisfy original scope? yes
+- Narrowing? no
+- Operator approved narrowing in: n/a
+- Explicit constraints and later user scope changes checked: yes
+- Unapproved narrowing blocker? no
+- Scope fidelity verdict: pass
+
 ## Rubric scores
 
 | Dimension | Score | Evidence | Residual gap |
diff --git a/uberaccept/tests/fixtures/valid/production_hard_blocked_acceptance.md b/uberaccept/tests/fixtures/valid/production_hard_blocked_acceptance.md
index 4076ad4..c15d810 100644
--- a/uberaccept/tests/fixtures/valid/production_hard_blocked_acceptance.md
+++ b/uberaccept/tests/fixtures/valid/production_hard_blocked_acceptance.md
@@ -11,6 +11,19 @@ Accepted a domain-neutral production implementation goal with child blockers and
 - tests/test_validators.py
 - evals/golden_skill_invocations.json
 
+
+## Scope fidelity verdict
+
+- Scope artifact: `coordination/test-scope/scope.md`
+- Original scope: `coordination/test-scope/scope.md` original operator instruction.
+- Implemented scope: local skill-package hardening and deterministic tests.
+- Does implemented scope satisfy original scope? yes
+- Narrowing? no
+- Operator approved narrowing in: n/a
+- Explicit constraints and later user scope changes checked: yes
+- Unapproved narrowing blocker? no
+- Scope fidelity verdict: pass
+
 ## Rubric scores
 
 | Dimension | Score | Evidence | Residual gap |
diff --git a/uberaccept/tests/test_validators.py b/uberaccept/tests/test_validators.py
index 33720c0..ececebc 100644
--- a/uberaccept/tests/test_validators.py
+++ b/uberaccept/tests/test_validators.py
@@ -31,6 +31,17 @@ class AcceptanceValidatorTests(unittest.TestCase):
     def test_valid_acceptance_passes(self) -> None:
         self.assertPasses(str(ACCEPT), str(FIX / "valid" / "final_acceptance.md"), "--agent-behavior")
 
+    def test_acceptance_requires_scope_fidelity_verdict(self) -> None:
+        text = (FIX / "valid" / "final_acceptance.md").read_text()
+        start = text.index("## Scope fidelity verdict")
+        end = text.index("## Rubric scores")
+        with tempfile.TemporaryDirectory() as tmp:
+            report = Path(tmp) / "missing_scope_fidelity_verdict.md"
+            report.write_text(text[:start] + text[end:])
+            result = run_cmd(str(ACCEPT), str(report), "--agent-behavior")
+            self.assertNotEqual(result.returncode, 0, "unexpected pass\n" + result.stdout)
+            self.assertIn("scope fidelity verdict", result.stderr)
+
     def test_blank_acceptance_fails(self) -> None:
         self.assertFails(str(ACCEPT), str(FIX / "invalid" / "blank_acceptance.md"), "--agent-behavior")
 
diff --git a/ubergoal/SKILL.md b/ubergoal/SKILL.md
index bd8747a..04cc61e 100644
--- a/ubergoal/SKILL.md
+++ b/ubergoal/SKILL.md
@@ -50,10 +50,14 @@ Review this intent before implementation when the task is above a trivial edit.
 
 Code review and intent/spec review catch different failures. Intent/spec review should catch missing requirements, bad scope, and design mismatches before code exists; code review should catch repo conventions, naming, module seams, integration details, and maintainability. Do not use the fast path to bypass tests, evidence, final `$uberaccept`, or Tier 2/3 operational outcome gates.
 
+## Scope artifact gate
+
+For Tier 1+ or any explicit `ubergoal` work, create or update `coordination/<task-slug>/scope.md` from `templates/scope.md` before planning. Preserve the operator original instruction verbatim, agent-interpreted scope, proposed narrowed scope, explicit deferrals/non-goals, approval evidence, constraints, and dated later user changes. Never overwrite the original scope.
+
 ## Lifecycle
 
 1. **Classify tier.** Choose the lowest safe Tier 0/1/2/3.
-2. **Frame enough to make the goal non-vague.** Before creating a platform goal, do the minimum clarification needed to name the outcome, rough scope, non-goals, likely tier, and what “done” could mean. For Tier 0/1, a micro-intent note may be enough. Preserve the operator original instruction, verbatim or by exact artifact path, before compressing it into a goal objective. For Tier 1+ or reviewer-involved work, record operator-original scope, agent-interpreted scope, proposed narrowed scope, explicit deferrals/non-goals, and approval evidence for any narrowing. This is not full planning and must not become implementation.
+2. **Frame enough to make the goal non-vague.** Before creating a platform goal, do the minimum clarification needed to name the outcome, rough scope, non-goals, likely tier, and what “done” could mean. For Tier 0/1, a micro-intent note may be enough. For Tier 1+ or explicit `ubergoal` work, first create/update `coordination/<task-slug>/scope.md`; record operator-original scope, interpreted scope, proposed narrowing, deferrals/non-goals, and approval evidence there. This is not full planning and must not become implementation.
 3. **Create or bind the goal before robust planning/execution.** If no goal exists and the user explicitly invoked `ubergoal`, call `create_goal` once the compact objective is specific enough. The goal may explicitly be “produce a robust plan, then execute it after the acceptance gate”; this preserves `ubergoal`’s purpose of preventing shallow plans while avoiding vague goal launch.
 4. **Plan.** Start Tier 1+ with a **user expectation / surprise assessment**. Use a micro-intent note, work contract, or `$uberplan` by tier/risk. Agentic-system plans bias toward thin deterministic harnesses around capable agents. Do not execute until the plan or work contract names verification, stop conditions, and a red/green proof ledger when the task changes code, skills, prompts, workflows, or agent behavior.
 5. **Review and execute.** Main agent owns integration. Explicit `ubergoal` authorizes bounded Tier 2+ specialist review-board agents/lenses unless the user says no/lightweight. Workers mutate files only with disjoint write scopes.
@@ -116,7 +120,7 @@ Use this only when the user explicitly asks for Claude review, e.g. `with Claude
 
 Default to one Claude challenge round; run two or three only when requested or when material unresolved risk remains. Each Claude challenge must name a claim, causal layer, why it matters, falsifying/satisfying evidence, and minimum impact threshold. If more than one challenge is raised, the first two challenges must use distinct causal layers; a single-challenge round must say why only one challenge is material. Codex reconciliation must classify each challenge as `Accepted`, `Risk added`, `Rejected`, `Uncertain`, or `No material impact`; `No material impact` is non-evidence: it proves a review ran, not that the artifact is acceptable. Bind the ledger to the artifact version/section reviewed.
 
-Before the skill-specific questions, include the Scope Fidelity Packet from `../references/claude-adversary.md` and require the reviewer to answer `Original-scope satisfaction`, `Narrowing approval`, and `Scope fidelity verdict` against the operator-original instruction. A reviewer must not assess only Codex's summary or proposed scope. Also require Claude to challenge whether Codex is sticking to the operator-approved plan and preserving modularity, thin harness / fat skills/tools, and agentic affordance unless the user explicitly overrides those defaults.
+Before the skill-specific questions, include the Scope Fidelity Packet from `../references/claude-adversary.md`: section 1 must be `coordination/<task-slug>/scope.md`; section 2 must be the diff/artifact under review; save the generated Claude prompt in that coordination folder. Require the reviewer to answer `Original-scope satisfaction`, `Narrowing approval`, and `Scope fidelity verdict` against the operator-original instruction. A reviewer must not assess only Codex's summary or proposed scope. Also require Claude to challenge whether Codex is sticking to the operator-approved plan and preserving modularity, thin harness / fat skills/tools, and agentic affordance unless the user explicitly overrides those defaults.
 
 Also include the Frame-independence / anti-roleplay check from `../references/claude-adversary.md`. The reviewer prompt must put the operator-original instruction first; if it is missing, Claude must stop and flag the review as invalid. Before any approval language, require Claude to state what role Codex is asking it to play and whether it accepts, modifies, or refuses that role; name what the operator's original instruction requires that Codex's summary might hide or narrow; and list three concrete reject conditions. Treat highly one-sided `Accepted`/`No material impact` ledgers as rubber-stamp warnings, not proof of quality. Model adversary review is reduced-noise, not zero-noise, and does not replace operator-defined observable success criteria, direct prompt/diff spot-checks, deterministic tests, evals, or receipts.
 
diff --git a/uberplan/SKILL.md b/uberplan/SKILL.md
index cb096b8..2d0bc5d 100644
--- a/uberplan/SKILL.md
+++ b/uberplan/SKILL.md
@@ -32,6 +32,10 @@ For product/rewrite/agentic-system work, first name the minimum user-visible pro
 
 For Type0, the default spine is: real feed/tip/wire input → normalized signal → admission decision → lane/story assignment → story processing → fact-check/publish/reject guard → traceable result.
 
+## Scope fidelity artifact gate
+
+Tier 1+ durable plans must include a `## Scope fidelity` block that links or quotes `coordination/<task-slug>/scope.md`, names the plan scope, states `Narrowing? yes/no`, and cites `Operator approved narrowing in:` whenever narrowed. Unapproved narrowing makes the plan invalid and cannot later count as completion; record it as blocked, deferred, or ask the operator to approve the narrower scope.
+
 ## Operational outcome contract
 
 Tier 1+ plans must include a **Definition of Done / Operational Outcome Contract** naming intended outcome, what counts as implemented/operational, evidence, non-implementation examples, and terminal state.
@@ -146,7 +150,7 @@ Use this only when the user explicitly asks for Claude review, e.g. `with Claude
 
 Default to one Claude challenge round; run two or three only when requested or when material unresolved risk remains. Each Claude challenge must name a claim, causal layer, why it matters, falsifying/satisfying evidence, and minimum impact threshold. If more than one challenge is raised, the first two challenges must use distinct causal layers; a single-challenge round must say why only one challenge is material. Codex reconciliation must classify each challenge as `Accepted`, `Risk added`, `Rejected`, `Uncertain`, or `No material impact`; `No material impact` is non-evidence: it proves a review ran, not that the artifact is acceptable. Bind the ledger to the artifact version/section reviewed.
 
-Before the skill-specific questions, include the Scope Fidelity Packet from `../references/claude-adversary.md` and require the reviewer to answer `Original-scope satisfaction`, `Narrowing approval`, and `Scope fidelity verdict` against the operator-original instruction. A reviewer must not assess only Codex's summary or proposed scope. Also require Claude to challenge whether Codex is sticking to the operator-approved plan and preserving modularity, thin harness / fat skills/tools, and agentic affordance unless the user explicitly overrides those defaults. For plan-phase review, require the Gall's Law / Basic Spine First adversary: think bigger about the ultimate goal and first principles, not bigger about architecture; identify the basic working spine, the thin/fat split, eval-driven evolution, what success is not, and the smallest next move.
+Before the skill-specific questions, include the Scope Fidelity Packet from `../references/claude-adversary.md`: section 1 must be `coordination/<task-slug>/scope.md`; section 2 must be the plan/diff/artifact under review; save the generated Claude prompt in that coordination folder. Require the reviewer to answer `Original-scope satisfaction`, `Narrowing approval`, and `Scope fidelity verdict` against the operator-original instruction. A reviewer must not assess only Codex's summary or proposed scope. Also require Claude to challenge whether Codex is sticking to the operator-approved plan and preserving modularity, thin harness / fat skills/tools, and agentic affordance unless the user explicitly overrides those defaults. For plan-phase review, require the Gall's Law / Basic Spine First adversary: think bigger about the ultimate goal and first principles, not bigger about architecture; identify the basic working spine, the thin/fat split, eval-driven evolution, what success is not, and the smallest next move.
 
 Also include the Frame-independence / anti-roleplay check from `../references/claude-adversary.md`. The reviewer prompt must put the operator-original instruction first; if it is missing, Claude must stop and flag the review as invalid. Before any approval language, require Claude to state what role Codex is asking it to play and whether it accepts, modifies, or refuses that role; name what the operator's original instruction requires that Codex's summary might hide or narrow; and list three concrete reject conditions. Treat highly one-sided `Accepted`/`No material impact` ledgers as rubber-stamp warnings, not proof of quality. Model adversary review is reduced-noise, not zero-noise, and does not replace operator-defined observable success criteria, direct prompt/diff spot-checks, deterministic tests, evals, or receipts.
 
diff --git a/uberplan/scripts/validate_plan_contract.py b/uberplan/scripts/validate_plan_contract.py
index 108f361..8771581 100755
--- a/uberplan/scripts/validate_plan_contract.py
+++ b/uberplan/scripts/validate_plan_contract.py
@@ -17,6 +17,7 @@ TIER_REQUIREMENTS = {
     "0": CORE_SECTIONS,
     "1": CORE_SECTIONS
     + [
+        "scope fidelity",
         "goal execution posture and delivery",
         "user expectation / surprise assessment",
         "definition of done / operational outcome contract",
@@ -29,6 +30,7 @@ TIER_REQUIREMENTS = {
     ],
     "2": CORE_SECTIONS
     + [
+        "scope fidelity",
         "goal execution posture and delivery",
         "user expectation / surprise assessment",
         "definition of done / operational outcome contract",
@@ -55,6 +57,7 @@ TIER_REQUIREMENTS = {
     ],
     "3": CORE_SECTIONS
     + [
+        "scope fidelity",
         "goal execution posture and delivery",
         "user expectation / surprise assessment",
         "definition of done / operational outcome contract",
diff --git a/uberplan/templates/plan-contract.md b/uberplan/templates/plan-contract.md
index 3174605..bb3895c 100644
--- a/uberplan/templates/plan-contract.md
+++ b/uberplan/templates/plan-contract.md
@@ -4,16 +4,19 @@
 
 State the concrete outcome and why it matters.
 
-## Scope Fidelity Ledger
+## Scope fidelity
 
-Use this to keep plans and second reviewers anchored to the operator's controlling instruction rather than the agent's compressed summary.
+This is the Scope Fidelity Ledger. Keep plans and second reviewers anchored to `coordination/<task-slug>/scope.md`, not the agent's compressed summary.
 
-- Operator original instruction, verbatim or exact artifact path:
-- Agent interpreted scope:
-- Proposed narrowed scope, if any:
+- Scope artifact: `coordination/<task-slug>/scope.md`
+- Original scope: quote or link to `scope.md` Operator original instruction
+- Plan scope:
+- Narrowing? yes/no
+- Operator approved narrowing in: quote/link required if narrowed
+- Approval evidence for narrowing/deferral: quote/link or n/a
+- Explicit constraints and later user scope changes checked: yes/no
 - Explicit deferrals / non-goals:
-- Approval evidence for each narrowing or deferral:
-- Diff between original and proposed scope:
+- If narrowing is unapproved, plan status: invalid / blocked / ask operator
 - Scope fidelity verdict before implementation: pass / fail / uncertain:
 
 ## Frame-independence / anti-roleplay check
diff --git a/uberplan/tests/fixtures/valid/tier2_agent_plan.md b/uberplan/tests/fixtures/valid/tier2_agent_plan.md
index 2e83027..f68937a 100644
--- a/uberplan/tests/fixtures/valid/tier2_agent_plan.md
+++ b/uberplan/tests/fixtures/valid/tier2_agent_plan.md
@@ -3,6 +3,19 @@
 ## Objective
 Improve a multi-agent handoff prompt so workers stop overwriting each other and return evidence-backed findings.
 
+
+## Scope fidelity
+
+- Scope artifact: `coordination/test-scope/scope.md`
+- Original scope: `coordination/test-scope/scope.md` original operator instruction.
+- Plan scope: maintain the skill-package behavior described in the objective.
+- Narrowing? no
+- Operator approved narrowing in: n/a
+- Explicit constraints and later user scope changes checked: yes
+- Explicit deferrals / non-goals: no unapproved deferrals.
+- If narrowing is unapproved, plan status: invalid / blocked / ask operator.
+- Scope fidelity verdict before implementation: pass
+
 ## Scope
 In scope: one skill prompt, one agent brief template, validator fixture updates. Out of scope: live runtime changes, commits, pushes, or production writes.
 
diff --git a/uberplan/tests/fixtures/valid/tier3_expensive_proof_plan_tree.md b/uberplan/tests/fixtures/valid/tier3_expensive_proof_plan_tree.md
index 7b0ed42..81306a3 100644
--- a/uberplan/tests/fixtures/valid/tier3_expensive_proof_plan_tree.md
+++ b/uberplan/tests/fixtures/valid/tier3_expensive_proof_plan_tree.md
@@ -3,6 +3,19 @@
 ## Objective
 Harden a Tier 3 agentic runtime production replacement proof with child plan files before burn-in and final proof.
 
+
+## Scope fidelity
+
+- Scope artifact: `coordination/test-scope/scope.md`
+- Original scope: `coordination/test-scope/scope.md` original operator instruction.
+- Plan scope: maintain the skill-package behavior described in the objective.
+- Narrowing? no
+- Operator approved narrowing in: n/a
+- Explicit constraints and later user scope changes checked: yes
+- Explicit deferrals / non-goals: no unapproved deferrals.
+- If narrowing is unapproved, plan status: invalid / blocked / ask operator.
+- Scope fidelity verdict before implementation: pass
+
 ## Scope
 In scope: risk/failure inventory, observability preflight, phase-boundary contract-fuzz preflight, child status ledger, burn-in proof, and separate final proof for a production replacement run. Out of scope: launching the final proof before burn-in passes.
 
diff --git a/uberplan/tests/test_validators.py b/uberplan/tests/test_validators.py
index 047cc32..da4e8e4 100644
--- a/uberplan/tests/test_validators.py
+++ b/uberplan/tests/test_validators.py
@@ -167,6 +167,17 @@ class PlanValidatorTests(unittest.TestCase):
             plan.write_text(text[:start] + text[end:])
             self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")
 
+    def test_tier2_requires_scope_fidelity(self) -> None:
+        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
+        start = text.index("## Scope fidelity")
+        end = text.index("## Scope\n", start + 1)
+        with tempfile.TemporaryDirectory() as tmp:
+            plan = Path(tmp) / "missing_scope_fidelity.md"
+            plan.write_text(text[:start] + text[end:])
+            result = run_cmd(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")
+            self.assertNotEqual(result.returncode, 0, "unexpected pass\n" + result.stdout)
+            self.assertIn("scope fidelity", result.stderr)
+
     def test_tier2_requires_goal_execution_posture(self) -> None:
         text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
         start = text.index("## Goal execution posture and delivery")

## Review request
Answer before any approval language:
1. Invited role: what role is Codex asking you to play, and do you accept/modify/refuse it?
2. Original-vs-summary gap: what does the operator original instruction require that this patch might hide, narrow, or skip?
3. Reject conditions: name three concrete outcomes that would make you reject this patch.

Then give challenges using causal layer, why it matters, falsifying/satisfying evidence, and minimum impact. Specifically check:
- Does the patch materially prevent scope laundering beyond another reminder line?
- Does it keep semantic judgment with the agent/reviewer and structural checks with the validator?
- Are ubergoal/uberplan/uberaccept/template/validator/test changes sufficient and surgical?
- Are there any missing required artifacts from the operator prompt?

Final gate: Ship yes/no within this patch scope, one sentence.
