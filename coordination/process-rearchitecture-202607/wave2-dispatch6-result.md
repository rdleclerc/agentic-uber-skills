Implemented in the pack repo only.

Changed:
- Added drift `git_ref` support with fallback notes and `source=git_ref(main)` reporting in [scripts/lint_pack_contract.py](/Users/rob/repos/agentic-uber-skills/scripts/lint_pack_contract.py:471).
- Decoupled pattern expansion from env overrides: target paths use env, fingerprint patterns use defaults in [scripts/lint_pack_contract.py](/Users/rob/repos/agentic-uber-skills/scripts/lint_pack_contract.py:372).
- Hardened registry entries, flipped requested fingerprints to blocking, added `lane-policy-home`, replaced `guide-version-line` with `stub-canonical-path` plus guide singlefile version check in [references/drift-fingerprints.toml](/Users/rob/repos/agentic-uber-skills/references/drift-fingerprints.toml:4).
- Slimmed `ubersimplify/SKILL.md` from 896 to 610 words, budget set to 700, with moved detail in `references/gates.md`, `modularity-principles.md`, and `test-confidence.md`.
- Added deletion receipt: [wave2-d6-deletion-receipt.md](/Users/rob/repos/agentic-uber-skills/coordination/process-rearchitecture-202607/wave2-d6-deletion-receipt.md:1).
- Expanded secret scan patterns and 40-hex exemptions in [scripts/lint_pack_contract.py](/Users/rob/repos/agentic-uber-skills/scripts/lint_pack_contract.py:124).
- Hardened `validate_failure_case.py` for nonexistent targets and title/cost/body sanitization in [scripts/validate_failure_case.py](/Users/rob/repos/agentic-uber-skills/scripts/validate_failure_case.py:129).

Verification:
- `python3 scripts/lint_pack_contract.py` PASS
- `python3 -m unittest discover -s tests -v` PASS, 54 tests, 1 expected skip for non-writable local `.git`
- `python3 ubersimplify/scripts/lint_skill_package.py /Users/rob/repos/agentic-uber-skills/ubersimplify` PASS
- `python3 -B -m unittest discover -s ubersimplify/tests -v` PASS, 12 tests
- `python3 uber-skill-creator/scripts/quick_validate.py ubersimplify` PASS
- `python3 scripts/validate_failure_case.py evals/failures/cases` PASS, 14 files
- `python3 scripts/validate_failure_case.py --index evals/failures/INDEX.md --cases evals/failures/cases` PASS

`uv run --with pyyaml ...` could not complete: default cache was unwritable, then writable-cache retry hit restricted network/DNS for PyPI. The same validator passed with installed Python.

`--drift` output:
```text
DOCTRINE DRIFT REPORT registry=/Users/rob/repos/agentic-uber-skills/references/drift-fingerprints.toml
MATCH id=test-channel-posture target=${GAIA_ROOT:-~/repos/agfunder-gaia}/GAIA_TESTING.md adoption_state=blocking severity=warn blocking_wave=2 source=git_ref(main)
MATCH id=test-channel-posture target=${GAIA_ROOT:-~/repos/agfunder-gaia}/CLAUDE.md adoption_state=blocking severity=warn blocking_wave=2 source=git_ref(main)
MATCH id=test-channel-posture target=${GAIA_ROOT:-~/repos/agfunder-gaia}/AGENTS.md adoption_state=blocking severity=warn blocking_wave=2 source=git_ref(main)
MATCH id=test-channel-posture target=${GAIA_ROOT:-~/repos/agfunder-gaia}/skills/gaia-testing/SKILL.md adoption_state=blocking severity=warn blocking_wave=2 source=git_ref(main)
MATCH id=canary-command target=${GAIA_ROOT:-~/repos/agfunder-gaia}/GAIA_TESTING.md adoption_state=blocking severity=warn blocking_wave=2 source=git_ref(main)
MATCH id=canary-command target=${GAIA_ROOT:-~/repos/agfunder-gaia}/CLAUDE.md adoption_state=blocking severity=warn blocking_wave=2 source=git_ref(main)
MATCH id=canary-command target=${HOME}/CLAUDE.md adoption_state=blocking severity=warn blocking_wave=2 source=working_tree
MATCH id=lane-policy-portable target=AGENTS.md adoption_state=blocking severity=error blocking_wave=1 source=working_tree
MATCH id=lane-policy-portable target=README.md adoption_state=blocking severity=error blocking_wave=1 source=working_tree
MATCH id=lane-policy-spine target=${GAIA_ROOT:-~/repos/agfunder-gaia}/knowledge/coding-agent-operating-spine.md adoption_state=blocking severity=warn blocking_wave=2 source=git_ref(main)
MATCH id=lane-policy-home target=${HOME}/CLAUDE.md adoption_state=report_only severity=warn blocking_wave=2 source=working_tree
MATCH id=stub-canonical-path target=${GAIA_ROOT:-~/repos/agfunder-gaia}/AGENTIC_ARCHITECTURE.md adoption_state=report_only severity=warn blocking_wave=2 source=git_ref(main)
MATCH id=tier-ladder-table-pack target=ubergoal/SKILL.md adoption_state=blocking severity=warn blocking_wave=2 source=working_tree
```

`--drift --strict` output was the same MATCH set and exited 0.

Contradiction flagged: my first Gaia `AGENTIC_ARCHITECTURE.md` read briefly showed the old full file, but the current working tree and `git_ref(main)` read both show the stub. The final registry validates against `git_ref(main)`, which is the requested doctrine source. No direct shell `git` commands were run; the linter/tests exercised `git show` internally for the new feature.

