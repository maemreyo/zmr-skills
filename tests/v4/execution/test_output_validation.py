from pathlib import Path

import pytest

from zamery_education_v4.kernel.execution.errors import OutputHashMismatch
from zamery_education_v4.kernel.execution.output_validation import validate_outputs
from zamery_education_v4.kernel.records.registry import default_registry
from zamery_education_v4.protocol.manifest import CapabilityManifest
from zamery_education_v4.protocol.result import CapabilityResult, OutputDeclaration


def test_kernel_recalculates_declared_hash(tmp_path: Path) -> None:
    (tmp_path / "brief.json").write_text('{"record_type":"teaching_brief","schema_version":"4.0.0","record_id":"brief:1","duration_minutes":90,"learner_level":"A2","source_ids":[],"lifecycle_goal":"publish_teaching_pack","requested_deliverables":[],"constraints":[]}')
    result = CapabilityResult(invocation_id="i", outputs=(OutputDeclaration(output_type="brief", path="brief.json", declared_hash="sha256:"+"0"*64, record_type="teaching_brief"),))
    manifest = CapabilityManifest(capability_id="c", capability_version="1", outputs=("brief",), deterministic=True, runtime_kind="python", runtime_version="3.12", runtime_digest="sha256:"+"a"*64, lockfile_hash="sha256:"+"b"*64)
    with pytest.raises(OutputHashMismatch):
        validate_outputs(result, output_root=tmp_path, manifest=manifest, registry=default_registry())
