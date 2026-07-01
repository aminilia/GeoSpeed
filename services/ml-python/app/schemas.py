from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


RoadClass = Literal["motorway", "primary", "secondary", "residential", "service", "unknown"]


class TraceSpeedStats(BaseModel):
    mean_mph: float = Field(ge=0.0, le=120.0)
    p85_mph: float = Field(ge=0.0, le=120.0)
    stddev_mph: float = Field(default=0.0, ge=0.0, le=80.0)
    sample_count: int = Field(default=0, ge=0)


class SpeedLimitInferenceRequest(BaseModel):
    known_speed_tag_mph: int | None = Field(default=None, ge=5, le=85)
    sign_detection_confidence: float = Field(ge=0.0, le=1.0)
    sign_to_road_match_confidence: float = Field(ge=0.0, le=1.0)
    trace_speed_stats: TraceSpeedStats
    road_class: RoadClass = "unknown"


class SpeedLimitInferenceResponse(BaseModel):
    inferred_speed_limit: int
    confidence_score: float = Field(ge=0.0, le=1.0)
    evidence_sources: list[str]
    issue_flags: list[str]


class EvaluationRecord(BaseModel):
    features: SpeedLimitInferenceRequest
    ground_truth_speed_limit_mph: int = Field(ge=5, le=85)


class EvaluationRequest(BaseModel):
    records: list[EvaluationRecord] = Field(min_length=1, max_length=500)


class EvaluationResponse(BaseModel):
    record_count: int
    exact_match_accuracy: float = Field(ge=0.0, le=1.0)
    mean_absolute_error_mph: float = Field(ge=0.0)


class QualityScoreRequest(BaseModel):
    inference: SpeedLimitInferenceRequest


class QualityScoreResponse(BaseModel):
    quality_score: float = Field(ge=0.0, le=1.0)
    inferred_speed_limit: int
    issue_flags: list[str]
    evidence_sources: list[str]

