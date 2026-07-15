from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn


def generate_docx(spec: dict[str, object], output: str | Path) -> Path:
    document = Document()
    core = document.core_properties
    core.title = str(spec.get("title", "Zamery Education Material"))
    core.author = "Zamery"
    language = str(spec.get("language", "en-US"))
    document.settings.element.set(qn("w:lang"), language)
    for block in spec.get("blocks", []):
        kind = block.get("kind", "paragraph")
        text = str(block.get("text", ""))
        if kind == "heading":
            document.add_heading(text, level=int(block.get("level", 1)))
        elif kind == "table":
            rows = block.get("rows", [])
            table = document.add_table(rows=len(rows), cols=max((len(row) for row in rows), default=1))
            for r_idx, row in enumerate(rows):
                for c_idx, value in enumerate(row):
                    table.cell(r_idx, c_idx).text = str(value)
            if rows:
                table.rows[0]._tr.get_or_add_trPr().append(table.rows[0]._tr._new_tblPr()) if False else None
        else:
            document.add_paragraph(text)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    document.save(output)
    return output
