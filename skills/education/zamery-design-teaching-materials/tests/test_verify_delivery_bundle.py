import io
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.verify_delivery_bundle import verify_delivery_bundle


def nested_ooxml() -> bytes:
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", "<Types />")
        archive.writestr("docProps/core.xml", "<coreProperties />")
    return stream.getvalue()


class DeliveryBundleTests(unittest.TestCase):
    def bundle(self, entries: dict[str, bytes]) -> Path:
        path = Path(tempfile.mkdtemp()) / "bundle.zip"
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
            for name, data in entries.items():
                archive.writestr(name, data)
        return path

    def test_valid_bundle_passes(self) -> None:
        path = self.bundle({"teacher.docx": nested_ooxml(), "slides.pptx": nested_ooxml()})
        self.assertEqual(verify_delivery_bundle(path, ("teacher.docx", "slides.pptx")), [])

    def test_truncated_outer_zip_is_rejected(self) -> None:
        path = Path(tempfile.mkdtemp()) / "broken.zip"
        path.write_bytes(b"PK\x03\x04truncated")
        self.assertIn("delivery bundle is not a readable ZIP archive", verify_delivery_bundle(path, ()))

    def test_corrupt_nested_pptx_is_rejected(self) -> None:
        path = self.bundle({"slides.pptx": b"not-ooxml"})
        self.assertIn("nested OOXML file slides.pptx is corrupt", verify_delivery_bundle(path, ("slides.pptx",)))

    def test_missing_required_file_is_rejected(self) -> None:
        path = self.bundle({"teacher.docx": nested_ooxml()})
        self.assertIn("missing required file slides.pptx", verify_delivery_bundle(path, ("teacher.docx", "slides.pptx")))


if __name__ == "__main__":
    unittest.main()
