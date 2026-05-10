# Test Confidence

## Baseline confidence
strong | medium | weak | unknown

## Evidence
| Layer | Command/artifact | Result | Confidence | Gap |
|---|---|---|---|---|
| unit/regression |  |  |  |  |
| integration |  |  |  |  |
| UI/browser |  |  |  |  |
| evals/real data |  |  |  |  |
| static/dead-code |  |  |  |  |

## Allowed action
- strong: patch/delete allowed with acceptance
- medium: add characterization tests first; patch only after touched slice reaches strong-enough local confidence
- weak: audit/plan only; never delete/refactor production behavior on weak evidence
- unknown: no deletion; discover tests/references first
