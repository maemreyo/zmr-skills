from __future__ import annotations

from pathlib import Path

from pptx import Presentation


def generate_pptx(spec: dict[str, object], output: str | Path) -> Path:
    presentation = Presentation()
    presentation.core_properties.title = str(spec.get("title", "Zamery Lesson"))
    for index, slide_spec in enumerate(spec.get("slides", [])):
        layout = presentation.slide_layouts[1]
        slide = presentation.slides.add_slide(layout)
        slide.shapes.title.text = str(slide_spec.get("title", f"Slide {index+1}"))
        body = slide.placeholders[1]
        body.text = str(slide_spec.get("body", ""))
        notes = str(slide_spec.get("notes", ""))
        notes_frame = slide.notes_slide.notes_text_frame
        notes_frame.text = notes
    if len(presentation.slides) > len(spec.get("slides", [])):
        # Default template normally starts empty; kept for unusual templates.
        pass
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    presentation.save(output)
    return output
