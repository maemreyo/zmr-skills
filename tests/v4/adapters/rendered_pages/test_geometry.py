from pathlib import Path

from PIL import Image

from adapters.rendered_pages.analyze.geometry import analyze_geometry


def test_analyzer_does_not_use_nonexistent_pillow_api() -> None:
    source = (Path(__file__).parents[4] / "adapters/rendered_pages/analyze/geometry.py").read_text()
    assert "get_flattened_data" not in source


def test_blank_page_is_detected(tmp_path: Path) -> None:
    path = tmp_path / "blank.png"
    Image.new("L", (100, 100), 255).save(path)
    assert "ACCIDENTAL_BLANK_PAGE" in analyze_geometry(path, "student_practice")
