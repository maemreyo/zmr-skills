from zamery_education_v4.kernel.gates import GateEngine


def test_pack_boolean_does_not_replace_reopen_receipt() -> None:
    engine = GateEngine()
    decision = engine.evaluate("pack", "sha256:"+"a"*64)
    assert decision.decision == "fail"
    assert "REOPEN_RECEIPT_MISSING" in {finding.code for finding in decision.findings}
