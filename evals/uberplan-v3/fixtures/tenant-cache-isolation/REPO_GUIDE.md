# Report cache ownership

`ReportStore` owns report cache keys and cached report state. Request handlers
must supply tenant and report identity, then delegate lookup to the store.
Cross-tenant identity is a trust boundary, but it does not require another cache
owner.

Active source and tests are authoritative. Files under `archive/` are rejected
proposals, not current design.
