from __future__ import annotations

from pathlib import Path

from pptx import Presentation


def inspect_geometry(path: str | Path, *, minimum_font_points: float = 16.0) -> list[str]:
    presentation = Presentation(path)
    findings: list[str] = []
    for slide_index, slide in enumerate(presentation.slides, 1):
        for shape in slide.shapes:
            if shape.left < 0 or shape.top < 0 or shape.left + shape.width > presentation.slide_width or shape.top + shape.height > presentation.slide_height:
                findings.append(f"OFF_CANVAS_SHAPE:{slide_index}")
            if getattr(shape, "has_text_frame", False):
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        if run.font.size is not None and run.font.size.pt < minimum_font_points:
                            findings.append(f"PROJECTED_FONT_BELOW_FLOOR:{slide_index}")
    return findings
