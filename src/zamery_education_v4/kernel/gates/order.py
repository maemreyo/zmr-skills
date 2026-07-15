GATE_ORDER = ("brief", "pedagogy", "content", "safety", "accessibility", "presentation", "pack")


def prior_gates(gate: str) -> tuple[str, ...]:
    try:
        index = GATE_ORDER.index(gate)
    except ValueError as exc:
        raise ValueError(f"unknown gate: {gate}") from exc
    return GATE_ORDER[:index]
