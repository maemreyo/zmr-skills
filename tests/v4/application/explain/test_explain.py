from zamery_education_v4.application.explain import explain_record


def test_explanation_sorts_provenance_edges() -> None:
    result = explain_record(
        "artifact:1",
        incoming=("source:b", "source:a"),
        outgoing=("receipt:z", "receipt:a"),
    )
    assert result["incoming"] == ["source:a", "source:b"]
    assert result["outgoing"] == ["receipt:a", "receipt:z"]
