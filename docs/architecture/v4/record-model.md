# Record model

All canonical records are immutable Pydantic models with forbidden unknown fields. `calculated_hash` is SHA-256 of normalized canonical JSON. Mutable trust booleans are prohibited.
