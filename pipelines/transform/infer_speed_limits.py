from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

PIPELINES_ROOT = Path(__file__).resolve().parents[1]
if str(PIPELINES_ROOT) not in sys.path:
    sys.path.insert(0, str(PIPELINES_ROOT))

from geospeed_pipeline.pipeline import build_release_candidate


def main() -> None:
    parser = argparse.ArgumentParser(description="Infer speed limits and write a release-candidate GeoJSON.")
    parser.add_argument("--segments", type=Path, required=True)
    parser.add_argument("--speeds", type=Path, required=True)
    parser.add_argument("--signs", type=Path, required=True)
    parser.add_argument("--observed", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    segments, issues = build_release_candidate(
        args.segments,
        args.speeds,
        args.signs,
        args.observed,
        args.output,
        today=date(2026, 7, 1),
    )
    print(f"wrote {len(segments)} segments and raised {len(issues)} quality issues")


if __name__ == "__main__":
    main()
