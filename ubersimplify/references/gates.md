# Simplification Gates

Before deleting or refactoring, pass these gates:

- **Basic Spine First veto**: for product, rewrite, or agentic-system work, if the minimum user-visible product spine is failing or lacks a canonical proof check, veto new architecture, abstractions, agents, contracts, routers, monitors, and eval frameworks. The next patch may only fix or create the spine check, or explicitly stay a non-readiness spike.
- **Burden-of-proof gate**: name the cost this complexity imposes and the failure it prevents.
- **Chesterton gate**: explain why the code or process was probably added, and whether that reason is gone or handled elsewhere.
- **Modularity gate**: ask whether better boundaries, a single source of truth, or stronger contracts reduce conceptual complexity.
- **Fail-fast gate**: ask whether a shared dependency or contract should make violations loud instead of allowing silent drift.
- **Evidence gate**: tests, evals, static checks, or characterization prove behavior is preserved or intentionally changed.
- **Dead-code safeguard**: check dynamic imports, CLI entrypoints, framework routes, configs, migrations, prompts, tools, and external references before deletion.
- **Rollback gate**: keep the patch small, reversible, and backed by a clear backout plan.
- **Agent Advocate / human-counterfactual gate**: for agentic-system complexity, ask whether a capable human with the same goal, context, and tools would have made the error. If not, fix missing context, bad tool feedback, conflicting source authority, or weak affordances before adding or removing compensating complexity.
