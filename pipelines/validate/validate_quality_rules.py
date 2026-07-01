from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PIPELINES_ROOT = Path(__file__).resolve().parents[1]
if str(PIPELINES_ROOT) not in sys.path:
    sys.path.insert(0, str(PIPELINES_ROOT))


def validate_quality_rules(path: Path) -> int:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    violations = 0
    for feature in data["features"]:
        props = feature["properties"]
        expected = (
            props["confidence_score"] >= 0.80
            and props["freshness_score"] >= 0.60
            and props["conflict_score"] <= 0.30
            and len(props["evidence_sources"]) > 0
            and "CONFLICTING_SOURCES" not in props["issue_flags"]
        )
        if props["release_ready"] != expected:
            violations += 1
    if violations:
        raise ValueError(f"{violations} release-ready policy violations found")
    return len(data["features"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate release-readiness policy fields.")
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    print(f"validated quality rules for {validate_quality_rules(args.input)} segments")


if __name__ == "__main__":
    main()
