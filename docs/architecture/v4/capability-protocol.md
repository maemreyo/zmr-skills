# Capability protocol

Capabilities receive one `zamery-capability.v1` invocation on stdin and return exactly one JSON result on stdout. Logs use stderr. The kernel recalculates hashes and validates output paths before commit.
