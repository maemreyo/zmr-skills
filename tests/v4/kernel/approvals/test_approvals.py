from datetime import UTC, datetime

from zamery_education_v4.kernel.approvals import ApprovalAuthority
from zamery_education_v4.kernel.records.approvals import ApprovalRecord


def approval_for(digest: str) -> ApprovalRecord:
    return ApprovalRecord(
        record_id="approval:1", scope="teaching_brief", approved_hashes=(digest,),
        approver_role="teacher", approved_at=datetime(2026, 7, 15, tzinfo=UTC),
    )


def test_approval_is_stale_after_subject_change() -> None:
    authority = ApprovalAuthority()
    authority.add(approval_for("sha256:" + "a" * 64))
    result = authority.resolve("teaching_brief", ("sha256:" + "b" * 64,))
    assert not result.approved
    assert result.reason == "APPROVAL_STALE"


def test_exact_hash_is_approved() -> None:
    authority = ApprovalAuthority()
    approval = approval_for("sha256:" + "a" * 64)
    authority.add(approval)
    assert authority.require("teaching_brief", approval.approved_hashes) == approval.calculated_hash


def test_superseded_approval_is_not_authoritative() -> None:
    authority = ApprovalAuthority()
    old = approval_for("sha256:" + "a" * 64)
    authority.add(old)
    replacement = ApprovalRecord(
        record_id="approval:2",
        scope="teaching_brief",
        approved_hashes=("sha256:" + "b" * 64,),
        approver_role="teacher",
        approved_at=datetime(2026, 7, 16, tzinfo=UTC),
        supersedes=(old.record_id,),
    )
    authority.add(replacement)
    assert authority.resolve("teaching_brief", old.approved_hashes).reason == "APPROVAL_STALE"
    assert authority.resolve("teaching_brief", replacement.approved_hashes).approved
