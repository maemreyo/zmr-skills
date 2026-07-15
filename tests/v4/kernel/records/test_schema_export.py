import json
from pathlib import Path


def test_record_and_protocol_schemas_are_committed() -> None:
    record_schemas = list(Path("schemas/v4/records").glob("*.schema.json"))
    protocol_schemas = list(Path("schemas/v4/protocol").glob("*.schema.json"))
    assert len(record_schemas) >= 15
    assert len(protocol_schemas) == 5
    for path in record_schemas + protocol_schemas:
        schema = json.loads(path.read_text())
        assert "$defs" in schema or "properties" in schema
