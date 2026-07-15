from __future__ import annotations
from .events import RunEvent
SENSITIVE_TOKENS=("student","learner_name","api_key","secret","token","password","email","phone")
def redact_event(event: RunEvent) -> RunEvent:
    return event.model_copy(update={"data":_redact(event.data)})
def _redact(value: object) -> object:
    if isinstance(value, dict):
        return {str(k):("[REDACTED]" if any(token in str(k).lower() for token in SENSITIVE_TOKENS) else _redact(v)) for k,v in value.items()}
    if isinstance(value, list): return [_redact(v) for v in value]
    if isinstance(value, tuple): return tuple(_redact(v) for v in value)
    return value
