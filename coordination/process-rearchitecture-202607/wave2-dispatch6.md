# Wave 2 — Dispatch 6: registry hardening + ubersimplify slim + review ride-alongs (pack)

You are Codex, implementer. Pack repo only; NO git commands. Context: all gaia-side Wave-2 unifications are landed and pushed (gaia main 5ae8cbd1); the E6 session's checkout has merged them.

## 1. Drift-module + registry hardening (scripts/lint_pack_contract.py + references/drift-fingerprints.toml)

a. **git_ref per-target support**: optional `git_ref = "main"` field per fingerprint entry; when set and the target path lies inside a git repo, read content via `git -C <repo> show <ref>:<relpath>` instead of the working tree (fall back to working tree with a printed note if git show fails). Set `git_ref = "main"` on ALL gaia-repo targets (doctrine truth = main, not whatever branch a session has checked out). Seeded test: fixture repo where working tree diverges from HEAD; assert git_ref mode reads the ref.
b. **Pattern-expansion decoupling (bug)**: `pattern_matches` expands `${VAR:-default}` in patterns using the live env, so overriding GAIA_ROOT changes the EXPECTED string and false-DIVERGEs (proven: canary-command ×3 false alarms when GAIA_ROOT pointed at a worktree). Fix: expand patterns with the DEFAULT value always; env overrides affect only target-path resolution. Regression test with env override set.
c. **guide-version-line entry**: the gaia copy is now a 14-line stub (no Version line) — retire this entry and replace with `stub-canonical-path`: literal fingerprint of the stub's canonical-path line (read gaia main:AGENTIC_ARCHITECTURE.md via your new git_ref mode) with targets = gaia AGENTIC_ARCHITECTURE.md; plus keep a `Version:` regex check on the canonical singlefile only (guide repo target), severity warn.
d. **Blocking flips** now that both homes exist and landed: test-channel-posture, canary-command, precedence-sentence, tier-ladder-table, lane-policy-spine → `adoption_state = "blocking"`, clear stale `pending` notes (remember: blocking only gates `--strict`, which runs at wave gates — default runs stay report-only).
e. **New fingerprint** `lane-policy-home`: the home-CLAUDE.md default-lane bullet (read ${HOME}/CLAUDE.md — fingerprint its "Default model lane (reversed 2026-06-30)" through "shadow until enforced" span as regex with .* joins), target ${HOME}/CLAUDE.md, report_only (home file, no VCS), severity warn.

## 2. ubersimplify keep-slimmed (per wave2-r8-retirement-evaluations.md's named cuts)

Move: Required-gates detailed bullets → `ubersimplify/references/gates.md`; Modularity-stance examples → `ubersimplify/references/modularity-principles.md`; Test-confidence table → `ubersimplify/references/test-confidence.md`; Parallel-simplification section → short pointer. Keep: Core rule, Modes (Audit default / Patch authorization boundary), Output contract, relationship/resources. Frontmatter/description unchanged. Deletion-receipt rows in a new `wave2-d6-deletion-receipt.md`. Update its word budget in SKILL_WORD_BUDGETS (new count +10%, round to 50). Run its tests/lint/quick_validate.

## 3. Review ride-alongs (wave-1 adversarial findings F10/F11)

a. Secret-scan pattern gaps: add `github_pat_`, base64url token class (JWT segments), `xoxc-/xoxs-/xapp-`, AWS-secret heuristic; exempt 40-hex when preceded by "commit"/inside backticks (prevents git-SHA false positives the current test would trip on). Extend the seeded fixture with one of each; keep report_only.
b. validate_failure_case robustness: nonexistent target → clean FAIL message (not a traceback); sanitization scan covers title/cost/body too (not just what_happened); add `none` to the placeholder set. Negative fixtures.

## 4. Verify + report

Full pack tests + lint; `--drift` (default) and `--drift --strict` WITH git_ref mode active — print both outputs (strict should now PASS against gaia main); per-skill checks for ubersimplify; validate_failure_case over cases + --index. Print word deltas + receipts inline. FLAG contradictions.
