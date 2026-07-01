from __future__ import annotations

from fastapi import FastAPI

from app.model import BaselineSpeedLimitModel
from app.schemas import (
    EvaluationRequest,
    EvaluationResponse,
    QualityScoreRequest,
    QualityScoreResponse,
    SpeedLimitInferenceRequest,
    SpeedLimitInferenceResponse,
)

app = FastAPI(title="GeoSpeed ML Service", version="0.2.0")
model = BaselineSpeedLimitModel()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "ml-python", "model": "baseline-speed-limit-v1"}


@app.post("/infer/speed-limit")
def infer_speed_limit(request: SpeedLimitInferenceRequest) -> SpeedLimitInferenceResponse:
    return model.infer(request)


@app.post("/evaluate")
def evaluate(request: EvaluationRequest) -> EvaluationResponse:
    predictions = [model.infer(record.features).inferred_speed_limit for record in request.records]
    truths = [record.ground_truth_speed_limit_mph for record in request.records]
    exact_matches = sum(1 for prediction, truth in zip(predictions, truths, strict=True) if prediction == truth)
    absolute_errors = [abs(prediction - truth) for prediction, truth in zip(predictions, truths, strict=True)]

    return EvaluationResponse(
        record_count=len(request.records),
        exact_match_accuracy=round(exact_matches / len(request.records), 3),
        mean_absolute_error_mph=round(sum(absolute_errors) / len(absolute_errors), 3),
    )


@app.post("/quality-score")
def quality_score(request: QualityScoreRequest) -> QualityScoreResponse:
    inference = model.infer(request.inference)
    issue_penalty = min(len(inference.issue_flags) * 0.06, 0.35)
    score = max(0.0, inference.confidence_score - issue_penalty)
    return QualityScoreResponse(
        quality_score=round(score, 3),
        inferred_speed_limit=inference.inferred_speed_limit,
        issue_flags=inference.issue_flags,
        evidence_sources=inference.evidence_sources,
    )

