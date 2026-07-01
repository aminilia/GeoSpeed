from __future__ import annotations

import argparse
import sys
from pathlib import Path

PIPELINES_ROOT = Path(__file__).resolve().parents[1]
if str(PIPELINES_ROOT) not in sys.path:
    sys.path.insert(0, str(PIPELINES_ROOT))

from geospeed_pipeline.io import load_sign_observations


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate traffic-sign observation GeoJSON sample.")
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    observations = load_sign_observations(args.input)
    print(f"loaded {len(observations)} sign observations")


if __name__ == "__main__":
    main()
