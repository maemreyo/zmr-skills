from __future__ import annotations
from pathlib import Path
from zamery_education_v4.application.publication.verify import inspect_archive as _inspect

def inspect_archive(path: str | Path) -> tuple[str,...]: return _inspect(Path(path))
