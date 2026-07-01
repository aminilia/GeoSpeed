from __future__ import annotations

from datetime import date
from pathlib import Path

from geospeed_pipeline.inference import infer_segment_speed_limit
from geospeed_pipeline.io import load_observed_speeds, load_road_segments, load_sign_observations, read_geojson
from geospeed_pipeline.pipeline import build_release_candidate, build_release_report
from geospeed_pipeline.quality import apply_quality_policy
from validate.validate_quality_rules import validate_quality_rules
from validate.validate_schema import validate_release_candidate_schema


ROOT = Path(__file__).resolve().parents[2]
SAMPLE = ROOT / "data" / "sample"


def test_inference_prioritizes_authoritative_open_data() -> None:
    segment = load_road_segments(SAMPLE / "roads.geojson")[0]
    signs = load_sign_observations(SAMPLE / "signs.geojson")
    observed = load_observed_speeds(SAMPLE / "observed_speeds.csv")

    infer_segment_speed_limit(
        segment,
        {"source": "dc_open_data_sample", "speed_limit": 25},
        [sign for sign in signs if sign.matched_segment_id == segment.segment_id],
        observed[segment.segment_id],
    )
    issues = apply_quality_policy(segment, today=date(2026, 7, 1))

    assert segment.inferred_speed_limit == 25
    assert segment.confidence_score >= 0.9
    assert segment.release_ready is True
    assert issues == []


def test_build_release_candidate_and_report(tmp_path: Path) -> None:
    output = tmp_path / "release_candidate.geojson"
    report = tmp_path / "release_report.md"

    segments, issues = build_release_candidate(
        SAMPLE / "roads.geojson",
        SAMPLE / "speed_limits.geojson",
        SAMPLE / "signs.geojson",
        SAMPLE / "observed_speeds.csv",
        output,
        today=date(2026, 7, 1),
    )
    summary = build_release_report(output, report)

    assert len(segments) == 3
    assert output.exists()
    assert report.exists()
    assert summary["total_segments"] == 3
    assert any(issue.issue_type == "OBSERVED_SPEED_ANOMALY" for issue in issues)
    assert validate_release_candidate_schema(output) == 3
    assert validate_quality_rules(output) == 3
    data = read_geojson(output)
    assert data["metadata"]["issue_count"] == len(issues)

