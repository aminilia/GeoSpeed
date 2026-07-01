from __future__ import annotations

import csv
from pathlib import Path

REQUIRED_COLUMNS = {"sign_id", "latitude", "longitude", "sign_type", "observed_at"}


def validate_synthetic_signs(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not REQUIRED_COLUMNS.issubset(reader.fieldnames):
            missing = REQUIRED_COLUMNS.difference(reader.fieldnames or [])
            raise ValueError(f"missing columns: {sorted(missing)}")

        count = 0
        for row in reader:
            latitude = float(row["latitude"])
            longitude = float(row["longitude"])
            if not -90 <= latitude <= 90:
                raise ValueError(f"invalid latitude for {row['sign_id']}")
            if not -180 <= longitude <= 180:
                raise ValueError(f"invalid longitude for {row['sign_id']}")
            count += 1

    return count


if __name__ == "__main__":
    sample_path = Path(__file__).resolve().parents[2] / "sample-data" / "synthetic_sign_observations.csv"
    print(f"validated {validate_synthetic_signs(sample_path)} synthetic records")

