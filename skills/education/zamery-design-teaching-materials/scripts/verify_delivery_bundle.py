from __future__ import annotations

import argparse
import io
import zipfile
from pathlib import Path, PurePosixPath


def _safe_member(name: str) -> bool:
    path = PurePosixPath(name)
    return not path.is_absolute() and ".." not in path.parts


def _nested_ooxml_error(name: str, data: bytes) -> str | None:
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            if archive.testzip() is not None or "[Content_Types].xml" not in archive.namelist():
                return f"nested OOXML file {name} is corrupt"
    except (zipfile.BadZipFile, OSError):
        return f"nested OOXML file {name} is corrupt"
    return None


def verify_delivery_bundle(path: Path, required_names: tuple[str, ...]) -> list[str]:
    try:
        with zipfile.ZipFile(path) as archive:
            corrupt = archive.testzip()
            if corrupt is not None:
                return [f"delivery bundle CRC failed for {corrupt}"]
            names = archive.namelist()
            errors: list[str] = []
            for name in names:
                if not _safe_member(name):
                    errors.append(f"unsafe archive member {name}")
            for required in required_names:
                if required not in names:
                    errors.append(f"missing required file {required}")
            for name in names:
                if name.casefold().endswith((".docx", ".pptx")):
                    nested_error = _nested_ooxml_error(name, archive.read(name))
                    if nested_error:
                        errors.append(nested_error)
            return errors
    except (zipfile.BadZipFile, OSError, EOFError):
        return ["delivery bundle is not a readable ZIP archive"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--required", action="append", default=[])
    args = parser.parse_args()
    errors = verify_delivery_bundle(args.bundle, tuple(args.required))
    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
