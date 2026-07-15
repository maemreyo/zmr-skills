from __future__ import annotations

from pathlib import Path

from zamery_education_v4.kernel.hashing import content_hash, sha256_file

from .geometry import analyze_geometry, page_occupancy


def analyze_page(path: str | Path, role: str) -> dict[str, object]:
    findings = analyze_geometry(path, role)
    occupancy = page_occupancy(path)
    return {
        "result": "fail" if findings else "pass",
        "findings": findings,
        "page_hash": sha256_file(path),
        "occupancy": occupancy,
        "semantic_fingerprint": content_hash(
            {
                "role": role,
                "occupancy_basis_points": round(occupancy * 10_000),
                "findings": findings,
            }
        ),
    }
