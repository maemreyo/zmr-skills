from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from ..records.approvals import ApprovalRecord
from .policy import role_can_approve


class ApprovalResolution(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)
    approved: bool
    reason: str
    approval_hash: str | None = None
    approval_record_id: str | None = None


class ApprovalAuthority:
    def __init__(self) -> None:
        self._approvals: dict[str, ApprovalRecord] = {}

    def add(self, approval: ApprovalRecord) -> None:
        if not role_can_approve(approval.approver_role, str(approval.scope)):
            raise PermissionError(
                f"role {approval.approver_role!r} cannot approve {approval.scope!r}"
            )
        unknown_superseded = set(approval.supersedes) - set(self._approvals)
        unknown_revoked = set(approval.revokes) - set(self._approvals)
        if unknown_superseded or unknown_revoked:
            raise ValueError(
                "approval references unknown records: "
                f"supersedes={sorted(unknown_superseded)}, "
                f"revokes={sorted(unknown_revoked)}"
            )
        self._approvals[approval.record_id] = approval

    def _inactive_record_ids(self) -> set[str]:
        inactive: set[str] = set()
        for approval in self._approvals.values():
            inactive.update(approval.revokes)
            inactive.update(approval.supersedes)
        return inactive

    def resolve(
        self,
        scope: str,
        subject_hashes: tuple[str, ...],
    ) -> ApprovalResolution:
        expected = tuple(sorted(set(subject_hashes)))
        inactive = self._inactive_record_ids()
        scoped = [
            approval
            for approval in self._approvals.values()
            if str(approval.scope) == scope
            and approval.record_id not in inactive
        ]
        candidates = [
            approval
            for approval in scoped
            if tuple(approval.approved_hashes) == expected
        ]
        if candidates:
            approval = max(
                candidates,
                key=lambda item: (item.approved_at, item.record_id),
            )
            return ApprovalResolution(
                approved=True,
                reason="APPROVED",
                approval_hash=approval.calculated_hash,
                approval_record_id=approval.record_id,
            )
        return ApprovalResolution(
            approved=False,
            reason="APPROVAL_STALE" if scoped else "APPROVAL_MISSING",
        )

    def require(self, scope: str, subject_hashes: tuple[str, ...]) -> str:
        result = self.resolve(scope, subject_hashes)
        if not result.approved or result.approval_hash is None:
            raise PermissionError(result.reason)
        return result.approval_hash
