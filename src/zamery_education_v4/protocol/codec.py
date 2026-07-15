from __future__ import annotations

import json

from pydantic import TypeAdapter, ValidationError

from ..kernel.canonical_json import canonical_json_bytes
from .manifest import CapabilityManifest
from .result import CapabilityFailure, CapabilityResult


class ProtocolViolation(ValueError):
    pass


_RESULT_ADAPTER = TypeAdapter(CapabilityResult | CapabilityFailure)


def encode_message(message: object) -> bytes:
    if hasattr(message, "model_dump"):
        return canonical_json_bytes(message.model_dump(mode="json", exclude_none=True))
    return canonical_json_bytes(message)


def decode_result(
    payload: bytes,
    *,
    expected_invocation_id: str | None = None,
    manifest: CapabilityManifest | None = None,
) -> CapabilityResult | CapabilityFailure:
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ProtocolViolation("stdout must be UTF-8") from exc
    decoder = json.JSONDecoder()
    stripped = text.lstrip()
    if not stripped:
        raise ProtocolViolation("stdout must contain exactly one JSON object")
    try:
        value, end = decoder.raw_decode(stripped)
    except json.JSONDecodeError as exc:
        raise ProtocolViolation("stdout must contain exactly one JSON object") from exc
    if stripped[end:].strip():
        raise ProtocolViolation("stdout must contain exactly one JSON object")
    if not isinstance(value, dict):
        raise ProtocolViolation("protocol message must be an object")
    try:
        result = _RESULT_ADAPTER.validate_json(stripped, strict=True)
    except ValidationError as exc:
        raise ProtocolViolation(str(exc)) from exc
    if expected_invocation_id is not None and result.invocation_id != expected_invocation_id:
        raise ProtocolViolation("wrong invocation id")
    if manifest is not None:
        if isinstance(result, CapabilityFailure):
            if manifest.failure_codes and result.failure_code not in manifest.failure_codes:
                raise ProtocolViolation("undeclared failure code")
        else:
            undeclared = {output.output_type for output in result.outputs} - set(manifest.outputs)
            if undeclared:
                raise ProtocolViolation(f"undeclared output type: {sorted(undeclared)}")
    return result
