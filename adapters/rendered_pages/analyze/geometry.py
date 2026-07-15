from __future__ import annotations

from pathlib import Path

import yaml
from PIL import Image


DEFAULT_ROLE_POLICY = Path("policies/v4/presentation/page-roles.yaml")


def page_occupancy(path: str | Path) -> float:
    image = Image.open(path).convert("L")
    values = image.tobytes()
    if not values:
        return 0.0
    non_white = sum(1 for value in values if value < 245)
    return non_white / len(values)


def _role_bounds(
    page_role: str,
    policy_path: str | Path = DEFAULT_ROLE_POLICY,
) -> tuple[float, float]:
    policies = yaml.safe_load(Path(policy_path).read_text(encoding="utf-8"))
    policy = policies.get(page_role, {})
    return (
        float(policy.get("min_occupancy", 0.005)),
        float(policy.get("max_occupancy", 0.90)),
    )


def analyze_geometry(
    path: str | Path,
    page_role: str,
    *,
    policy_path: str | Path = DEFAULT_ROLE_POLICY,
) -> tuple[str, ...]:
    occupancy = page_occupancy(path)
    minimum, maximum = _role_bounds(page_role, policy_path)
    findings: list[str] = []
    if occupancy < 0.005:
        findings.append("ACCIDENTAL_BLANK_PAGE")
    elif occupancy < minimum:
        findings.append("PAGE_ROLE_UNDERFILLED")
    if occupancy > maximum:
        findings.append("PAGE_ROLE_OVERFILLED")
    return tuple(findings)
