from __future__ import annotations

import re
import unicodedata

from zamery_education_v4.kernel.hashing import content_hash


_WHITESPACE = re.compile(r"\s+")


def normalize_visible_text(value: str) -> str:
    return _WHITESPACE.sub(
        " ",
        unicodedata.normalize("NFC", value),
    ).strip()


def semantic_text_fingerprint(value: str) -> str:
    return content_hash({"visible_text": normalize_visible_text(value)})
