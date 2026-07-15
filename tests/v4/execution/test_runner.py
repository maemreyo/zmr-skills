import json
import sys
from pathlib import Path

import pytest

from zamery_education_v4.kernel.execution.runner import CapabilityRunner
from zamery_education_v4.protocol.codec import decode_result
from zamery_education_v4.protocol.invocation import CapabilityInvocation
from zamery_education_v4.protocol.manifest import CapabilityManifest


def manifest() -> CapabilityManifest:
    return CapabilityManifest(capability_id="reference.python_echo", capability_version="4.0.0", outputs=("echo_record",), deterministic=True, runtime_kind="python", runtime_version="3.12", runtime_digest="sha256:"+"b"*64, lockfile_hash="sha256:"+"a"*64, failure_codes=("INVALID_INPUT",))


@pytest.mark.asyncio
async def test_reference_capability_runs(tmp_path: Path) -> None:
    runner = CapabilityRunner()
    invocation = CapabilityInvocation(invocation_id="i1", capability_id="reference.python_echo", capability_version="4.0.0")
    script = Path(__file__).parents[3] / "capabilities/reference/python_echo/main.py"
    result = await runner.run(manifest(), invocation, [sys.executable, str(script)], workspace=tmp_path)
    decoded = decode_result(result.stdout, expected_invocation_id="i1", manifest=manifest())
    assert decoded.status == "success"
