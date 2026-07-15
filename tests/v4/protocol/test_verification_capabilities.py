from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from zamery_education_v4.kernel.records.registry import default_registry
from zamery_education_v4.protocol.codec import decode_result
from zamery_education_v4.protocol.manifest import CapabilityManifest


def test_source_lineage_capability_emits_valid_receipt(tmp_path: Path) -> None:
    capability_root = Path("capabilities/verification/source_lineage")
    manifest = CapabilityManifest.model_validate_json(
        (capability_root / "manifest.json").read_text()
    )
    output = tmp_path / "outputs"
    output.mkdir()
    invocation = {
        "protocol_version": "zamery-capability.v1",
        "invocation_id": "verify-1",
        "capability_id": manifest.capability_id,
        "capability_version": manifest.capability_version,
        "input_records": [],
        "configuration": {
            "payload": {
                "items": [
                    {"record_id": "item:1", "source_ids": []},
                ]
            }
        },
        "input_mount": str(tmp_path / "inputs"),
        "output_mount": str(output),
    }
    completed = subprocess.run(
        [sys.executable, str(capability_root / "main.py")],
        input=json.dumps(invocation).encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        env={"PYTHONPATH": "src:."},
    )
    result = decode_result(
        completed.stdout,
        expected_invocation_id="verify-1",
        manifest=manifest,
    )
    declared = result.outputs[0]
    payload = json.loads((output / declared.path).read_text())
    receipt = default_registry().parse(payload)
    assert receipt.calculated_hash == declared.declared_hash
    assert receipt.findings[0].code == "MISSING_SOURCE_LINEAGE"
