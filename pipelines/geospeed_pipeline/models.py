from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any


Geometry = dict[str, Any]


@dataclass(frozen=True)
class TrafficSignObservation:
    sign_id: str
    lon: float
    lat: float
    detected_speed_limit: int | None
    detection_confidence: float
    heading: float
    image_id: str
    capture_date: str
    source: str
    matched_segment_id: str | None = None
    road_match_confidence: float = 0.0


@dataclass(frozen=True)
class ObservedSpeed:
    segment_id: str
    timestamp: str
    average_speed: float
    percentile_50_speed: float
    percentile_85_speed: float
    source: str


@dataclass(frozen=True)
class QualityIssue:
    issue_id: str
    segment_id: str
    issue_type: str
    severity: str
    description: str
    recommended_action: str


@dataclass
class RoadSegment:
    segment_id: str
    source: str
    road_name: str
    road_class: str
    geometry: Geometry
    direction: str
    known_speed_limit: int | None = None
    inferred_speed_limit: int | None = None
    speed_unit: str = "mph"
    confidence_score: float = 0.0
    freshness_score: float = 0.0
    conflict_score: float = 0.0
    release_ready: bool = False
    evidence_sources: list[str] = field(default_factory=list)
    issue_flags: list[str] = field(default_factory=list)
    last_updated: str = ""


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value[:10])
    except ValueError:
        return None

