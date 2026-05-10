# Dead-Code Audit

| ID | Location | Evidence unused | Commands/artifacts checked | Dynamic/external reference check | Risk | Action |
|---|---|---|---|---|---|---|
| D1 |  |  |  | imports/config/routes/prompts/tools/external consumers checked |  | defer until proof |

## Dynamic-reference checklist
- imports/reflection/importlib/registries/decorators:
- CLI entrypoints/package metadata/console scripts:
- framework routes/event handlers/background jobs:
- config files/feature flags/environment variables:
- migrations/data contracts/schemas:
- tests/fixtures/golden data:
- prompts/tools/skills/agent manifests:
- shell scripts/CI/cron/launchd/deployment manifests:
- docs/runbooks/external consumers/installed copies:
