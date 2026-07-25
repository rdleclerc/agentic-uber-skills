# Cross-tenant report leak

Tenant `orchard` requested report `weekly-7` and received the cached report
generated for tenant `harbor`. The current proposal is to add a separate cache
service with a centralized key registry and migrate report reads to it.
