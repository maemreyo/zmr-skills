from pathlib import Path
from zipfile import ZipFile

from zamery_education_v4.application.publication import assemble_bundle, inspect_archive
from zamery_education_v4.kernel.hashing import sha256_file


def test_exact_membership_and_clean_extract(tmp_path: Path) -> None:
    source = tmp_path / "source"; source.mkdir(); (source / "a.txt").write_text("a")
    members = {"a.txt": sha256_file(source / "a.txt")}
    archive = assemble_bundle(members=members, source_root=source, output_path=tmp_path / "bundle.zip")
    result = inspect_archive(archive, expected_members=members, extract_to=tmp_path / "extract")
    assert result["result"] == "pass"


def test_zip_slip_is_rejected(tmp_path: Path) -> None:
    archive = tmp_path / "bad.zip"
    with ZipFile(archive, "w") as out: out.writestr("../escape.txt", "x")
    assert "ARCHIVE_PATH_TRAVERSAL" in inspect_archive(archive)["findings"]


def test_case_collision_fixture_is_rejected() -> None:
    result = inspect_archive("tests/v4/fixtures/archives/case-collision.zip")
    assert "ARCHIVE_CASE_COLLISION" in result["findings"]


def test_symlink_fixture_is_rejected() -> None:
    result = inspect_archive("tests/v4/fixtures/archives/symlink.zip")
    assert "ARCHIVE_SYMLINK" in result["findings"]


def test_archive_limits_fail_closed(tmp_path: Path) -> None:
    archive = tmp_path / "many.zip"
    with ZipFile(archive, "w") as out:
        out.writestr("a.txt", "a")
        out.writestr("b.txt", "b")
    result = inspect_archive(archive, max_files=1)
    assert "ARCHIVE_FILE_COUNT_EXCEEDED" in result["findings"]
