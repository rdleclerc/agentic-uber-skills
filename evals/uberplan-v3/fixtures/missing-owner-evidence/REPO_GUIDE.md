# Ownership authority

Export terminal-state ownership is generated from the deployment registry at
`generated/owner-map.json`. That file is the authority when handler, adapter,
and ledger call paths overlap. Do not infer ownership from filenames or call
frequency. If the generated registry is unavailable, obtain it from the target
deployment or ask the operator for the authoritative owner before planning an
implementation.
