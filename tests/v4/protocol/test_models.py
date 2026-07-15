import pytest
from pydantic import ValidationError

from zamery_education_v4.protocol.result import CapabilityResult, OutputDeclaration


def test_duplicate_output_path_is_rejected() -> None:
    output = OutputDeclaration(output_type="x", path="same", declared_hash="sha256:" + "a" * 64)
    with pytest.raises(ValidationError):
        CapabilityResult(invocation_id="i", outputs=(output, output))
