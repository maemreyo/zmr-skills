from __future__ import annotations

import argparse
import json
from pathlib import Path

from zamery_education_v4.kernel.records.registry import default_registry
from zamery_education_v4.protocol.invocation import CapabilityInvocation
from zamery_education_v4.protocol.manifest import CapabilityManifest
from zamery_education_v4.protocol.result import CapabilityFailure, CapabilityResult, OutputDeclaration


def _write_schemas(target: Path, schemas: dict[str, dict[str, object]]) -> None:
    target.mkdir(parents=True, exist_ok=True)
    for name, schema in sorted(schemas.items()):
        (target / f"{name}.schema.json").write_text(
            json.dumps(schema, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--group", choices=("records", "protocol", "all"), default="records")
    parser.add_argument("--output")
    args = parser.parse_args()

    if args.group in {"records", "all"}:
        target = Path(args.output or "schemas/v4/records")
        _write_schemas(target, default_registry().export_schemas())
    if args.group in {"protocol", "all"}:
        target = Path(args.output or "schemas/v4/protocol")
        models = (CapabilityManifest, CapabilityInvocation, OutputDeclaration, CapabilityResult, CapabilityFailure)
        _write_schemas(target, {model.__name__: model.model_json_schema() for model in models})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
