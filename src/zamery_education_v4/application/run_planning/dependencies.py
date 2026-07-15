from __future__ import annotations

from collections import defaultdict


def topological_order(dependencies: dict[str, tuple[str, ...]]) -> tuple[str, ...]:
    nodes = set(dependencies)
    for deps in dependencies.values():
        nodes.update(deps)
    indegree = {node: 0 for node in nodes}
    dependents: dict[str, set[str]] = defaultdict(set)
    for node, deps in dependencies.items():
        for dep in deps:
            indegree[node] += 1
            dependents[dep].add(node)
    ready = sorted(node for node, degree in indegree.items() if degree == 0)
    result: list[str] = []
    while ready:
        node = ready.pop(0)
        result.append(node)
        for child in sorted(dependents[node]):
            indegree[child] -= 1
            if indegree[child] == 0:
                ready.append(child)
                ready.sort()
    if len(result) != len(nodes):
        raise ValueError("capability dependency cycle")
    return tuple(result)
