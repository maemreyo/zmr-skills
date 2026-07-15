from __future__ import annotations

import asyncio
import os
import shutil
import signal
import tempfile
from dataclasses import dataclass
from pathlib import Path

from ...protocol.codec import encode_message
from ...protocol.invocation import CapabilityInvocation
from ...protocol.manifest import CapabilityManifest
from .errors import CapabilityTimeout, SandboxViolation
from .sandbox import SandboxPolicy, validate_output_tree


@dataclass(frozen=True)
class RawInvocationResult:
    returncode: int
    stdout: bytes
    stderr: bytes
    output_root: Path
    output_files: tuple[Path, ...]
    isolation_level: str


class CapabilityRunner:
    def __init__(self, policy: SandboxPolicy | None = None) -> None:
        self.policy = policy or SandboxPolicy()

    async def run(
        self,
        manifest: CapabilityManifest,
        invocation: CapabilityInvocation,
        command: list[str],
        *,
        input_files: dict[str, bytes] | None = None,
        workspace: str | Path | None = None,
    ) -> RawInvocationResult:
        if invocation.capability_id != manifest.capability_id or invocation.capability_version != manifest.capability_version:
            raise SandboxViolation("invocation does not match manifest")
        base = Path(workspace) if workspace else Path(tempfile.mkdtemp(prefix="zamery-capability-"))
        cleanup = workspace is None
        input_root = base / "inputs"
        output_root = base / "outputs"
        input_root.mkdir(parents=True, exist_ok=True)
        output_root.mkdir(parents=True, exist_ok=True)
        for relative, payload in (input_files or {}).items():
            target = input_root / relative
            if input_root.resolve() not in target.resolve().parents:
                raise SandboxViolation("input path escapes mount")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)
        effective = invocation.model_copy(update={"input_mount": str(input_root), "output_mount": str(output_root)})
        env = self.policy.environment()
        env["ZAMERY_INPUT_MOUNT"] = str(input_root)
        env["ZAMERY_OUTPUT_MOUNT"] = str(output_root)
        try:
            process = await asyncio.create_subprocess_exec(
                *command,
                cwd=base,
                env=env,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                start_new_session=(os.name != "nt"),
            )
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(encode_message(effective)), timeout=manifest.timeout_seconds
                )
            except TimeoutError as exc:
                if os.name != "nt":
                    os.killpg(process.pid, signal.SIGKILL)
                else:
                    process.kill()
                await process.wait()
                raise CapabilityTimeout(manifest.capability_id) from exc
            if len(stdout) > self.policy.max_stdout_bytes:
                raise SandboxViolation("stdout limit exceeded")
            if len(stderr) > self.policy.max_stderr_bytes:
                raise SandboxViolation("stderr limit exceeded")
            output_files = validate_output_tree(output_root, self.policy)
            return RawInvocationResult(process.returncode or 0, stdout, stderr, output_root, output_files, self.policy.isolation_level)
        finally:
            if cleanup:
                # Caller needs outputs for validation, so preserve successful workspaces.
                pass
