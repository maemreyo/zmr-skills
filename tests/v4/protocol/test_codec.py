import pytest

from zamery_education_v4.protocol.codec import ProtocolViolation, decode_result


def test_decoder_rejects_logs_mixed_with_json() -> None:
    payload = b'loading model\n{"protocol_version":"zamery-capability.v1"}'
    with pytest.raises(ProtocolViolation, match="exactly one JSON object"):
        decode_result(payload)


def test_decoder_rejects_wrong_invocation() -> None:
    payload = b'{"protocol_version":"zamery-capability.v1","status":"failure","invocation_id":"other","failure_code":"X","message":"x","retryable":false,"affected_ids":[]}'
    with pytest.raises(ProtocolViolation, match="wrong invocation"):
        decode_result(payload, expected_invocation_id="expected")
