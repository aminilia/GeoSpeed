from __future__ import annotations

import argparse
import sys
from pathlib import Path

PIPELINES_ROOT = Path(__file__).resolve().parents[1]
if str(PIPELINES_ROOT) not in sys.path:
    sys.path.insert(0, str(PIPELINES_ROOT))

from geospeed_pipeline.pipeline import build_release_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a Markdown release report.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    summary = build_release_report(args.input, args.output)
    print(f"wrote report for {summary['total_segments']} segments")


if __name__ == "__main__":
    main()
