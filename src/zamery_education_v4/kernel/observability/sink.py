from __future__ import annotations
from pathlib import Path
from .events import RunEvent
from .redaction import redact_event
class JsonlEventSink:
    def __init__(self, path: str | Path) -> None: self.path=Path(path)
    def emit(self, event: RunEvent) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(redact_event(event).model_dump_json()+"\n")
