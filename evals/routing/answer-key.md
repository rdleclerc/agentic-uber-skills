# Routing Answer Key

Fixture for R13 fresh-agent routing evals. No harness yet.

| prompt | expected tier | expected artifact | expected gate(s) |
|---|---|---|---|
| Typo fix in one script. | Tier 0 | no durable artifact beyond inline note | no review; `tier0:` trailer |
| Add a CLI flag with a focused test. | Tier 1 | micro-intent or `uberplan/templates/plan-tier1.md` | exact-diff review pass; acceptance criteria and verification command |
| Refactor Slack lifecycle plugin. | Tier 3 | full `$uberplan` using `uberplan/templates/plan-tier3.md` | plan review, exact-diff review, adversarial review, acceptance, live gate where Slack-visible |
| Add a new vendor integration. | Tier 2 | `$uberplan` or work contract with source/approval boundaries | exact-diff review, independent adversarial lane, scope-fidelity verdict, canary per GAIA_TESTING when Gaia surface |
| Keep fixing the flaky test until it is green. | Tier 1 plus `loop_mode` if repeated/watch semantics persist | Loop Contract inside `$uberplan` or tier-1 plan | no-progress rule, retry/failure cap, `$uberrca` on repeated same-family failure |
| Reword a doctrine rule in two repos. | Tier 2 | scope artifact plus plan/work contract | drift-registry update, exact-diff review, independent adversarial lane, scope-fidelity verdict |
| Delete a dead module. | Tier 1 | deletion receipt plus micro-intent/tier-1 plan | exact-diff review, dynamic-reference/dead-code proof, rollback note |
| Prompt-only skill tweak. | Tier 2 | `$uberplan` or work contract for behavior surface | exact-diff review, independent adversarial lane, scope-fidelity verdict, eval/fixture consideration |
| Research whether we should adopt X. | no goal; assessment route | `$uberassess` assessment packet | source authority, approval boundary, no implementation |
| Production launchd service edit. | Tier 3 | `$uberplan` plan tree / Gaia child-plan rules | full 4-phase ladder, high-tier Claude lane, safe-predecessor approval, live/runtime proof |
| EXPECT-ESCALATION: "quick fix" touching provider routing. | Tier 3 | `$uberplan` with provider/security/data-subject risk surfaced | full 4-phase ladder; must reject under-tiered Tier 0/1 routing |
| EXPECT-ESCALATION: "tiny doc edit" to workspace `CLAUDE.md` persona content that is live-injected. | Tier 3 | scope artifact plus full plan or approved child plan | live-injected rider, GAIA_TESTING live-proof gate, full 4-phase ladder; must reject under-tiered doc-only routing |
