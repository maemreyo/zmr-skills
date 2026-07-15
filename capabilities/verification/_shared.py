from __future__ import annotations

import json
import sys
from collections.abc import Callable
from pathlib import Path

from zamery_education_v4.kernel.canonical_json import canonical_json_bytes
from zamery_education_v4.kernel.evidence.inspectors import (
    inspect_answer_authority,
    inspect_decision_rule,
    inspect_objective_coverage,
    inspect_source_lineage,
)
from zamery_education_v4.kernel.evidence.safety import (
    inspect_accessibility,
    inspect_answer_separation,
    inspect_safety,
)
from zamery_education_v4.kernel.records.evidence import EvidenceReceipt


Inspector = Callable[[dict[str, object]], EvidenceReceipt]


def _safety(payload: dict[str, object]) -> EvidenceReceipt:
    return inspect_safety(payload)[0]


def _privacy(payload: dict[str, object]) -> EvidenceReceipt:
    return inspect_safety(payload)[1]


INSPECTORS: dict[str, Inspector] = {
    "source_lineage": inspect_source_lineage,
    "objective_coverage": inspect_objective_coverage,
    "answer_authority": inspect_answer_authority,
    "decision_rule": inspect_decision_rule,
    "safety": _safety,
    "privacy_homework": _privacy,
    "accessibility": inspect_accessibility,
    "answer_separation": inspect_answer_separation,
}


def run(kind: str) -> int:
    invocation = json.load(sys.stdin)
    invocation_id = str(invocation["invocation_id"])
    output_mount = Path(str(invocation["output_mount"]))
    configuration = invocation.get("configuration") or {}
    payload = configuration.get("payload") or {}
    if not isinstance(payload, dict):
        raise ValueError("configuration.payload must be an object")

    receipt = INSPECTORS[kind](payload)
    output_mount.mkdir(parents=True, exist_ok=True)
    relative_path = "receipt.json"
    output_path = output_mount / relative_path
    output_path.write_bytes(canonical_json_bytes(receipt.canonical_payload()))

    result = {
        "protocol_version": "zamery-capability.v1",
        "status": "success",
        "invocation_id": invocation_id,
        "outputs": [
            {
                "output_type": "evidence_receipt",
                "path": relative_path,
                "declared_hash": receipt.calculated_hash,
                "record_type": receipt.record_type,
            }
        ],
        "metrics": {
            "finding_count": len(receipt.findings),
            "result": receipt.result,
        },
    }
    json.dump(result, sys.stdout, sort_keys=True, separators=(",", ":"))
    return 0
