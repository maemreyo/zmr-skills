import json
from pathlib import Path

from capabilities.composition.h5p_export import export_h5p_manifest


def test_video_learning_requires_provenance_fallback_and_privacy() -> None:
    data = json.loads(Path("goldens/v4/video-learning/manifest.json").read_text())
    assert all(data.values())
    manifest = export_h5p_manifest(
        "Unit 1 video",
        "https://example.edu/video/1",
        "sha256:" + "a" * 64,
    )
    assert manifest["mainLibrary"] == "H5P.InteractiveVideo"
