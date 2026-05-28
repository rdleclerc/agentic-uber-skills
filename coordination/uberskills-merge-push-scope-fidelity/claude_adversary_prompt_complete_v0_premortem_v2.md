# Claude adversarial review prompt — V0 premortem v2 after applying prior review fix

You are reviewing Codex changes. Section 1 is the durable scope artifact; Section 2 is the actual diff/artifact set. This v2 prompt includes the fix made after prior Claude feedback: the V0 premortem validator no longer forces the verdict to start with pass, and includes a regression proving replan is structurally allowed.

Review questions: Does this now satisfy the operator scope addition? Are there any remaining blockers? Is it surgical and does it cover overengineering/code-bloat without creating process bloat?

## Section 1 — scope.md

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

### 2026-05-28T12:58:00-0700 — Operator scope addition: V0 premortem / Claude recs / overengineering

```text
"I slightly disagree with Claude’s wording “make the adversary question mandatory” if that implies mandatory external Claude review. I’d make the premortem block mandatory, while external Claude stays optional unless requested." -- disagree...  okay include the overengineering part and claudes recs, use uberskills and claude to build
```

- Scope change: extend the in-progress Uber skills patch to add a durable `uberplan` V0 premortem / failure-disposition gate, including overengineering/code-bloat failure analysis and Claude's recommendation that adversary failure questions become load-bearing for Tier 2+ plans.
- Constraint preserved: keep the change surgical; do not create a new top-level skill; avoid broad ceremony or semantic deterministic judgment.
- Review requirement: use Claude OAuth review on the actual updated artifacts, with prompt saved in the coordination folder.


## Section 2 — actual artifact/diff under review

### Git status

```text
## session/uberskills-merge-push-scope-fidelity
 M references/claude-adversary.md
 M uberaccept/SKILL.md
 M uberaccept/scripts/validate_acceptance_report.py
 M uberaccept/templates/final-acceptance.md
 M uberaccept/tests/fixtures/valid/final_acceptance.md
 M uberaccept/tests/fixtures/valid/production_hard_blocked_acceptance.md
 M uberaccept/tests/test_validators.py
 M ubergoal/SKILL.md
 M uberplan/SKILL.md
 M uberplan/scripts/validate_plan_contract.py
 M uberplan/templates/confidence-gate.md
 M uberplan/templates/plan-contract.md
 M uberplan/tests/fixtures/valid/tier2_agent_plan.md
 M uberplan/tests/fixtures/valid/tier3_expensive_proof_plan_tree.md
 M uberplan/tests/test_validators.py
?? coordination/
?? scripts/check_scope_fidelity_artifacts.py
?? tests/fixtures/
?? tests/test_scope_fidelity_artifacts.py
?? ubergoal/templates/scope.md
```

### Tracked-file diff

```diff
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
index cb096b8..138aed9 100644
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
@@ -106,6 +110,12 @@ Choose lanes by risk, not ceremony: Architecture Steward; **Agent Advocate / Age
 
 Do not create a standalone `ubertesting`/`ubereval` plan lane merely because testing is important; use the red/green proof ledger and Black-box Tester / Quality-Eval Auditor first, and extract only after repeated failures prove benefit >> cost.
 
+## V0 plan premortem / failure dispositions
+
+For Tier 2/3 plans, after drafting the first concrete plan and before the confidence gate, run an explicit premortem against that V0 plan. This is a required plan artifact, not a reminder. Ask the adversary questions even when no separate reviewer is available; if Claude or another adversarial reviewer is requested or available for the plan review, use that reviewer and save the prompt/output with the coordination artifacts.
+
+The premortem must assume the V0 plan failed, then name: the most likely execution failure, missing affordance/context/tool/source, overengineering or code-bloat failure mode, files/modules/abstractions proposed, what can be deleted/merged/avoided, and the 80/50 alternative that gets most value with much less surface area. Every material failure mode needs a failure disposition: either a concrete plan revision, or an explicit accepted-risk rationale. Do not pass the confidence gate with unresolved premortem blockers or with findings that did not mutate the plan or risk ledger.
+
 ## Parallel exploration and execution planning
 
 Map the critical path before parallel work. If subagents are authorized, split exploration into non-overlapping slices and require trails: key files, invariants, commands/tests, unknowns, false leads, next angles. Even without subagents, identify parallelizable work, serial blockers, disjoint write scopes, and batching/max-concurrency policy. Do not spawn duplicate agents over the same context.
@@ -146,7 +156,7 @@ Use this only when the user explicitly asks for Claude review, e.g. `with Claude
 
 Default to one Claude challenge round; run two or three only when requested or when material unresolved risk remains. Each Claude challenge must name a claim, causal layer, why it matters, falsifying/satisfying evidence, and minimum impact threshold. If more than one challenge is raised, the first two challenges must use distinct causal layers; a single-challenge round must say why only one challenge is material. Codex reconciliation must classify each challenge as `Accepted`, `Risk added`, `Rejected`, `Uncertain`, or `No material impact`; `No material impact` is non-evidence: it proves a review ran, not that the artifact is acceptable. Bind the ledger to the artifact version/section reviewed.
 
