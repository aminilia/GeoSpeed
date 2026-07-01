from __future__ import annotations

from datetime import date

from geospeed_pipeline.models import QualityIssue, RoadSegment, parse_date

HIGH_SEVERITY_TYPES = {"CONFLICTING_SOURCES", "GEOMETRY_MATCH_FAILURE"}


def apply_quality_policy(segment: RoadSegment, today: date | None = None) -> list[QualityIssue]:
    today = today or date.today()
    segment.freshness_score = freshness_score(segment.last_updated, today)
    issues = build_quality_issues(segment)
    has_high_issue = any(issue.severity in {"high", "critical"} for issue in issues)
    has_reliable_evidence = any(source != "road_class_prior" for source in segment.evidence_sources)
    segment.release_ready = (
        segment.confidence_score >= 0.80
        and not has_high_issue
        and segment.freshness_score >= 0.60
        and segment.conflict_score <= 0.30
        and has_reliable_evidence
    )
    return issues


def freshness_score(last_updated: str, today: date) -> float:
    parsed = parse_date(last_updated)
    if parsed is None:
        return 0.0
    age_days = (today - parsed).days
    if age_days <= 540:
        return 1.0
    if age_days >= 1095:
        return 0.25
    return round(1.0 - ((age_days - 540) / 555) * 0.75, 3)


def build_quality_issues(segment: RoadSegment) -> list[QualityIssue]:
    issues: list[QualityIssue] = []
    for flag in segment.issue_flags:
        severity = severity_for(flag)
        issues.append(
            QualityIssue(
                issue_id=f"{segment.segment_id}_{flag.lower()}",
                segment_id=segment.segment_id,
                issue_type=flag,
                severity=severity,
                description=description_for(flag),
                recommended_action=recommended_action_for(flag),
            )
        )
    if segment.freshness_score < 0.60:
        issues.append(
            QualityIssue(
                issue_id=f"{segment.segment_id}_stale_observation",
                segment_id=segment.segment_id,
                issue_type="STALE_OBSERVATION",
                severity="medium",
                description="Best available source data is stale or missing an update date.",
                recommended_action="Refresh authoritative or OSM source evidence before release.",
            )
        )
    return issues


def severity_for(issue_type: str) -> str:
    if issue_type in HIGH_SEVERITY_TYPES:
        return "high"
    if issue_type in {"LOW_CONFIDENCE_INFERENCE", "OBSERVED_SPEED_ANOMALY"}:
        return "medium"
    return "low"


def description_for(issue_type: str) -> str:
    return {
        "MISSING_SPEED_LIMIT": "No reliable legal speed-limit source is available.",
        "LOW_CONFIDENCE_INFERENCE": "Inference confidence is below release threshold.",
        "CONFLICTING_SOURCES": "Reliable sources disagree by more than policy allows.",
        "LOW_SIGN_MATCH_CONFIDENCE": "A sign observation has weak detection or road-match confidence.",
        "OBSERVED_SPEED_ANOMALY": "Observed p85 speed is much higher than the inferred legal limit.",
        "GEOMETRY_MATCH_FAILURE": "Sign or road geometry could not be matched reliably.",
    }.get(issue_type, "Quality policy raised an issue.")


def recommended_action_for(issue_type: str) -> str:
    return {
        "MISSING_SPEED_LIMIT": "Add authoritative data, OSM maxspeed, or validated sign evidence.",
        "LOW_CONFIDENCE_INFERENCE": "Review source evidence and add corroborating data.",
        "CONFLICTING_SOURCES": "Manually inspect source recency and jurisdiction rules.",
        "LOW_SIGN_MATCH_CONFIDENCE": "Re-run sign matching or inspect the image observation.",
        "OBSERVED_SPEED_ANOMALY": "Treat as validation signal and check for incorrect geometry or source value.",
        "GEOMETRY_MATCH_FAILURE": "Repair geometry or exclude segment from release.",
    }.get(issue_type, "Review the segment before release.")

