from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def convert_csv(input_path: Path) -> list[dict[str, object]]:
    """Convert a tiny SUMO-like CSV into GeoSpeed vehicle signal replay records."""
    replay: list[dict[str, object]] = []
    with input_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            replay.append(
                {
                    "timestamp": row.get("timestamp"),
                    "lat": float(row.get("lat", 0.0)),
                    "lon": float(row.get("lon", 0.0)),
                    "heading": float(row.get("heading", 0.0)),
                    "vehicle_speed": float(row.get("speed", 0.0)),
                    "matched_road_segment": row.get("segment_id", "unknown"),
                    "speed_limit": int(row["speed_limit"]) if row.get("speed_limit") else None,
                    "alert_status": "normal",
                    "adas_mismatch_flag": False,
                }
            )
    return replay


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert SUMO-like CSV trajectories into vehicle signal replay JSON.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({"replay": convert_csv(args.input)}, indent=2), encoding="utf-8")
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()

