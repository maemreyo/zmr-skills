from __future__ import annotations

def explain_record(record_id: str, *, incoming: tuple[str,...]=(), outgoing: tuple[str,...]=()) -> dict[str, object]:
    return {"record_id":record_id,"incoming":sorted(incoming),"outgoing":sorted(outgoing),"next_actions":[]}

def explain_gate_decision(decision: object) -> dict[str, object]:
    payload=decision.model_dump(mode="json") if hasattr(decision,"model_dump") else dict(decision)
    return {"gate":payload.get("gate"),"decision":payload.get("decision"),"findings":payload.get("findings",[]),"required_repair":payload.get("decision") == "fail"}
