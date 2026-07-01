from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from geospeed_pipeline.inference import infer_segment_speed_limit
from geospeed_pipeline.io import (
    load_authoritative_speed_limits,
    load_observed_speeds,
    load_road_segments,
    load_sign_observations,
    segment_to_feature,
    write_geojson,
)
from geospeed_pipeline.models import QualityIssue, RoadSegment
from geospeed_pipeline.quality import apply_quality_policy


def build_release_candidate(
    segments_path: Path,
    speed_limits_path: Path,
    signs_path: Path,
    observed_speeds_path: Path,
    output_path: Path,
    today: date | None = None,
) -> tuple[list[RoadSegment], list[QualityIssue]]:
    segments = load_road_segments(segments_path)
    speed_limits = load_authoritative_speed_limits(speed_limits_path)
    signs = load_sign_observations(signs_path)
    observed_speeds = load_observed_speeds(observed_speeds_path)

    all_issues: list[QualityIssue] = []
    for segment in segments:
        segment_signs = [sign for sign in signs if sign.matched_segment_id == segment.segment_id]
        infer_segment_speed_limit(
            segment,
            speed_limits.get(segment.segment_id),
            segment_signs,
            observed_speeds.get(segment.segment_id),
        )
        all_issues.extend(apply_quality_policy(segment, today=today))

    write_geojson(
        output_path,
        {
            "type": "FeatureCollection",
            "features": [segment_to_feature(segment) for segment in segments],
            "metadata": {
                "issue_count": len(all_issues),
                "release_ready_count": sum(1 for segment in segments if segment.release_ready),
            },
        },
    )
    return segments, all_issues


def build_release_report(release_candidate_path: Path, output_path: Path) -> dict[str, Any]:
    import json

    with release_candidate_path.open(encoding="utf-8") as handle:
        data = json.load(handle)

    features = data.get("features", [])
    total = len(features)
    ready = sum(1 for feature in features if feature["properties"].get("release_ready"))
    avg_confidence = (
        sum(float(feature["properties"].get("confidence_score", 0.0)) for feature in features) / total
        if total
        else 0.0
    )
    blocked = [
        feature["properties"]["segment_id"]
        for feature in features
        if not feature["properties"].get("release_ready")
    ]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        "\n".join(
            [
                "# GeoSpeed Release Report",
                "",
                f"- Total segments: {total}",
                f"- Release-ready segments: {ready}",
                f"- Blocked segments: {len(blocked)}",
                f"- Average confidence: {avg_confidence:.3f}",
                "",
                "## Blocked Segments",
                "",
                *(f"- {segment_id}" for segment_id in blocked),
                "",
            ]
        ),
        encoding="utf-8",
    )
    return {
        "total_segments": total,
        "release_ready_segments": ready,
        "blocked_segments": blocked,
        "average_confidence": round(avg_confidence, 3),
    }

