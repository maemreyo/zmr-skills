from __future__ import annotations

from collections import defaultdict, deque

from ...kernel.graph.model import PackGraph
from .models import ImpactReport


def analyze_impact(*, graph: PackGraph, changed_ids: tuple[str, ...], all_record_ids: tuple[str, ...] | None = None) -> ImpactReport:
    reverse: dict[str, set[str]] = defaultdict(set)
    reasons: dict[str, set[str]] = defaultdict(set)
    for edge in graph.edges:
        reverse[edge.source_id].add(edge.target_id)
        reasons[edge.target_id].add(str(edge.edge_type))
    invalidated = set(changed_ids)
    queue = deque(changed_ids)
    while queue:
        current = queue.popleft()
        for dependent in sorted(reverse[current]):
            if dependent not in invalidated:
                invalidated.add(dependent)
                queue.append(dependent)
    universe = set(all_record_ids or tuple(record.record_id for record in graph.records))
    return ImpactReport(
        changed_ids=tuple(sorted(changed_ids)), invalidated_ids=tuple(sorted(invalidated)),
        preserved_ids=tuple(sorted(universe - invalidated)),
        reasons={key: tuple(sorted(value)) for key, value in sorted(reasons.items()) if key in invalidated},
        material=bool(changed_ids),
    )
