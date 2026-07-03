# Test Confidence

Classify proof before deleting or simplifying.

| Confidence | Allowed action |
|---|---|
| strong | patch/delete allowed with acceptance |
| medium | add characterization tests first, then patch only after the touched slice reaches strong-enough local confidence |
| weak | audit/plan only; never delete/refactor production behavior on weak evidence |
| unknown | no deletion; discover tests/references first |

- **Strong**: focused tests cover behavior; integration/eval/static checks cover important flows; failure would be visible.
- **Medium**: tests cover main behavior but edge cases/history are uncertain; add characterization tests before patching.
- **Weak**: tests are sparse, generic, or unrelated; audit/plan only.
- **Unknown**: no reliable understanding of test surface; discover tests and references first.

When tests are weak, passing them is not proof. Use candidates, characterization tests, and small reversible patches.
