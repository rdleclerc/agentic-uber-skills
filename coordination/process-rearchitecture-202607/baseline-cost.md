# Baseline cost — 4 representative pre-change tasks (captured 2026-07-03)

Read-only extraction from `coordination/` folders and git history in `/Users/rob/repos/agfunder-gaia`. Pre-change baseline for the process-rearchitecture campaign (Measurement spine, judgment #8); compare post-change runs against the same columns and honor the caveats.

| task | span (wall-clock) | review-rounds | rework-commits | artifacts | words | tokens | sessions/dispatches |
|---|---|---|---|---|---|---|---|
| 1. Model-week WS2-S2 orphan-edge reconciliation (`gaia-model-week-execution-2026-07-01`, `7fc28e6e`) | S2 slice ~16 min; whole 5-slice campaign ~2h | 1 slice review + shared campaign final acceptance | 0 | 11 s2-* files (folder 28) | s2 md 1,160 (folder md 7,445) | unknown | 1 Fable orchestrator; Codex per-slice dispatches (count unrecorded); dispatch-ops incidents logged |
| 2. Comms E1 gmail hook outcome contract (+ uberrca fix folder) | E1 core ~2h; fully-fixed ~16.7h incl. overnight | 2 E1 rounds + uberrca (2 adversarial rounds + acceptance) | 2 | ≈108 across 3 folders | E1 receipts 1,364; campaign folder 20,459 | **804,902** for the one Codex implementation session; all other lanes unknown | 1 Fable orchestrator; 2 Codex E1 rounds; 6 vehicle dispatches; fix = 1 Codex + 3 Claude reviews |
| 3. gbrain read-mirror comparison (2026-06-30) | 75 min work; merged 16:56 in mixed commit `f342456a` | 3 plan rounds + 2 impl reviews + 1 acceptance = 7 review dispatches | 0 recoverable (squashed) | 42 files | 88,343 total; **~74% of md = review-dispatch prompts** (~44.9K of 61K) | unknown | 1 implementer session + 7 Claude review dispatches |
| 4. Automated health-RCA run (gmail-hook-terminality, 06-28) | 7m45s | 0 | same alert: 4 consecutive daily runs, zero resolution (class fixed manually 07-02) | 12 files | 15,241 | unknown (3 MiniMax probes died ProviderAuthError; Codex repair died on usage limit) | 5 dispatches |

## Data-quality caveats

- mtimes measure last write, not work; in-file timestamps beat mtimes; orchestrator think-time invisible.
- Campaign folders are shared surfaces — per-slice cost separable only by filename prefix + commit boundaries.
- Word counts conflate prose with mechanical receipts (DB backups, one 131K-line Codex transcript); md-only is the better prose proxy, and gbrain's md is ~74% dispatch prompts (context re-priming cost, a target of this campaign).
- Tokens essentially unrecorded: ONE hard number across all four tasks (Codex terminal output). Post-change token comparison requires the per-dispatch usage receipt convention (R13c) first; until then only that lane is comparable.
- Review-round counts count artifacts, not effort (132-word reconciliation vs 11,964-word dispatch prompt both = 1 round).
- Rework detection is squash-blind and scope-ambiguous; counts here were commit-message-adjudicated by hand.
- Wall-clock spans include idle gaps; the automated RCA's 8-minute cheapness is a failure symptom (auth-dead probes, quota-dead repair), not efficiency.
- Session/dispatch counts are floors (double-launches/zombies left no artifacts). Post-change runs must log dispatch counts explicitly.
