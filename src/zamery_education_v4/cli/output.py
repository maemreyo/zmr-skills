from __future__ import annotations

import json


def emit(payload: object, *, as_json: bool = False) -> str:
    if as_json:
        return json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    if isinstance(payload, str):
        return payload
    return json.dumps(payload, indent=2, sort_keys=True, default=str)
