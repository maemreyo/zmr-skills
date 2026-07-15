from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ResourceLimits:
    timeout_seconds: int
    max_stdout_bytes: int = 2_000_000
    max_stderr_bytes: int = 2_000_000
    max_output_files: int = 500
    max_output_bytes: int = 100_000_000