-Before the skill-specific questions, include the Scope Fidelity Packet from `../references/claude-adversary.md` and require the reviewer to answer `Original-scope satisfaction`, `Narrowing approval`, and `Scope fidelity verdict` against the operator-original instruction. A reviewer must not assess only Codex's summary or proposed scope. Also require Claude to challenge whether Codex is sticking to the operator-approved plan and preserving modularity, thin harness / fat skills/tools, and agentic affordance unless the user explicitly overrides those defaults. For plan-phase review, require the Gall's Law / Basic Spine First adversary: think bigger about the ultimate goal and first principles, not bigger about architecture; identify the basic working spine, the thin/fat split, eval-driven evolution, what success is not, and the smallest next move.
+Before the skill-specific questions, include the Scope Fidelity Packet from `../references/claude-adversary.md`: section 1 must be `coordination/<task-slug>/scope.md`; section 2 must be the plan/diff/artifact under review; save the generated Claude prompt in that coordination folder. Require the reviewer to answer `Original-scope satisfaction`, `Narrowing approval`, and `Scope fidelity verdict` against the operator-original instruction. A reviewer must not assess only Codex's summary or proposed scope. Also require Claude to challenge whether Codex is sticking to the operator-approved plan and preserving modularity, thin harness / fat skills/tools, and agentic affordance unless the user explicitly overrides those defaults. For plan-phase review, require the Gall's Law / Basic Spine First adversary: think bigger about the ultimate goal and first principles, not bigger about architecture; identify the basic working spine, the thin/fat split, eval-driven evolution, what success is not, and the smallest next move.
 
 Also include the Frame-independence / anti-roleplay check from `../references/claude-adversary.md`. The reviewer prompt must put the operator-original instruction first; if it is missing, Claude must stop and flag the review as invalid. Before any approval language, require Claude to state what role Codex is asking it to play and whether it accepts, modifies, or refuses that role; name what the operator's original instruction requires that Codex's summary might hide or narrow; and list three concrete reject conditions. Treat highly one-sided `Accepted`/`No material impact` ledgers as rubber-stamp warnings, not proof of quality. Model adversary review is reduced-noise, not zero-noise, and does not replace operator-defined observable success criteria, direct prompt/diff spot-checks, deterministic tests, evals, or receipts.
 
@@ -154,7 +164,8 @@ For `uberplan`, ask exactly:
 
 1. **Most likely execution failure.** Causal layer: failure prediction. Name the single most likely execution failure and its mitigation, not just acknowledgment. Evidence: tie it to a prior failure/source constraint. Minimum impact: add a stop gate or remove the risky branch.
 2. **Missing affordance.** Causal layer: agent affordance/tooling. What skill, tool, source, or context does this plan depend on that does not exist or is unproven? Evidence: identify the exact missing affordance. Minimum impact: add proof/fallback or remove dependency.
-3. **Linear 80/50 alternative.** Causal layer: simplification. Is there a linear no-branch version that gets at least 80% of the value with at most 50% of the surface? Evidence: describe it. Minimum impact: replace the plan or justify complexity.
+3. **Overengineering / code-bloat failure.** Causal layer: complexity and topology. If this plan fails by adding too much machinery, too many files, or the wrong abstraction, what caused it? Evidence: name proposed files/modules/abstractions and what can be deleted, merged, or avoided. Minimum impact: simplify the plan or explicitly accept the bloat risk.
+4. **Linear 80/50 alternative.** Causal layer: simplification. Is there a linear no-branch version that gets at least 80% of the value with at most 50% of the surface? Evidence: describe it. Minimum impact: replace the plan or justify complexity.
 
 ## Helpful resources
 
