# Dead-Code Safeguards

Dead-code detection is often wrong. Before deleting, check:

- dynamic imports/reflection/string-based dispatch
- CLI entrypoints and scripts
- framework routes/pages/serverless functions
- config references and environment-driven names
- migrations, data contracts, schemas, generated files
- tests/fixtures and snapshot expectations
- prompts, tools, skills, MCP/app registrations
- public API or external consumers
- docs/runbooks that operators still follow

Delete only when evidence is strong. If references are unknown, produce a candidate and proof plan, not a patch.
