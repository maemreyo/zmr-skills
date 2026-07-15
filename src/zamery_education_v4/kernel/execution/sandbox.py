from __future__ import annotations

import os
from pathlib import Path

from pydantic import BaseModel, ConfigDict

from .errors import SandboxViolation


class SandboxPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)
    isolation_level: str = "development_unisolated"
    allow_environment: tuple[str, ...] = ("PATH", "LANG", "LC_ALL", "SYSTEMROOT", "WINDIR")
    max_stdout_bytes: int = 2_000_000
    max_stderr_bytes: int = 2_000_000
    max_output_files: int = 500
    max_output_bytes: int = 100_000_000

    def environment(self) -> dict[str, str]:
        return {name: os.environ[name] for name in self.allow_environment if name in os.environ}


def validate_output_tree(output_root: Path, policy: SandboxPolicy) -> tuple[Path, ...]:
    root = output_root.resolve()
    files: list[Path] = []
    total = 0
    for path in output_root.rglob("*"):
        if path.is_symlink():
            raise SandboxViolation(f"symlink output forbidden: {path}")
        resolved = path.resolve()
        if root not in resolved.parents and resolved != root:
            raise SandboxViolation(f"output escapes output mount: {path}")
        if path.is_file():
            files.append(path)
            total += path.stat().st_size
    if len(files) > policy.max_output_files:
        raise SandboxViolation("excessive output file count")
    if total > policy.max_output_bytes:
        raise SandboxViolation("excessive output bytes")
    return tuple(sorted(files))