diff --git a/uberplan/scripts/validate_plan_contract.py b/uberplan/scripts/validate_plan_contract.py
index 108f361..ea803fd 100755
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
@@ -29,11 +30,13 @@ TIER_REQUIREMENTS = {
     ],
     "2": CORE_SECTIONS
     + [
+        "scope fidelity",
         "goal execution posture and delivery",
         "user expectation / surprise assessment",
         "definition of done / operational outcome contract",
         "product / prd checklist",
         "task map / implementation graph",
+        "v0 plan premortem",
         "verifiable subgoals and metrics",
         "parallelization plan",
         "runtime agent topology / codex depth-thread policy",
@@ -55,11 +58,13 @@ TIER_REQUIREMENTS = {
     ],
     "3": CORE_SECTIONS
     + [
+        "scope fidelity",
         "goal execution posture and delivery",
         "user expectation / surprise assessment",
         "definition of done / operational outcome contract",
         "product / prd checklist",
         "task map / implementation graph",
+        "v0 plan premortem",
         "verifiable subgoals and metrics",
         "parallelization plan",
         "runtime agent topology / codex depth-thread policy",
@@ -204,7 +209,7 @@ def table_meaningful_rows(section: str) -> list[list[str]]:
         cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
         if not cells or all(not cell or set(cell) <= {"-", ":"} for cell in cells):
             continue
-        headerish = {"surface", "dimension", "risk/failure mode", "agent role", "deterministic harness owns"}
+        headerish = {"surface", "dimension", "risk/failure mode", "failure mode", "agent role", "deterministic harness owns"}
         if cells[0].strip().lower() in headerish:
             continue
         if any(cell for cell in cells) and not all(cell in {"", " ", "-"} for cell in cells):
@@ -533,6 +538,41 @@ def validate_task_map(found: dict[str, str], tier: str, errors: list[str]) -> No
             errors.append(f"Task map / implementation graph missing concept: {term}")
 
 
+def validate_v0_plan_premortem(found: dict[str, str], tier: str, errors: list[str]) -> None:
+    if tier not in {"2", "3"}:
+        return
+    section_name = "v0 plan premortem"
+    section = found.get(section_name, "")
+    if not section:
+        return
+    if not section_has_substance(section):
+        errors.append("required section lacks completed substance: V0 plan premortem")
+        return
+    for label in [
+        "V0 plan artifact/version reviewed",
+        "Premortem reviewer",
+        "Assumed failure summary",
+        "Most likely execution failure",
+        "Missing affordance/context/tool/source",
+        "Overengineering or code-bloat failure mode",
+        "Files/modules/abstractions proposed",
+        "What can be deleted, merged, avoided, or postponed",
+        "Linear 80/50 alternative",
+        "Required plan changes before implementation",
+        "Accepted risks with rationale",
+        "Premortem gate verdict",
+    ]:
+        require_field(section, label, errors)
+
+    section_lower = normalize(section)
+    for term in ["overengineering", "code-bloat", "80/50", "plan revision", "accepted risk"]:
+        if term not in section_lower:
+            errors.append(f"V0 plan premortem missing concept: {term}")
+    rows = table_meaningful_rows(section)
+    if not rows:
+        errors.append("V0 plan premortem needs at least one failure-disposition row")
+
+
 
 DEAD_CODE_TOOL_TERMS = [
     "vulture",
@@ -1338,6 +1378,7 @@ def main() -> int:
 
     validate_prd_checklist(found, args.tier or "1", errors)
     validate_task_map(found, args.tier or "1", errors)
+    validate_v0_plan_premortem(found, args.tier or "1", errors)
     validate_verifiable_subgoals(found, args.tier or "1", errors)
     validate_parallelization_plan(found, args.tier or "1", errors)
     validate_testing_adaptation_gate(found, args.tier or "1", errors)
diff --git a/uberplan/templates/confidence-gate.md b/uberplan/templates/confidence-gate.md
index cec0759..4d0559d 100644
--- a/uberplan/templates/confidence-gate.md
+++ b/uberplan/templates/confidence-gate.md
@@ -21,6 +21,8 @@ Check:
 - For model-output boundaries, did the plan prove shape, authority, isolation, failure semantics, observability, and replay/eval evidence rather than listing generic reliability words?
 - Are regexes, keyword lists, and string matchers limited to mechanical parsing or candidate signals, with no unapproved semantic authority over natural language?
 - Has the Loophole Hunter found any unresolved blockers?
+- For Tier 2/3, did the V0 plan premortem run after the first concrete plan, and did every material failure mode receive either a plan revision or explicit accepted-risk rationale?
+- Did the premortem challenge overengineering/code-bloat, proposed new files/modules/abstractions, what can be deleted/merged/avoided, and the 80/50 alternative?
 - Has the Simplifier found a smaller/elegant path that should replace this plan?
 - Has the Codebase Scout checked existing patterns/tests/claims when the repo is nontrivial?
 - Has the OpenClaw/Platform Steward checked local policy when OpenClaw/Type0/runtime is touched?
diff --git a/uberplan/templates/plan-contract.md b/uberplan/templates/plan-contract.md
index 3174605..1cf980d 100644
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
@@ -221,6 +224,28 @@ flowchart TD
 | T2 |  | T1 |  |  |  |  |
 | T3 |  | T1 |  |  |  |  |
 
+## V0 plan premortem
+
+Required for Tier 2/3 after the first concrete plan/task map is drafted and before the confidence gate. Assume the V0 plan failed. The purpose is to revise the plan, not to generate a risk list that can be ignored.
+
+- V0 plan artifact/version reviewed:
+- Premortem reviewer: main agent / Claude / other adversarial reviewer:
+- If Claude/reviewer was requested or available, prompt/output path:
+- Assumed failure summary:
+- Most likely execution failure:
+- Missing affordance/context/tool/source:
+- Overengineering or code-bloat failure mode:
+- Files/modules/abstractions proposed:
+- What can be deleted, merged, avoided, or postponed:
+- Linear 80/50 alternative:
+- Required plan changes before implementation:
+- Accepted risks with rationale:
+- Premortem gate verdict: pass / block / replan:
+
+| Failure mode | Disposition: plan revision / accepted risk | Plan change or accepted-risk rationale | Status |
+|---|---|---|---|
+|  |  |  |  |
+
 ## Verifiable subgoals and metrics
 
 For Tier 1+ work, convert the objective into high-quality subgoals. Every subgoal needs observable evidence; use quantitative scores where useful, but allow qualitative rubrics when judgment is the product.
diff --git a/uberplan/tests/fixtures/valid/tier2_agent_plan.md b/uberplan/tests/fixtures/valid/tier2_agent_plan.md
index 2e83027..e03246d 100644
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
 
@@ -68,6 +81,28 @@ flowchart TD
 | T4 | Preserve real bug as eval seed | T1 | eval owner | evals/golden_skill_invocations.json | recurring overwrite bug is captured as replayable fixture | eval schema test output |
 | T5 | Acceptance review and report | T2, T3, T4 | integrator | no new writes except report | all goals satisfy acceptance rubric | unittest, package lint, and acceptance summary |
 
+## V0 plan premortem
+
+- V0 plan artifact/version reviewed: v0 task map and implementation graph above.
+- Premortem reviewer: main agent running the required adversary failure questions; no separate reviewer for this fixture.
+- If Claude/reviewer was requested or available, prompt/output path: not requested for this fixture; no external prompt/output path.
+- Assumed failure summary: the plan fails by adding ownership ceremony that agents ignore or by overbuilding a coordination harness instead of fixing the contract.
+- Most likely execution failure: agents still edit shared files without disjoint write sets; mitigation is to revise the plan to require validator-backed ownership and return-contract evidence.
+- Missing affordance/context/tool/source: missing fixture-backed validator and agent brief contract; mitigation is to add them before implementation.
+- Overengineering or code-bloat failure mode: creating a new skill, router, or orchestration layer for ownership instead of a small template and validator contract.
+- Files/modules/abstractions proposed: no new top-level skill or harness; only existing `uberplan` skill text, template, validator, and targeted fixtures.
+- What can be deleted, merged, avoided, or postponed: avoid new orchestration, merge guidance into existing sections, postpone fresh-agent automated eval harness.
+- Linear 80/50 alternative: one ownership/evidence block plus one validator fixture gets most of the safety with much less surface area.
+- Required plan changes before implementation: keep the patch inside existing `uberplan` files and make the validator fixture fail before adding broader machinery.
+- Accepted risks with rationale: accepted risk that fresh-agent automated eval remains deferred because the structural validator catches the known recurrence cheaply.
+- Premortem gate verdict: pass; material blockers were converted into plan revision or accepted risk rows.
+
+| Failure mode | Disposition: plan revision / accepted risk | Plan change or accepted-risk rationale | Status |
+|---|---|---|---|
+| ownership ceremony ignored | plan revision | require validator-backed ownership evidence in the existing contract | revised |
+| overbuilt coordination harness | plan revision | avoid new skill/router/harness and patch existing template plus validator only | revised |
+| fresh-agent eval missing | accepted risk | defer automated eval harness because targeted fixture covers the known failure class | accepted |
+
 ## Verifiable subgoals and metrics
 
 | Subgoal ID | Outcome | Acceptance evidence | Metric / score / rubric | Owner | Parallelizable? | Done when |
diff --git a/uberplan/tests/fixtures/valid/tier3_expensive_proof_plan_tree.md b/uberplan/tests/fixtures/valid/tier3_expensive_proof_plan_tree.md
index 7b0ed42..f58b0de 100644
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
 
@@ -123,6 +136,28 @@ flowchart TD
 | T4 | Preserve real bug as eval seed | T1 | eval owner | evals/golden_skill_invocations.json | recurring overwrite bug is captured as replayable fixture | eval schema test output |
 | T5 | Acceptance review and report | T2, T3, T4 | integrator | no new writes except report | all goals satisfy acceptance rubric | unittest, package lint, and acceptance summary |
 
+## V0 plan premortem
+
+- V0 plan artifact/version reviewed: v0 task map and implementation graph above.
+- Premortem reviewer: main agent running the required adversary failure questions; no separate reviewer for this fixture.
+- If Claude/reviewer was requested or available, prompt/output path: not requested for this fixture; no external prompt/output path.
+- Assumed failure summary: the plan fails by adding ownership ceremony that agents ignore or by overbuilding a coordination harness instead of fixing the contract.
+- Most likely execution failure: agents still edit shared files without disjoint write sets; mitigation is to revise the plan to require validator-backed ownership and return-contract evidence.
+- Missing affordance/context/tool/source: missing fixture-backed validator and agent brief contract; mitigation is to add them before implementation.
+- Overengineering or code-bloat failure mode: creating a new skill, router, or orchestration layer for ownership instead of a small template and validator contract.
+- Files/modules/abstractions proposed: no new top-level skill or harness; only existing `uberplan` skill text, template, validator, and targeted fixtures.
+- What can be deleted, merged, avoided, or postponed: avoid new orchestration, merge guidance into existing sections, postpone fresh-agent automated eval harness.
+- Linear 80/50 alternative: one ownership/evidence block plus one validator fixture gets most of the safety with much less surface area.
+- Required plan changes before implementation: keep the patch inside existing `uberplan` files and make the validator fixture fail before adding broader machinery.
+- Accepted risks with rationale: accepted risk that fresh-agent automated eval remains deferred because the structural validator catches the known recurrence cheaply.
+- Premortem gate verdict: pass; material blockers were converted into plan revision or accepted risk rows.
+
+| Failure mode | Disposition: plan revision / accepted risk | Plan change or accepted-risk rationale | Status |
+|---|---|---|---|
+| ownership ceremony ignored | plan revision | require validator-backed ownership evidence in the existing contract | revised |
+| overbuilt coordination harness | plan revision | avoid new skill/router/harness and patch existing template plus validator only | revised |
+| fresh-agent eval missing | accepted risk | defer automated eval harness because targeted fixture covers the known failure class | accepted |
+
 ## Verifiable subgoals and metrics
 
 | Subgoal ID | Outcome | Acceptance evidence | Metric / score / rubric | Owner | Parallelizable? | Done when |
diff --git a/uberplan/tests/test_validators.py b/uberplan/tests/test_validators.py
index 047cc32..fed6e6b 100644
--- a/uberplan/tests/test_validators.py
+++ b/uberplan/tests/test_validators.py
@@ -75,6 +75,39 @@ class PlanValidatorTests(unittest.TestCase):
             plan.write_text(text[:start] + text[end:])
             self.assertFails(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")
 
+    def test_tier2_requires_v0_plan_premortem(self) -> None:
+        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
+        start = text.index("## V0 plan premortem")
+        end = text.index("## Verifiable subgoals and metrics")
+        with tempfile.TemporaryDirectory() as tmp:
+            plan = Path(tmp) / "missing_v0_plan_premortem.md"
+            plan.write_text(text[:start] + text[end:])
+            result = run_cmd(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")
+            self.assertNotEqual(result.returncode, 0, "unexpected pass\n" + result.stdout)
+            self.assertIn("v0 plan premortem", result.stderr.lower())
+
+    def test_tier2_v0_plan_premortem_requires_failure_dispositions(self) -> None:
+        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
+        start = text.index("| ownership ceremony ignored |")
+        end = text.index("## Verifiable subgoals and metrics")
+        with tempfile.TemporaryDirectory() as tmp:
+            plan = Path(tmp) / "missing_failure_dispositions.md"
+            plan.write_text(text[:start] + "\n" + text[end:])
+            result = run_cmd(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")
+            self.assertNotEqual(result.returncode, 0, "unexpected pass\n" + result.stdout)
+            self.assertIn("failure-disposition", result.stderr.lower())
+
+    def test_tier2_v0_plan_premortem_allows_replan_verdict_structurally(self) -> None:
+        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
+        text = text.replace(
+            "Premortem gate verdict: pass; material blockers were converted into plan revision or accepted risk rows.",
+            "Premortem gate verdict: replan; V0 issues were converted into the revised final contract and disposition rows.",
+        )
+        with tempfile.TemporaryDirectory() as tmp:
+            plan = Path(tmp) / "replan_premortem_verdict.md"
+            plan.write_text(text)
+            self.assertPasses(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")
+
     def test_tier2_requires_verifiable_subgoals(self) -> None:
         text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
         start = text.index("## Verifiable subgoals and metrics")
@@ -167,6 +200,17 @@ class PlanValidatorTests(unittest.TestCase):
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

```

### New untracked files intended for the patch

#### New file: `scripts/check_scope_fidelity_artifacts.py`

```python
#!/usr/bin/env python3
"""Presence/order checks for Uber scope-fidelity artifacts.

This is intentionally non-semantic: it does not compare original scope to
implemented scope. It only verifies that the durable scope artifact exists,
that plans/acceptance reports expose required fields, and that ship language
cannot appear before the scope-fidelity verdict.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PLACEHOLDERS = {
    "",
    "todo",
    "tbd",
    "n/a",
    "na",
    "none",
    "no",
    "yes/no",
    "quote/link required",
    "required if narrowed",
}


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def non_empty_citation(value: str) -> bool:
    cleaned = normalize(value).strip("[]()<>` ")
    return cleaned not in PLACEHOLDERS


def read(path: Path, errors: list[str], label: str) -> str:
    try:
        return path.read_text()
    except FileNotFoundError:
        errors.append(f"{label} missing: {path}")
    except OSError as exc:
        errors.append(f"{label} unreadable: {path}: {exc}")
    return ""


def check_ship_order(text: str, errors: list[str], path: Path) -> None:
    match = re.search(r"^##\s+Scope fidelity verdict\s*$", text, flags=re.I | re.M)
    if not match:
        errors.append(f"acceptance/final report lacks ## Scope fidelity verdict: {path}")
        return
    before = text[: match.start()]
    if re.search(r"\bship\b", before, flags=re.I):
        errors.append(f"SHIP/ship language appears before scope-fidelity verdict: {path}")


def approval_after_narrowing(lines: list[str], index: int) -> bool:
    window = lines[index : min(len(lines), index + 10)]
    for line in window:
        match = re.match(
            r"^\s*-\s*(?:Operator approved narrowing in|Approval evidence[^:]*)\s*:\s*(.+?)\s*$",
            line,
            flags=re.I,
        )
        if match and non_empty_citation(match.group(1)):
            return True
    return False


def check_narrowing_approval(text: str, errors: list[str], path: Path) -> None:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if re.match(r"^\s*-\s*Narrowing\?\s*(?::\s*)?yes\b", line, flags=re.I):
            if not approval_after_narrowing(lines, idx):
                errors.append(f"Narrowing? yes lacks non-empty approval citation: {path}:{idx + 1}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", type=Path, required=True, help="coordination/<task-slug>/scope.md")
    parser.add_argument("--plan", type=Path, action="append", default=[], help="durable plan file to inspect")
    parser.add_argument("--acceptance", type=Path, action="append", default=[], help="final acceptance/report file to inspect")
    args = parser.parse_args()

    errors: list[str] = []
    if not args.scope.exists():
        errors.append(f"scope.md missing: {args.scope}")
    elif not args.scope.is_file():
        errors.append(f"scope path is not a file: {args.scope}")

    for plan in args.plan:
        text = read(plan, errors, "plan")
        if text:
            if not re.search(r"^##\s+Scope fidelity\s*$", text, flags=re.I | re.M):
                errors.append(f"plan lacks ## Scope fidelity block: {plan}")
            check_narrowing_approval(text, errors, plan)

    for acceptance in args.acceptance:
        text = read(acceptance, errors, "acceptance")
        if text:
            check_ship_order(text, errors, acceptance)
            check_narrowing_approval(text, errors, acceptance)

    if errors:
        print("FAIL: scope fidelity artifact checks failed", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("PASS: scope fidelity artifact checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

#### New file: `ubergoal/templates/scope.md`

```markdown
# Scope Artifact

Task slug: `<task-slug>`
Created: `<YYYY-MM-DDTHH:MM:SS±TZ>`
Owner/session: `<agent/session>`

## Original operator instruction

Paste the operator's controlling instruction verbatim. If the instruction is too long or sensitive, give an exact artifact path and a short redaction note; do not replace it with an agent summary.

```text
<verbatim operator instruction>
```

## Explicit constraints and non-goals from original instruction

- Constraint:
- Non-goal:

## Scope change ledger

Append later user scope changes here. Do not overwrite or edit the original instruction above.

### <YYYY-MM-DDTHH:MM:SS±TZ> — initial capture

- Source: original operator instruction
- Change type: initial / clarification / expansion / narrowing / deferral
- User instruction or artifact path:
- Effect on scope:
- Approval evidence for narrowing/deferral: n/a for initial capture
```

#### New file: `tests/test_scope_fidelity_artifacts.py`

```python
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECK = ROOT / "scripts" / "check_scope_fidelity_artifacts.py"
FIX = ROOT / "tests" / "fixtures" / "scope_fidelity"


def run_check(case: str, *, missing_scope: bool = False) -> subprocess.CompletedProcess[str]:
    case_dir = FIX / case
    scope = case_dir / ("missing-scope.md" if missing_scope else "scope.md")
    return subprocess.run(
        [
            sys.executable,
            str(CHECK),
            "--scope",
            str(scope),
            "--plan",
            str(case_dir / "plan.md"),
            "--acceptance",
            str(case_dir / "final.md"),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


class ScopeFidelityArtifactTests(unittest.TestCase):
    def test_missing_scope_file_fails(self) -> None:
        result = run_check("approved_narrowing", missing_scope=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("scope.md missing", result.stderr)

    def test_unapproved_slack_only_narrowing_fails(self) -> None:
        result = run_check("unapproved_narrowing")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Narrowing? yes lacks non-empty approval citation", result.stderr)

    def test_operator_approved_narrowing_passes(self) -> None:
        result = run_check("approved_narrowing")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_ship_before_scope_verdict_fails(self) -> None:
        result = run_check("ship_before_verdict")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("appears before scope-fidelity verdict", result.stderr)


if __name__ == "__main__":
    unittest.main()
```

#### New file: `tests/fixtures/scope_fidelity/unapproved_narrowing/scope.md`

```markdown
# Scope Artifact

## Original operator instruction

```text
Run a codebase-wide OpenClaw ownership audit and implement the necessary ownership fixes.
```

## Scope change ledger

### 2026-05-28T08:00:00-0700 — initial capture

- Source: original operator instruction
- Change type: initial
- User instruction or artifact path: prompt above
- Effect on scope: codebase-wide audit and implementation remain required
- Approval evidence for narrowing/deferral: n/a
```

#### New file: `tests/fixtures/scope_fidelity/unapproved_narrowing/plan.md`

```markdown
# Plan

## Scope fidelity

- Scope artifact: `scope.md`
- Original scope: codebase-wide OpenClaw ownership audit and implementation
- Plan scope: Slack transcript patch only
- Narrowing? yes
- Operator approved narrowing in:
- If narrowing is unapproved, plan status: invalid / blocked / ask operator
```

#### New file: `tests/fixtures/scope_fidelity/unapproved_narrowing/final.md`

```markdown
# Final Acceptance Report

## Scope fidelity verdict

- Scope artifact: `scope.md`
- Original scope: codebase-wide OpenClaw ownership audit and implementation
- Implemented scope: Slack transcript patch only
- Does implemented scope satisfy original scope? no
- Narrowing? yes
- Operator approved narrowing in:
- Unapproved narrowing blocker? yes
- Scope fidelity verdict: fail
```

#### New file: `tests/fixtures/scope_fidelity/approved_narrowing/scope.md`

```markdown
# Scope Artifact

## Original operator instruction

```text
Run a codebase-wide OpenClaw ownership audit and implement the necessary ownership fixes.
```

## Scope change ledger

### 2026-05-28T08:05:00-0700 — operator-approved narrowing

- Source: user reply
- Change type: narrowing
- User instruction or artifact path: "Start by narrowing this to Slack ownership; codebase-wide audit is deferred."
- Effect on scope: Slack ownership patch is acceptable for this run
- Approval evidence for narrowing/deferral: user reply 2026-05-28T08:05:00-0700
```

#### New file: `tests/fixtures/scope_fidelity/approved_narrowing/plan.md`

```markdown
# Plan

## Scope fidelity

- Scope artifact: `scope.md`
- Original scope: codebase-wide OpenClaw ownership audit and implementation
- Plan scope: Slack ownership patch only
- Narrowing? yes
- Operator approved narrowing in: user reply 2026-05-28T08:05:00-0700
- If narrowing is unapproved, plan status: invalid / blocked / ask operator
```

#### New file: `tests/fixtures/scope_fidelity/approved_narrowing/final.md`

```markdown
# Final Acceptance Report

## Scope fidelity verdict

- Scope artifact: `scope.md`
- Original scope: codebase-wide OpenClaw ownership audit and implementation
- Implemented scope: Slack ownership patch only
- Does implemented scope satisfy original scope? partial, via approved narrowing
- Narrowing? yes
- Operator approved narrowing in: user reply 2026-05-28T08:05:00-0700
- Unapproved narrowing blocker? no
- Scope fidelity verdict: pass

SHIP: yes within approved narrowed scope.
```

#### New file: `tests/fixtures/scope_fidelity/ship_before_verdict/scope.md`

```markdown
# Scope Artifact

## Original operator instruction

```text
Run a codebase-wide OpenClaw ownership audit and implement the necessary ownership fixes.
```
```

#### New file: `tests/fixtures/scope_fidelity/ship_before_verdict/plan.md`

```markdown
# Plan

## Scope fidelity

- Scope artifact: `scope.md`
- Original scope: codebase-wide OpenClaw ownership audit and implementation
- Plan scope: codebase-wide OpenClaw ownership audit and implementation
- Narrowing? no
- Operator approved narrowing in: n/a
```

#### New file: `tests/fixtures/scope_fidelity/ship_before_verdict/final.md`

```markdown
# Final Acceptance Report

SHIP: yes, ready.

## Scope fidelity verdict

- Scope artifact: `scope.md`
- Original scope: codebase-wide OpenClaw ownership audit and implementation
- Implemented scope: codebase-wide OpenClaw ownership audit and implementation
- Does implemented scope satisfy original scope? yes
- Narrowing? no
- Operator approved narrowing in: n/a
- Scope fidelity verdict: pass
```

