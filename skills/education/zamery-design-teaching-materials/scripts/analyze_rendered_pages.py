from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image


def analyze_page(path: Path) -> dict[str, object]:
    image = Image.open(path).convert("RGB")
    pixels = image.get_flattened_data()
    occupied = sum(1 for red, green, blue in pixels if min(red, green, blue) < 245)
    ratio = occupied / (image.width * image.height)
    return {
        "path": str(path),
        "width": image.width,
        "height": image.height,
        "occupied_ratio": round(ratio, 4),
        "sparse": ratio < 0.25,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("images", nargs="+", type=Path)
    args = parser.parse_args()
    reports = [analyze_page(path) for path in args.images]
    print(json.dumps(reports, indent=2))
    return 1 if any(report["sparse"] for report in reports) else 0


if __name__ == "__main__":
    raise SystemExit(main())
