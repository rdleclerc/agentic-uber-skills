# Nightly reconciliation loop

Run the existing reconciliation calculation every night without an operator
starting it manually. The loop must resume safely after interruption and must
not run forever on records that cannot be reconciled.
