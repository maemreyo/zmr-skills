from __future__ import annotations

import argparse
import re


def advise_route(request: str) -> str:
    """Return the primary V3 specialist intent for common boundary cases."""
    text = " ".join(request.casefold().split())
    if "ielts" in text:
        return "ielts_practice"
    if any(term in text for term in ("youtube", "video link", "transcript", "h5p", "timestamped")):
        return "video_learning"
    if any(term in text for term in ("exam", "graded test", "quiz", "exit ticket", "form a", "form b", "qti")):
        return "assessment_composition"
    counts = [int(value) for value in re.findall(r"\b(\d{2,4})\s*[- ]?(?:question|item|câu)", text)]
    if any(term in text for term in ("item bank", "question bank", "reusable bank", "semester pool", "resumable", "sqlite", "deduplicate")):
        return "item_bank"
    if counts and max(counts) >= 80:
        return "item_bank"
    if any(term in text for term in ("docx", "pdf", "print-ready", "branded", "layout")):
        return "material_design"
    if any(term in text for term in ("worksheet", "homework", "ungraded", "practice", "flashcard")):
        return "practice"
    return "design"


def main() -> int:
    parser = argparse.ArgumentParser(description="Advise the primary Zamery V3 route.")
    parser.add_argument("request")
    args = parser.parse_args()
    print(advise_route(args.request))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
