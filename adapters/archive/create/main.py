from __future__ import annotations
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

def create_archive(output: str | Path, files: dict[str, bytes]) -> Path:
    output=Path(output); output.parent.mkdir(parents=True,exist_ok=True)
    normalized: set[str]=set()
    with ZipFile(output,"w",compression=ZIP_DEFLATED) as archive:
        for name,payload in sorted(files.items()):
            clean=name.replace("\\","/").strip("/")
            folded=clean.casefold()
            if not clean or clean.startswith("../") or "/../" in f"/{clean}" or folded in normalized: raise ValueError(f"unsafe or duplicate archive path: {name}")
            normalized.add(folded)
            info=ZipInfo(clean,date_time=(1980,1,1,0,0,0)); info.compress_type=ZIP_DEFLATED; info.external_attr=0o100644 << 16
            archive.writestr(info,payload)
    return output
