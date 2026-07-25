# Settlement ownership authority

Provider settlement ownership varies by deployment and is bound in
`generated/provider-settlement-binding.json`. That generated file is the sole
authority when adapters, ledgers, and handlers overlap. Do not infer ownership
from fallback order or call frequency.

If the binding is absent, obtain the read-only generated file from the target
deployment or ask the operator for an authoritative binding before planning
implementation.
