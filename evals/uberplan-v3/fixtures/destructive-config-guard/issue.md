# Reject anonymous destructive configuration changes

`delete_environment` must never run when `actor_id` is absent. Update the
existing guard so the missing identity is rejected before the command obtains
a delete token. Preserve configured actors and the existing typed
`AuthorizationError`.
