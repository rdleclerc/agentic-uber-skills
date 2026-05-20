# Agentic Uber Skills Roadmap

This roadmap keeps the skill pack evolving without turning it into bureaucracy. The rule is always: add durable machinery only when benefit is **clearly much greater than** total downstream cost.

## Current architecture

- `ubergoal` — goal-owning lifecycle wrapper: create/bind the platform goal, classify, run Tier 2+ specialist review boards, route, ledger, final policy-adherence acceptance, tradeoff/surprise reporting, learning.
- `uberplan` — rigorous planning: plan contract, review lanes, verifiable subgoals, Mermaid task graphs, target file trees, parallelization maps, code-health/dead-code plans, Agent Advocate RCA, first-principles simplifier, confidence gate.
- `uberaccept` — adversarial final proof: evidence audit, architecture drift, Agent Advocate final check, completion recommendation.
- `uberskillevolver` — post-run learning loop: learning records, lesson candidates, promotion batches, anti-bloat gate.
- `deep-rca` — class-level root cause analysis before patches.
- `ubersimplify` — opt-in complexity/modularity/dead-code simplification with timestamped trails and proof gates; Audit/Plan are current default, Patch mode remains conservative/experimental until dogfooded on real codebases.
- `uberassess` = source-to-recommendation due diligence — explicit assessment for X/GitHub/arXiv/articles/videos/Hermes signals before adoption; produces packets, not implementation.
- `ubershow` — browser-first visual communication utility for decision boards, implementation plans, maps, timelines, questionnaires, and visual briefs; produces generated HTML views with copyable decision receipts, not source-of-truth records.
- `uber-skill-creator` — portable Uber skill authoring and migration utility for Codex, Claude, and SKILL.md-compatible agents; keeps general skill-authoring guidance under version control and adds legacy alias deprecation support, read-only quality reports, eval-driven iteration, HTML review reports, and trigger-description tuning without runtime-specific commands.

## Routing and source-authority policy

- `ubergoal` is the only implicit/default Uber lifecycle router.
- Phase skills are explicit or wrapper-invoked to prevent ceremony creep; descriptions/prompts say not to auto-trigger from task similarity, while Codex adapter metadata still exposes every skill in the pack.
- `skill-creator` and `skill-creator-pro` are legacy local alias names, not parallel canonical creator skills. Redirect them to `uber-skill-creator` for portable SKILL.md work, or `openclaw-agentic-skill-creator` for OpenClaw/Gaia/Type0/Soho-specific skills.
- `uberassess` is explicit or routed by `ubergoal` for source/artifact assessment only. Its portable validator requires completed project rows but does not hardcode Rob-local project names; local adapter references may provide Type0/Gaia/Soho/Hermes defaults.
- `deep-rca` is the general incident RCA utility. Agent Advocate is the agent-behavior RCA lens inside planning/acceptance/simplification. If both apply, use the `deep-rca` ladder plus Agent Advocate human-counterfactual evidence.
- `ubershow` is a utility skill, not a lifecycle phase. It may be used when the user needs visual compression; source authority stays in Markdown/session logs/ADRs and decisions register via pasted receipts.
- Pack-level drift tests should enforce routing metadata, root agent contracts, install consistency, and RCA authority wording.

## Near-term priorities

1. **Fresh-agent behavioral evals**
   - Build a small pack-level harness before creating a standalone `ubereval` skill.
   - Verify a fresh agent routes `ubergoal → uberplan → uberaccept → uberskillevolver` correctly.
   - Turn golden eval seeds into an executable or semi-automated harness.
   - Test de-escalation: tiny tasks should not trigger the full machine.

2. **Cross-machine learning loop**
   - Keep raw learning records local/private by default.
   - Share only sanitized learning packets through Git.
   - Periodically review shared packets and promote repeated/high-severity lessons into evals, validators, templates, or deletions.

