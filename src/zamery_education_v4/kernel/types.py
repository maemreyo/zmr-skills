from __future__ import annotations

import re
from typing import Annotated

from pydantic import AfterValidator

_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


def validate_record_hash(value: str) -> str:
    if not _HASH_RE.fullmatch(value):
        raise ValueError("expected sha256:<64 lowercase hex characters>")
    return value


RecordHash = Annotated[str, AfterValidator(validate_record_hash)]
RecordId = Annotated[str, AfterValidator(lambda value: value if value.strip() else (_ for _ in ()).throw(ValueError("record id cannot be blank")))]
