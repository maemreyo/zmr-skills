from __future__ import annotations

def export_h5p_manifest(title: str, source_url: str, transcript_hash: str) -> dict[str, object]:
    if not source_url.startswith("https://"): raise ValueError("H5P source must use HTTPS")
    if not transcript_hash.startswith("sha256:"): raise ValueError("transcript hash required")
    return {"title":title,"mainLibrary":"H5P.InteractiveVideo","embedTypes":["div"],"preloadedDependencies":[],"zamery":{"source_url":source_url,"transcript_hash":transcript_hash}}