3. **Real-project dogfooding**
   - Use the pack on several non-trivial coding/agentic-system tasks.
   - Record where it made work faster, where it slowed work down, and where it prevented tech debt.
   - Prefer removing or simplifying instructions that do not pay for themselves.

4. **Second-pass architecture review**
   - Re-review boundaries between `ubergoal`, `uberplan`, `uberaccept`, and `uberskillevolver`.
   - Check whether any duplicated wording should move to a shared reference or be deleted.
   - Keep Work Contract and Uberplan precedence clear: Tier 1 should usually use the work contract as the plan artifact; Tier 2/3 can extend it.
   - Confirm that the Agent Advocate and First-Principles Simplifier lanes are strong enough without becoming ceremony.

5. **Uberassess dogfooding**
   - Use `uberassess` on real X bookmarks, GitHub repos, arXiv papers, articles, and Hermes findings.
   - Promote only repeated, evidence-backed assessment lessons into validators/evals/templates.
   - Retirement trigger: if three real assessment batches show it adds ceremony without preventing shallow-source, over-adoption, or approval-boundary failures, fold the useful checklist back into `ubergoal`/`uberplan` and remove the standalone skill.

6. **Ubershow dogfooding**
   - Use `ubershow` only when it materially increases decision speed or comprehension.
   - Keep artifacts static and self-contained; do not add a callback server or component library until repeated receipt-copy friction proves the need.
   - Track whether visual artifacts reduce user back-and-forth or hide missing evidence. If they become decorative ceremony, fold the useful templates back into prose examples and retire the standalone skill.

7. **Ubersimplify dogfooding**
   - Run `ubersimplify` Audit mode on real codebases before trusting Patch mode.
   - Promote only simplification patterns that survive tests/evals and rollback review.
   - Watch for undersimplification (reports only, no code removal) and oversimplification (deleting hidden invariants).
   - Keep explicit benefit/retirement trigger: if `ubersimplify` adds ceremony without producing safe net-deletion/refactor wins across real projects, demote Patch mode or merge the audit checklist back into `uberaccept`/`uberplan`.

## Deferred modules

Do not build these until real usage proves benefit >> cost:

- `ubercode` — execution-wave orchestration.
- `ubergit` / `ubership` — commit, PR, release, and GitHub-management workflows.
- `ubereval` — dedicated eval design/execution workflow.
- `uberui` — UI/browser verification workflow, distinct from `ubershow` visual communication artifacts.
- standalone specialist skills for Codebase Scout, Architecture Steward, Agent Advocate, Loophole Hunter, Quality/Eval Strategist.

Default: keep specialist roles as lanes/templates inside `uberplan` and `uberaccept` until repeated use proves a standalone skill would reduce context/cost or prevent failures.

## Promotion criteria for new subskills

A deferred module may become a skill only when at least one is true:

- The same lane is used repeatedly across real projects and consumes enough context to justify extraction.
- A failure recurs because the lane was too hidden or too weak inside an existing skill.
- A deterministic script/validator/eval harness needs its own focused package.
- Splitting it makes the common path smaller and faster, not just more organized.

Every new subskill needs:

- a named failure class it prevents
- benefit >> cost argument
- example invocation/eval seed
- package lint/test coverage
- clear relationship to `ubergoal`
- deletion/retirement trigger

## Cross-machine learning policy

Use Git to combine learnings, but do not commit raw traces by default.

- Raw records: local/private, e.g. `~/.agentic-uber-learnings/<machine-id>/...`.
- Shared packets: sanitized, small, safe-to-commit Markdown under `learning/inbox/<machine-id>/...`.
- Promotion: periodic human-reviewed batches move repeated/high-value lessons into skill diffs, evals, validators, templates, or deletions.
- Archive: after promotion/rejection, move packets to `learning/processed/` or leave them referenced by the promotion batch.

No silent self-modification: shared learnings are evidence, not authority.
