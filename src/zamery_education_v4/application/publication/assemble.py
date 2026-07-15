from __future__ import annotations

from pathlib import Path, PurePosixPath
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from ...kernel.hashing import sha256_file


def assemble_bundle(*, members: dict[str, str], source_root: str | Path, output_path: str | Path) -> Path:
    source_root = Path(source_root).resolve()
    actual = {path.relative_to(source_root).as_posix() for path in source_root.rglob("*") if path.is_file()}
    expected = set(members)
    if actual != expected:
        raise ValueError(f"bundle membership mismatch: missing={sorted(expected-actual)} unknown={sorted(actual-expected)}")
    normalized: set[str] = set()
    for relative, digest in members.items():
        normalized_relative = relative.replace("\\", "/")
        posix = PurePosixPath(normalized_relative)
        if "\x00" in relative or posix.is_absolute() or ".." in posix.parts or (posix.parts and ":" in posix.parts[0]):
            raise ValueError(f"unsafe bundle path: {relative}")
        key = posix.as_posix().casefold()
        if key in normalized:
            raise ValueError(f"duplicate normalized path: {relative}")
        normalized.add(key)
        if sha256_file(source_root / relative) != digest:
            raise ValueError(f"file hash mismatch: {relative}")
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output_path, "w") as archive:
        for relative in sorted(members):
            info = ZipInfo(relative, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, (source_root / relative).read_bytes())
    return output_path
