from zamery_education_v4.kernel.observability import RunEvent, redact_event

def test_redaction_removes_pii_and_secrets_but_preserves_hashes() -> None:
    event=RunEvent(event_type="RUN_PLANNED",run_id="r1",data={"student_name":"Protected","api_key":"secret","record_hash":"sha256:"+"a"*64})
    output=redact_event(event).model_dump_json()
    assert "Protected" not in output and "secret" not in output and "sha256:" in output
