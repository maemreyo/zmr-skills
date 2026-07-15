from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def render_to_pdf(source: str | Path, output_dir: str | Path, *, timeout_seconds: int = 120) -> Path:
    executable = shutil.which("libreoffice") or shutil.which("soffice")
    if executable is None:
        raise RuntimeError("LibreOffice is not installed")
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run([executable, "--headless", "--convert-to", "pdf", "--outdir", str(output_dir), str(source)], check=True, timeout=timeout_seconds, capture_output=True)
    output = output_dir / (Path(source).stem + ".pdf")
    if not output.exists():
        raise RuntimeError("LibreOffice did not produce expected PDF")
    return output
