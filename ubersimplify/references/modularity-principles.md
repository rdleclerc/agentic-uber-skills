# Modularity Principles

Simplicity is not just fewer lines. Good modularity reduces concepts and enforces invariants.

Prefer centralizing when:

- duplicated policy or source-of-truth exists
- the invariant is domain-critical
- failure should be loud and observable
- the dependency is narrow, named, tested, and owned
- callers become simpler and less error-prone

Avoid modularity theater:

- wrappers with no semantic value
- god modules or global mutable singletons
- vague `utils` dumping grounds
- abstraction before two real use cases
- splitting cohesive code only because files are long
- hidden runtime dependencies without contract tests
