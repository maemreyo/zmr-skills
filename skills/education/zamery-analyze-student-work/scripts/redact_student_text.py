"""Deterministic PII redaction that supplements, not replaces, manual visual review."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

EMAIL = re.compile(r"(?<![\w.+-])[\w.+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?!\w)")
PHONE = re.compile(r"(?<!\w)(?:\+?84|0)(?:[\s.-]*\d){8,10}(?!\d)")
STUDENT_ID = re.compile(
    r"(?i)\b(?:student[\s-]*id|id\s+học\s+sinh|mã\s+học\s+sinh)\s*[:#-]?\s*[A-Z0-9][A-Z0-9_-]*"
)


def redact_student_text(
    text: str,
    known_names: tuple[str, ...] = (),
) -> tuple[str, tuple[str, ...]]:
    """Replace deterministic identifiers and return finding categories in text order."""
    patterns: list[tuple[str, str, re.Pattern[str]]] = [
        ("email", "[EMAIL]", EMAIL),
        ("phone", "[PHONE]", PHONE),
        ("student_id", "[STUDENT_ID]", STUDENT_ID),
    ]
    names = [name.strip() for name in known_names if name.strip()]
    if names:
        name_pattern = re.compile(
            "|".join(sorted((re.escape(name) for name in names), key=len, reverse=True)),
            re.IGNORECASE,
        )
        patterns.append(("known_name", "[STUDENT_NAME]", name_pattern))

    candidates: list[tuple[int, int, str, str]] = []
    for category, replacement, pattern in patterns:
        for match in pattern.finditer(text):
            candidates.append((match.start(), match.end(), category, replacement))
    candidates.sort(key=lambda item: (item[0], -(item[1] - item[0])))

    accepted: list[tuple[int, int, str, str]] = []
    cursor = -1
    for match in candidates:
        if match[0] < cursor:
            continue
        accepted.append(match)
        cursor = match[1]

    output: list[str] = []
    findings: list[str] = []
    cursor = 0
    for start, end, category, replacement in accepted:
        output.append(text[cursor:start])
        output.append(replacement)
        cursor = end
        if category not in findings:
            findings.append(category)
    output.append(text[cursor:])
    return "".join(output), tuple(findings)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--name", action="append", default=[])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    source = args.input.read_text(encoding="utf-8")
    redacted, findings = redact_student_text(source, tuple(args.name))
    if args.output:
        args.output.write_text(redacted, encoding="utf-8")
    else:
        print(redacted)
    print("findings=" + ",".join(findings))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
