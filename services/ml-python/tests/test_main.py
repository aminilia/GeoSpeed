from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def baseline_payload() -> dict[str, object]:
    return {
        "known_speed_tag_mph": 25,
        "sign_detection_confidence": 0.92,
        "sign_to_road_match_confidence": 0.88,
        "trace_speed_stats": {
            "mean_mph": 23.4,
            "p85_mph": 27.1,
            "stddev_mph": 4.2,
            "sample_count": 42,
        },
        "road_class": "residential",
    }


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["model"] == "baseline-speed-limit-v1"


def test_infer_speed_limit_uses_all_evidence_sources() -> None:
    response = client.post("/infer/speed-limit", json=baseline_payload())

    assert response.status_code == 200
    body = response.json()
    assert body["inferred_speed_limit"] == 25
    assert body["confidence_score"] > 0.75
    assert body["issue_flags"] == []
    assert set(body["evidence_sources"]) == {
        "known_speed_tag",
        "sign_detection",
        "trace_speed_statistics",
        "road_class_prior",
    }


def test_infer_speed_limit_flags_weak_inputs() -> None:
    payload = baseline_payload()
    payload["known_speed_tag_mph"] = None
    payload["sign_detection_confidence"] = 0.4
    payload["sign_to_road_match_confidence"] = 0.35
    payload["trace_speed_stats"] = {
        "mean_mph": 50.0,
        "p85_mph": 55.0,
        "stddev_mph": 20.0,
        "sample_count": 4,
    }

    response = client.post("/infer/speed-limit", json=payload)

    assert response.status_code == 200
    flags = set(response.json()["issue_flags"])
    assert "missing_known_speed_tag" in flags
    assert "low_sign_detection_confidence" in flags
    assert "low_sign_to_road_match_confidence" in flags
    assert "low_trace_sample_count" in flags


def test_evaluate_returns_accuracy_metrics() -> None:
    response = client.post(
        "/evaluate",
        json={
            "records": [
                {
                    "features": baseline_payload(),
                    "ground_truth_speed_limit_mph": 25,
                },
                {
                    "features": baseline_payload(),
                    "ground_truth_speed_limit_mph": 30,
                },
            ]
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["record_count"] == 2
    assert body["exact_match_accuracy"] == 0.5
    assert body["mean_absolute_error_mph"] == 2.5


def test_quality_score_returns_penalized_confidence() -> None:
    response = client.post("/quality-score", json={"inference": baseline_payload()})

    assert response.status_code == 200
    body = response.json()
    assert body["quality_score"] > 0.75
    assert body["inferred_speed_limit"] == 25

