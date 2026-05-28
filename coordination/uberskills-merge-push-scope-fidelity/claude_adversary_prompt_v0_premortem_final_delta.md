# Claude delta review — final V0 premortem false-positive fix

Section 1 is scope.md. Section 2 is the current uberplan diff relevant to the V0 premortem update. Prior Claude review flagged that `plan revision` might be over-required even though accepted-risk-only dispositions should be valid. I patched the validator to allow accepted-risk-only disposition rows and added a regression test. Review only whether that prior residual is resolved and whether any blocker remains in this V0 premortem change.

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


## Section 2 — current V0 premortem diff

```diff
diff --git a/uberplan/SKILL.md b/uberplan/SKILL.md
index cb096b8..84acd43 100644
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
+The premortem must assume the V0 plan failed, then name: the most likely execution failure, missing affordance/context/tool/source, overengineering or code-bloat failure mode, files/modules/abstractions proposed, what can be deleted/merged/avoided, and the 80/50 alternative that gets most value with much less surface area. Every material failure mode needs a failure disposition: either a concrete plan revision, or an explicit accepted-risk rationale; accepted-risk-only disposition tables are valid when every row has a rationale. Do not pass the confidence gate with unresolved premortem blockers or with findings that did not mutate the plan or risk ledger.
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
index 108f361..0ab5588 100755
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
@@ -533,6 +538,44 @@ def validate_task_map(found: dict[str, str], tier: str, errors: list[str]) -> No
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
+    for term in ["overengineering", "code-bloat", "80/50"]:
+        if term not in section_lower:
+            errors.append(f"V0 plan premortem missing concept: {term}")
+    rows = table_meaningful_rows(section)
+    if not rows:
+        errors.append("V0 plan premortem needs at least one failure-disposition row")
+    disposition_cells = normalize(" ".join(row[1] for row in rows if len(row) > 1))
+    if rows and not any(term in disposition_cells for term in ["plan revision", "accepted risk", "accepted-risk"]):
+        errors.append("V0 plan premortem dispositions must be plan revision or accepted risk")
+
+
 
 DEAD_CODE_TOOL_TERMS = [
     "vulture",
@@ -1338,6 +1381,7 @@ def main() -> int:
 
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
index 047cc32..a89a15e 100644
--- a/uberplan/tests/test_validators.py
+++ b/uberplan/tests/test_validators.py
@@ -75,6 +75,49 @@ class PlanValidatorTests(unittest.TestCase):
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
+    def test_tier2_v0_plan_premortem_allows_accepted_risk_only_dispositions(self) -> None:
+        text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
+        text = text.replace("plan revision / accepted risk", "accepted risk")
+        text = text.replace("plan revision |", "accepted risk |")
+        text = text.replace("plan revision or accepted risk rows", "accepted risk rows")
+        with tempfile.TemporaryDirectory() as tmp:
+            plan = Path(tmp) / "accepted_risk_only_premortem.md"
+            plan.write_text(text)
+            self.assertPasses(str(PLAN), str(plan), "--tier", "2", "--agent-behavior")
+
     def test_tier2_requires_verifiable_subgoals(self) -> None:
         text = (FIX / "valid" / "tier2_agent_plan.md").read_text()
         start = text.index("## Verifiable subgoals and metrics")
@@ -167,6 +210,17 @@ class PlanValidatorTests(unittest.TestCase):
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
