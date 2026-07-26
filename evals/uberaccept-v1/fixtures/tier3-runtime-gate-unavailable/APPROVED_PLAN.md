# Approved plan

Tier 3. Accept the provider-route replacement only after an already-authorized
canary and authoritative runtime readback. The canary authorization is recorded
as `auth-77`. If the runtime gate itself is unavailable, fail closed and file
failure intake; do not reinterpret the missing result as rejection.
