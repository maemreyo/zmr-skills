from __future__ import annotations

from collections import defaultdict

from ..records.evidence import EvidenceReceipt, ReviewRecord


class EvidenceRegistry:
    def __init__(self) -> None:
        self._receipts: dict[str, EvidenceReceipt] = {}
        self._reviews: dict[str, ReviewRecord] = {}

    def add_receipt(self, receipt: EvidenceReceipt) -> None:
        self._receipts[receipt.record_id] = receipt

    def add_review(self, review: ReviewRecord) -> None:
        self._reviews[review.record_id] = review

    def receipts(self, *, receipt_type: str | None = None, subject_hash: str | None = None) -> tuple[EvidenceReceipt, ...]:
        values = self._receipts.values()
        return tuple(sorted((r for r in values if (receipt_type is None or r.receipt_type == receipt_type) and (subject_hash is None or r.subject_hash == subject_hash)), key=lambda r: r.record_id))

    def reviews(self, *, rubric_version: str | None = None, subject_hash: str | None = None) -> tuple[ReviewRecord, ...]:
        values = self._reviews.values()
        return tuple(sorted((r for r in values if (rubric_version is None or r.rubric_version == rubric_version) and (subject_hash is None or subject_hash in r.subject_hashes)), key=lambda r: r.record_id))
