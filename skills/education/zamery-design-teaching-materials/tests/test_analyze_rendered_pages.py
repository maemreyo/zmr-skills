import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

from scripts.analyze_rendered_pages import analyze_page


class RenderedPageTests(unittest.TestCase):
    def page(self, ratio: float) -> Path:
        directory = Path(tempfile.mkdtemp())
        path = directory / "page.png"
        image = Image.new("RGB", (200, 300), "white")
        draw = ImageDraw.Draw(image)
        height = int(300 * ratio)
        draw.rectangle((0, 0, 199, max(height - 1, 0)), fill="black")
        image.save(path)
        return path

    def test_sparse_page_is_flagged(self) -> None:
        report = analyze_page(self.page(0.08))
        self.assertTrue(report["sparse"])
        self.assertLess(report["occupied_ratio"], 0.25)

    def test_meaningfully_filled_page_passes(self) -> None:
        report = analyze_page(self.page(0.55))
        self.assertFalse(report["sparse"])
        self.assertGreater(report["occupied_ratio"], 0.5)


if __name__ == "__main__":
    unittest.main()
