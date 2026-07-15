from zamery_education_v4.kernel.evidence.freshness import receipt_applies
from zamery_education_v4.kernel.records.evidence import EvidenceReceipt


def test_receipt_does_not_apply_to_a_different_binary() -> None:
    receipt = EvidenceReceipt(record_id="receipt:notes", receipt_type="speaker_notes", subject_hash="sha256:"+"a"*64, checker_id="pptx-notes-inspector", checker_version="4.0.0", checker_runtime_digest="sha256:"+"c"*64, policy_version="presentation-policy@4.0.0", result="pass", findings=())
    assert not receipt_applies(receipt, subject_hash="sha256:"+"b"*64, policy_version="presentation-policy@4.0.0")
