Implemented R3/R4 inside this repo only. No git commands were run, and no files outside this checkout were edited.

**Files Changed**
- [scripts/lint_pack_contract.py](/Users/rob/repos/agentic-uber-skills/scripts/lint_pack_contract.py): added `check_doctrine_drift`, `check_skill_install_sync`, `--drift`, `--install-sync`, `--strict`, registry schema validation, and report-only default wiring.
- [references/drift-fingerprints.toml](/Users/rob/repos/agentic-uber-skills/references/drift-fingerprints.toml): added initial Wave 1 registry.
- [tests/test_pack_contract.py](/Users/rob/repos/agentic-uber-skills/tests/test_pack_contract.py): added drift, schema, install desync, and real install-sync tests.
- `tests/fixtures/drift/*`: added seeded drift and invalid-registry fixtures.

**Registry States**
- `report_only`: `test-channel-posture`, `canary-command`, `post-upgrade-canary-mandate`, `guide-version-line`
- `blocking`: `lane-policy-portable`
- `planned`: `precedence-sentence`, `tier-ladder-table`

**Flag**
Spec contradiction: `lane-policy-portable` asks for the exact full `AGENTS.md` sentence while also targeting README’s shorter first-sentence form. A single literal cannot satisfy both, so I encoded that entry as a regex matching both intended forms.

**Verification**
- `python3 scripts/lint_pack_contract.py`: PASS
- `python3 -m pytest tests/ -q`: 32 passed
- `python3 -m unittest discover -s tests -v`: 32 tests OK
- `python3 scripts/lint_pack_contract.py --install-sync --strict`: PASS
- `python3 scripts/lint_pack_contract.py --drift --strict`: PASS

**Current Drift Report**
```text
DOCTRINE DRIFT REPORT registry=/Users/rob/repos/agentic-uber-skills/references/drift-fingerprints.toml
DIVERGED id=test-channel-posture target=${GAIA_ROOT:-~/repos/agfunder-gaia}/GAIA_TESTING.md adoption_state=report_only severity=warn blocking_wave=2 detail=literal not found
MATCH id=test-channel-posture target=${GAIA_ROOT:-~/repos/agfunder-gaia}/CLAUDE.md adoption_state=report_only severity=warn blocking_wave=2
DIVERGED id=test-channel-posture target=${GAIA_ROOT:-~/repos/agfunder-gaia}/AGENTS.md adoption_state=report_only severity=warn blocking_wave=2 detail=literal not found
DIVERGED id=test-channel-posture target=${GAIA_ROOT:-~/repos/agfunder-gaia}/skills/gaia-testing/SKILL.md adoption_state=report_only severity=warn blocking_wave=2 detail=literal not found
DIVERGED id=canary-command target=${GAIA_ROOT:-~/repos/agfunder-gaia}/GAIA_TESTING.md adoption_state=report_only severity=warn blocking_wave=2 detail=literal not found
DIVERGED id=canary-command target=${GAIA_ROOT:-~/repos/agfunder-gaia}/CLAUDE.md adoption_state=report_only severity=warn blocking_wave=2 detail=literal not found
MATCH id=canary-command target=${HOME}/CLAUDE.md adoption_state=report_only severity=warn blocking_wave=2
MATCH id=lane-policy-portable target=AGENTS.md adoption_state=blocking severity=error blocking_wave=1
MATCH id=lane-policy-portable target=README.md adoption_state=blocking severity=error blocking_wave=1
MATCH id=post-upgrade-canary-mandate target=${GAIA_ROOT:-~/repos/agfunder-gaia}/GAIA_TESTING.md adoption_state=report_only severity=warn blocking_wave=2
MATCH id=guide-version-line target=${GAIA_ROOT:-~/repos/agfunder-gaia}/AGENTIC_ARCHITECTURE.md adoption_state=report_only severity=warn blocking_wave=2
MATCH id=guide-version-line target=${UBER_GUIDE_ROOT:-~/repos/agentic-architecture-guide}/agentic_architecture_singlefile.md adoption_state=report_only severity=warn blocking_wave=2
ABSENT(allowed) id=precedence-sentence target=${GAIA_ROOT:-~/repos/agfunder-gaia}/AGENTS.md adoption_state=planned severity=warn blocking_wave=2 detail=empty pattern pending=Wave 2 R7/R6
ABSENT(allowed) id=precedence-sentence target=AGENTS.md adoption_state=planned severity=warn blocking_wave=2 detail=empty pattern pending=Wave 2 R7/R6
ABSENT(allowed) id=tier-ladder-table target=${GAIA_ROOT:-~/repos/agfunder-gaia}/knowledge/coding-agent-operating-spine.md adoption_state=planned severity=warn blocking_wave=2 detail=empty pattern pending=Wave 2 R7/R6
ABSENT(allowed) id=tier-ladder-table target=ubergoal/SKILL.md adoption_state=planned severity=warn blocking_wave=2 detail=empty pattern pending=Wave 2 R7/R6
```

