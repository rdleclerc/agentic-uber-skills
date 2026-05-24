# Tier 3 Expensive-Proof Plan Tree Template

Use this template when a Tier 3 plan will run an agentic/runtime/production-replacement proof, burn-in, soak, canary expansion, or other high-cost proof where a shallow plan can burn hours.

This is a **pre-launch contract**, not final acceptance. It is intentionally general: do not hardcode OpenClaw/Type0 unless they are the current target system.

## Scope trigger

- Expensive-proof class: agentic runtime / production replacement / long-run E2E / soak / canary expansion / final proof / other:
- Why Tier 3:
- Estimated burn cost if wrong:
- Target-system proof required:
- Flat-plan exception? no/yes, with user approval path:

## Risk/failure-class inventory

Name concrete failure classes before launch. Use prior incidents, canaries, evals, logs, and architecture seams.

| ID | Failure class | Prior evidence / why plausible | Preflight or child plan that covers it | Stop signal |
|---|---|---|---|---|
| F1 |  |  |  |  |
| F2 |  |  |  |  |
| F3 |  |  |  |  |

## Observability / telemetry preflight

- Receipts/traces/logs/metrics available before burn-in:
- How to inspect phase status while run is active:
- Failure summary artifact path:
- Replay/debug artifact path:
- Preflight command(s) and expected result:
- Missing observability that blocks launch:

## Phase-boundary / contract-fuzz preflight

For each high-risk model/tool/phase boundary, prove malformed, truncated, missing, timeout, stale, and wrong-shape outputs become typed outcomes or repairable failures before the expensive run.

| Boundary | Shape/authority contract | Fuzz/negative case | Expected typed outcome / repair path | Evidence |
|---|---|---|---|---|
| B1 |  |  |  |  |
| B2 |  |  |  |  |
| B3 |  |  |  |  |

## Burn-in proof plan

- Burn-in/canary/soak size:
- Why this is small enough to fail cheaply:
- Pass threshold:
- Stop threshold:
- Evidence produced:
- What a burn-in pass does and does not authorize:

## Final-proof separation

- Final proof launch criteria after burn-in:
- What must be revalidated immediately before final proof:
- How final proof differs from burn-in:
- Evidence that burn-in artifacts are not being reused as final proof:
- Final proof stop/replan threshold:

## Stop/replan rules

- Stop immediately if:
- Stop before or at N same-family failures:
- Stop if a new un-inventoried failure class appears:
- Required RCA artifact:
- Required child plan / subplan before relaunch:
- Parent status-ledger update rule:
- Relaunch allowed only after:

## Child-plan/status-ledger structure

Use child files whenever there is more than one operational outcome, phase family, or expensive proof gate.

| Child ID | Child plan file | Owns failure classes / phase | Terminal states allowed | Evidence receipt |
|---|---|---|---|---|
| C1 | plans/<goal>/children/C1-observability-preflight.md | observability/telemetry | operational / blocked / re_scoped_with_approval | receipts/C1.md |
| C2 | plans/<goal>/children/C2-contract-fuzz-preflight.md | phase-boundary/contract fuzz | operational / blocked / re_scoped_with_approval | receipts/C2.md |
| C3 | plans/<goal>/children/C3-burn-in.md | burn-in/canary | operational / blocked / re_scoped_with_approval | receipts/C3.md |
| C4 | plans/<goal>/children/C4-final-proof.md | final proof | operational / blocked / re_scoped_with_approval | receipts/C4.md |

## Flat-plan exception record

Only fill if the agent/user explicitly accepts a flat plan despite the expensive-proof trigger.

- Flat-plan exception? yes/no:
- Approval evidence:
- Validator-bypass reason:
- Why benefit >> cost despite bypass:
- Added monitoring/stop rule that compensates:

## Ready-to-launch checklist

- [ ] Risk/failure-class inventory has at least three concrete failure classes.
- [ ] Observability/telemetry preflight has passed or named exact blocker.
- [ ] Phase-boundary/contract-fuzz preflight has passed or named exact blocker.
- [ ] Burn-in and final proof are separate gates.
- [ ] Stop/replan rules are written before launch.
- [ ] Child-plan/status-ledger structure exists, or flat-plan exception has approval and bypass reason.
- [ ] Acceptance rubric names Tier 3 expensive-proof preflight and burn-in vs final-proof evidence.
