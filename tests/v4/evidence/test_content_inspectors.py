from zamery_education_v4.kernel.evidence.inspectors import inspect_answer_authority, inspect_decision_rule, inspect_source_lineage


def test_denominator_mismatch_is_detected() -> None:
    receipt = inspect_decision_rule({"decision_rules":[{"record_id":"rule:1","member_item_ids":["i1","i2"],"denominator":3,"threshold":2}]})
    assert receipt.result == "fail"
    assert receipt.findings[0].code == "DECISION_RULE_DENOMINATOR_MISMATCH"


def test_missing_lineage_and_answer_authority_are_detected() -> None:
    payload = {"items":[{"record_id":"i1","scored":True,"source_ids":[]}],"answers":[]}
    assert inspect_source_lineage(payload).result == "fail"
    assert inspect_answer_authority(payload).result == "fail"
