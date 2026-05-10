# Test Confidence

Classify proof before deleting or simplifying.

- **Strong**: focused tests cover behavior; integration/eval/static checks cover important flows; failure would be visible.
- **Medium**: tests cover main behavior but edge cases/history are uncertain; add characterization tests before patching.
- **Weak**: tests are sparse, generic, or unrelated; audit/plan only.
- **Unknown**: no reliable understanding of test surface; discover tests and references first.

When tests are weak, passing them is not proof. Use candidates, characterization tests, and small reversible patches.
