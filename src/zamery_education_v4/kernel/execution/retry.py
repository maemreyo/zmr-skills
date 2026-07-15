from __future__ import annotations


def should_retry(*, attempt: int, max_attempts: int, failure_code: str, retryable_codes: tuple[str, ...]) -> bool:
    return attempt < max_attempts and failure_code in retryable_codes
