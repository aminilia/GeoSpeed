from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PIPELINES_ROOT = Path(__file__).resolve().parents[1]
if str(PIPELINES_ROOT) not in sys.path:
    sys.path.insert(0, str(PIPELINES_ROOT))

from geospeed_pipeline.io import load_road_segments


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize a small OSM-compatible road sample.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    segments = load_road_segments(args.input)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps([segment.__dict__ for segment in segments], indent=2),
        encoding="utf-8",
    )
    print(f"normalized {len(segments)} road segments")


if __name__ == "__main__":
    main()
