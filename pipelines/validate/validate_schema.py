from __future__ import annotations

import argparse
import sys
from pathlib import Path

PIPELINES_ROOT = Path(__file__).resolve().parents[1]
if str(PIPELINES_ROOT) not in sys.path:
    sys.path.insert(0, str(PIPELINES_ROOT))

from geospeed_pipeline.io import read_geojson


def validate_release_candidate_schema(path: Path) -> int:
    data = read_geojson(path)
    required = {
        "segment_id",
        "source",
        "road_name",
        "road_class",
        "known_speed_limit",
        "inferred_speed_limit",
        "confidence_score",
        "freshness_score",
        "conflict_score",
        "release_ready",
        "evidence_sources",
        "issue_flags",
    }
    for feature in data["features"]:
        missing = required.difference(feature.get("properties", {}))
        if missing:
            raise ValueError(f"missing properties for feature: {sorted(missing)}")
    return len(data["features"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate release-candidate GeoJSON schema.")
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    print(f"validated {validate_release_candidate_schema(args.input)} release-candidate segments")


if __name__ == "__main__":
    main()
