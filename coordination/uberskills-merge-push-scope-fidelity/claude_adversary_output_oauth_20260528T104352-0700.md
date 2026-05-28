## Adversarial Review — `uberskills-merge-push-scope-fidelity`

---

### 0. Frame-independence check

**Invited role:** Adversarial structural reviewer confirming this patch implements the operator's scope-fidelity gate. I accept this role without modification — the prompt provides the original instruction verbatim as Section 1 and the actual diff as Section 2, which is exactly the required format.

**Role Codex is asking me to play:** Confirm a scope-fidelity implementation is complete. I accept, but I won't let the role collapse into ratification — I'm checking whether the implementation is actually complete, not just whether it looks like an implementation.

---

### 1. Original-vs-summary gap

Three things the operator instruction requires that this diff either omits or leaves structurally unverified:

**A. `scripts/check_scope_fidelity_artifacts.py` is absent from the diff.**
Git status shows `?? scripts/check_scope_fidelity_artifacts.py` and `?? tests/test_scope_fidelity_artifacts.py` as *untracked*. The diff does not include them. Untracked = not committed = not shipped. The operator explicitly required this script as the cross-cutting structural gate with four specific fail conditions. What's in the diff only adds section-presence checks to two *existing* validators; the new standalone validator that checks `scope.md` existence, SHIP ordering, and `Narrowing? yes` + empty approval citation is entirely absent from what can be reviewed.

**B. `ubergoal/templates/scope.md` is absent from the diff.**
Also shown as untracked. The operator required a scope artifact template. The diff references `coordination/<task-slug>/scope.md` in multiple places but provides no template for how agents generate that file. Without a template, the "durable artifact" the whole system anchors on has no canonical format.

**C. Narrowing regression tests are missing.**
The operator required two specific fixtures: (1) plan/acceptance narrows "codebase-wide OpenClaw audit" to Slack-only without approval → validator fails; (2) operator explicitly approves Slack narrowing → validator passes. Neither is in the diff. The tests that *are* present only check section presence, not narrowing semantics.

---

### 2. Reject conditions

1. **`check_scope_fidelity_artifacts.py` doesn't implement the four required fail conditions** (missing `scope.md`, missing verdict, SHIP before verdict, `Narrowing? yes` without approval citation). If the file doesn't exist or is incomplete, the primary structural gate is unshipped.

2. **SHIP-before-verdict ordering is not enforced by any validator in this diff.** `validate_acceptance_report.py` checks section *presence* via `REQUIRED_SECTIONS`, not order. An agent can write `SHIP IT` at line 3, add `## Scope fidelity verdict` at the bottom, and pass all checks. This is exactly the failure mode the operator described.

3. **`Narrowing? yes` without a non-empty approval citation is not caught by any validator in this diff.** The plan and acceptance validators only check that the `## Scope fidelity` / `## Scope fidelity verdict` headers exist. A plan that says `Narrowing? yes` and `Operator approved narrowing in: n/a` passes both validators today.

---

### 3. Challenges

**Challenge 1 — Missing cross-cutting validator (causal: absent artifact)**

*Claim:* The operator's primary structural gate — `scripts/check_scope_fidelity_artifacts.py` — is not in the diff.

*Why it matters:* The operator's stated root failure was that scope laundering happened at the junction between three skills. Intra-skill section-presence checks can't catch cross-artifact failures (e.g., scope.md missing, SHIP appearing before a verdict that exists). The new standalone script was the mechanism to catch exactly that.

*Falsifying evidence:* Show the file in the diff with the four required fail conditions implemented and tested.

*Satisfying evidence:* The script is committed with tests covering all four cases from the operator spec.

*Minimum impact threshold:* Without this, the gate against "scope.md missing" and "SHIP before verdict" ordering is entirely absent. Scope laundering at those two surfaces remains unblocked.

---

**Challenge 2 — SHIP ordering gap in existing validators (causal: structural incompleteness)**

*Claim:* `validate_acceptance_report.py` checks section presence but not order. A compliant-looking acceptance report can place SHIP before the verdict and pass.

*Why it matters:* The operator specifically named `SHIP appears before the scope-fidelity verdict` as a required fail condition. This is not a theoretical edge case — it's a common pattern when agents hedge: write the completion language, then add the required section below it.

*Falsifying evidence:* Show a test where a report with SHIP at line 1 and `## Scope fidelity verdict` at the end fails validation.

*Satisfying evidence:* The validator (either existing or new) checks that SHIP/completion language does not appear before the verdict section.

*Minimum impact threshold:* Without this, the "must appear before SHIP" language in the template is advisory, not enforced.

---

**Challenge 3 — Narrowing-specific regression tests missing (causal: incomplete test coverage)**

*Claim:* The operator required two specific regression fixtures for unapproved vs. approved narrowing. Neither exists in this diff.

*Why it matters:* The `Narrowing? yes` + empty citation check is the semantic core of scope-fidelity enforcement. Without tests that exercise it, neither Codex nor future maintainers know whether the validators actually catch it.

*Falsifying evidence:* Show a test where a report with `Narrowing? yes` and `Operator approved narrowing in: n/a` fails.

*Satisfying evidence:* Both fixtures (unapproved narrowing fails, approved narrowing passes) are present and green.

*Minimum impact threshold:* Without these, the "unapproved narrowing is a blocker" requirement is a textual assertion, not a verified behavior.

---

### 4. What's solid

- The SKILL.md changes in `ubergoal`, `uberplan`, and `uberaccept` are surgical. They add scope artifact gates without bloat.
- Renaming `## Scope Fidelity Ledger` → `## Scope fidelity` in the plan template is correct — it matches the case-insensitive checks in `validate_plan_contract.py`.
- Adding `"scope fidelity verdict"` to `REQUIRED_SECTIONS` in `validate_acceptance_report.py` is the right move; the section name is consistent with the template.
- `references/claude-adversary.md` is properly updated — Section 1 = scope.md, Section 2 = artifact, prompt saved to coordination folder.
- Fixture files for the existing valid-plan and valid-acceptance tests are correctly updated.
- Tests `test_acceptance_requires_scope_fidelity_verdict` and `test_tier2_requires_scope_fidelity` are well-formed regression guards for section presence.

---

### Final gate

**Ship: No.**

Three unshipped artifacts (the standalone scope validator, the scope template, and the narrowing regression tests) leave the operator's primary structural fail conditions — `scope.md` missing, SHIP before verdict, `Narrowing? yes` without approval — unenforced by any committed code in this diff.

---

## 🧠 What You Need to Know
- The diff implements the *text and template* layer of scope fidelity correctly, but three required artifacts from the operator spec are untracked on disk and absent from the diff: `scripts/check_scope_fidelity_artifacts.py`, `ubergoal/templates/scope.md`, and the narrowing regression test fixtures.
- SHIP-before-verdict ordering is not enforced by any committed validator — section presence is checked, but not order.
- `Narrowing? yes` without approval citation is not caught by any validator in this diff — it would pass all current checks.

## ✅ What I Need From You
1. **Three missing artifacts** — The standalone validator, scope template, and narrowing tests need to be either committed (if already on disk) or implemented. **Recommendation: stage and diff those untracked files first — if they implement the four required fail conditions correctly, a second review pass on just those files may be sufficient to ship.**

## 💡 My Recommendation
**Stage the three untracked files, run the full test suite, and send the new diff for a narrow second review before merging.**

---

— uberskills-merge-push, 8:28am Wednesday, May 28
