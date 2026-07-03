# Wave 1 — Dispatch 3 of 4: R16a pack side (failure-eval DB, validators, terminal mode, intake)

You are Codex, implementer for the process-rearchitecture campaign. Authority: `plan-v3.md` R16a + amendments A, C, D, G (partial), L; `failure-catalog.md` (21 cases). Work ONLY in this repo; NO git commands. Slices 1–2 landed (portability oracle, drift registry, install-sync). Keep SKILL.md prose additions MINIMAL (one-liners with pointers — Wave 2 owns text restructuring); record word deltas for any SKILL.md you touch.

## 1. Failure-eval DB (pack layer)

- `evals/failures/README.md`: schema v2 doc (fields from failure-catalog.md: id, date_observed, layer, canonical_layer, title, what_happened, failure_class, cost, gate_that_missed_it, eval_check, eval_type executable|fixture|checklist|live, plan_items, status seed|eval_built|enforced) + sanitization rules + the P4 completeness rule + intake field grammar (`failure_case_id: <id> | case_updated: <id> | not_applicable_with_reason: <text>`).
- Per-case files `evals/failures/cases/<id>.md` (YAML frontmatter + short body) for the 12 PROCESS-canonical cases: scope-laundering-20260528, evaluator-saturation, claw1-path-rot, install-drift-uberarchitect, doctrine-drift-trio, sandbox-fake-row-shape, dispatch-double-launch, credential-exposure-by-agent, pinned-external-identifier-rot, dispatch-preflight-writeability, unverified-baseline-claims, subprocess-dies-without-terminal-state. Populate from failure-catalog.md rows (sanitized; dates: cases 1-14 observed 2026-06-18..07-02 per catalog, 15-19 date_observed 2026-07-03, 20-21 2026-07-03). status: cases 7/8/9 = eval_built (their evals landed slices 1-2 — name the aggregator module in eval_check); others seed. plan_items from the catalog's last column.
- `evals/failures/INDEX.md`: ALL 21 cases, one line each: id · layer(canonical) · status · where canonical lives (process cases here; runtime-canonical cases marked "canonical: agfunder-gaia/evals/failures/ (pending dispatch 4)").
- `scripts/validate_failure_case.py` — NEW standalone CLI (justified: invoked cross-repo by the gaia suite via `${UBER_SKILLS_ROOT:-~/repos/agentic-uber-skills}/scripts/validate_failure_case.py`; note this justification in the module docstring per amendment J). Validates one case file or a cases/ dir: required fields, enum values, canonical_layer consistency (layer=both requires canonical_layer; pointer files must name the canonical repo), sanitization heuristics (no /Users/<name> paths in what_happened except parameterized, defer secrets to the secret-scan module). Invalid fixtures + tests wired into tests/test_pack_contract.py or a new tests/test_failure_cases.py.

## 2. Amendment A — terminal-status mode for acceptance

`uberaccept/scripts/validate_acceptance_report.py`: add `acceptance_status: accepted | rejected | blocked_with_failure_intake`. `accepted` keeps current strict checks. `rejected`/`blocked_with_failure_intake` must VALIDATE (that is the point) with: the status line, a truthful blocker/finding section, and the intake field present. Keep backward compat: reports without the field are treated as `accepted` (legacy) — but the template gains the field. Fixtures: accepted-passes, rejected-with-intake-passes, rejected-without-intake-fails, accepted-with-unresolved-blockers-fails.

## 3. P4 intake enforcement (amendments C/D/G-partial)

- `ubergoal/scripts/validate_uber_run_receipt.py` + `ubergoal/templates/uber-run-receipt.md`: require ONE of `failure_case_id | case_updated | not_applicable_with_reason` (non-empty). Also add cost fields to the template: `tokens`, `minutes`, `source` (self_reported|measured|unknown) next to the existing `lane_used`; validator requires presence, `unknown` allowed.
- `uberaccept` template + validator: same intake requirement (any surprise row or rejected status must carry it; simplest enforceable rule: the field is always required, `not_applicable_with_reason: no failure observed` is the happy path).
- NEW `uberrca/scripts/validate_rca_artifact.py` + a minimal `uberrca/templates/rca-artifact.md`: requires `class_invariant` (one sentence), `surface_enumeration` (list), and the intake field. Wire into uberrca/tests. Add ONE line to uberrca/SKILL.md output-shape section pointing at the template/validator.
- Add ONE line each to ubergoal + uberaccept SKILL.md where receipts/acceptance are described: intake field is mandatory; grammar in evals/failures/README.md.

## 4. Secret-scan module (case 15)

Aggregator module `--secret-scan` in scripts/lint_pack_contract.py: scan doctrine text + coordination/ + evals/ for likely credential literals (prefixes: sk-, xoxb-, xoxp-, ghp_, gho_, AKIA, AIza, Bearer <40+ chars>, PEM headers, high-entropy 32+ char base64/hex tokens). `op://` references are SAFE (they are the approved form). Report-only default, `--strict` flag, blocking_wave=2; seeded fixture with a fake key must be detected; ensure the fake key lives ONLY under tests/fixtures (marker-exempt it from its own detection via path, not content).

## 5. Wrap-up

Run: full pack tests + lint (all modules) + every touched skill's tests + `validate_failure_case.py` over evals/failures/cases/. Print: files changed, SKILL.md word deltas, test counts, and the case INDEX summary. FLAG contradictions prominently; do not resolve silently.
