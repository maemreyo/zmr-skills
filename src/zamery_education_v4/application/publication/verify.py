from __future__ import annotations

import stat
import tempfile
from pathlib import Path, PurePosixPath
from zipfile import BadZipFile, ZipFile

from adapters.docx.inspect import inspect_docx
from adapters.libreoffice.render.main import render_to_pdf
from adapters.pdf.inspect import inspect_pdf
from adapters.pptx.inspect import inspect_pptx

from ...kernel.hashing import sha256_file


def inspect_archive(
    path: str | Path,
    *,
    expected_members: dict[str, str] | None = None,
    extract_to: str | Path | None = None,
    max_files: int = 10_000,
    max_uncompressed_bytes: int = 1_073_741_824,
) -> dict[str, object]:
    path = Path(path)
    findings: list[str] = []
    seen: set[str] = set()
    extracted: dict[str, str] = {}
    try:
        with ZipFile(path) as archive:
            bad = archive.testzip()
            if bad:
                findings.append("ARCHIVE_CRC_FAILURE")
            infos = archive.infolist()
            file_infos = [info for info in infos if not info.is_dir()]
            if len(file_infos) > max_files:
                findings.append("ARCHIVE_FILE_COUNT_EXCEEDED")
            if sum(info.file_size for info in file_infos) > max_uncompressed_bytes:
                findings.append("ARCHIVE_SIZE_LIMIT_EXCEEDED")
            for info in infos:
                name = info.filename
                canonical_name = name.replace("\\", "/")
                posix = PurePosixPath(canonical_name)
                normalized = posix.as_posix().casefold()
                if "\x00" in name or posix.is_absolute() or ".." in posix.parts or (posix.parts and ":" in posix.parts[0]):
                    findings.append("ARCHIVE_PATH_TRAVERSAL")
                if normalized in seen:
                    findings.append("ARCHIVE_CASE_COLLISION")
                seen.add(normalized)
                mode = info.external_attr >> 16
                if stat.S_ISLNK(mode):
                    findings.append("ARCHIVE_SYMLINK")
                if info.flag_bits & 0x1:
                    findings.append("ARCHIVE_ENCRYPTED_ENTRY")
            actual_members = {
                info.filename
                for info in infos
                if not info.is_dir()
            }
            if (
                expected_members is not None
                and actual_members != set(expected_members)
            ):
                findings.append("ARCHIVE_MEMBERSHIP_MISMATCH")
            if extract_to is not None and not findings:
                root = Path(extract_to).resolve()
                root.mkdir(parents=True, exist_ok=True)
                for info in infos:
                    if info.is_dir():
                        continue
                    target = (root / info.filename).resolve()
                    if root not in target.parents:
                        findings.append("ARCHIVE_PATH_TRAVERSAL")
                        continue
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(archive.read(info))
                    extracted[info.filename] = sha256_file(target)
    except BadZipFile:
        findings.append("ARCHIVE_INVALID_ZIP")
    if expected_members is not None and extracted:
        for name, digest in expected_members.items():
            if extracted.get(name) != digest:
                findings.append("ARCHIVE_EXTRACTED_HASH_MISMATCH")
    return {
        "result": "fail" if findings else "pass",
        "findings": sorted(set(findings)),
        "archive_hash": sha256_file(path),
        "extracted_hashes": extracted,
    }


def verify_extracted_bundle(
    root: str | Path,
    *,
    rerender: bool = True,
) -> dict[str, object]:
    root = Path(root)
    findings: list[str] = []
    artifacts: dict[str, dict[str, object]] = {}
    renders: dict[str, dict[str, object]] = {}
    with tempfile.TemporaryDirectory(prefix="zamery-rerender-") as temp:
        render_root = Path(temp)
        for path in sorted(item for item in root.rglob("*") if item.is_file()):
            relative = path.relative_to(root).as_posix()
            suffix = path.suffix.casefold()
            if suffix == ".docx":
                inspection = inspect_docx(path)
            elif suffix == ".pptx":
                inspection = inspect_pptx(path)
            elif suffix == ".pdf":
                inspection = inspect_pdf(path)
            else:
                continue
            artifacts[relative] = inspection
            findings.extend(str(item) for item in inspection.get("findings", []))
            if rerender and suffix in {".docx", ".pptx"}:
                try:
                    rendered = render_to_pdf(path, render_root / path.stem)
                    render_inspection = inspect_pdf(rendered)
                    renders[relative] = render_inspection
                    findings.extend(
                        str(item)
                        for item in render_inspection.get("findings", [])
                        if not str(item).startswith("PDF_TITLE_MISSING")
                    )
                    if (
                        inspection.get("semantic_fingerprint")
                        != render_inspection.get("semantic_fingerprint")
                    ):
                        findings.append(
                            f"SEMANTIC_FINGERPRINT_MISMATCH:{relative}"
                        )
                except Exception:
                    findings.append(f"RERENDER_FAILED:{relative}")
    return {
        "result": "fail" if findings else "pass",
        "findings": sorted(set(findings)),
        "artifacts": artifacts,
        "renders": renders,
        "reopened": bool(artifacts),
        "rerendered": bool(renders) if rerender else False,
    }


def verify_published_archive(
    archive_path: str | Path,
    *,
    expected_members: dict[str, str],
) -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="zamery-publish-verify-") as temp:
        archive_result = inspect_archive(
            archive_path,
            expected_members=expected_members,
            extract_to=temp,
        )
        if archive_result["result"] != "pass":
            return {
                "result": "fail",
                "findings": archive_result["findings"],
                "archive": archive_result,
                "bundle": None,
            }
        bundle_result = verify_extracted_bundle(temp)
        return {
            "result": bundle_result["result"],
            "findings": bundle_result["findings"],
            "archive": archive_result,
            "bundle": bundle_result,
        }
