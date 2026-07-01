from __future__ import annotations

from dataclasses import dataclass

from geospeed_pipeline.models import ObservedSpeed, RoadSegment, TrafficSignObservation

ROAD_CLASS_PRIORS = {
    "motorway": 65,
    "primary": 35,
    "secondary": 30,
    "residential": 25,
    "service": 15,
    "unknown": 30,
}


@dataclass(frozen=True)
class Evidence:
    source: str
    speed_limit: int
    weight: float
    reliable: bool = True


def infer_segment_speed_limit(
    segment: RoadSegment,
    authoritative_record: dict[str, object] | None,
    sign_observations: list[TrafficSignObservation],
    observed_speed: ObservedSpeed | None,
) -> RoadSegment:
    evidence: list[Evidence] = []

    if authoritative_record and authoritative_record.get("speed_limit") is not None:
        source = str(authoritative_record.get("source", "authoritative_open_data"))
        evidence.append(Evidence(source, int(authoritative_record["speed_limit"]), 1.0))

    if segment.known_speed_limit is not None:
        evidence.append(Evidence("osm_maxspeed", int(segment.known_speed_limit), 0.82))

    for sign in sign_observations:
        if sign.detected_speed_limit is None:
            continue
        quality = sign.detection_confidence * sign.road_match_confidence
        weight = 0.72 * quality
        evidence.append(Evidence(sign.source, int(sign.detected_speed_limit), weight, reliable=quality >= 0.55))

    prior = ROAD_CLASS_PRIORS.get(segment.road_class, ROAD_CLASS_PRIORS["unknown"])
    evidence.append(Evidence("road_class_prior", prior, 0.35, reliable=False))

    weighted_total = sum(item.speed_limit * item.weight for item in evidence)
    total_weight = sum(item.weight for item in evidence)
    if authoritative_record and authoritative_record.get("speed_limit") is not None:
        inferred = int(authoritative_record["speed_limit"])
    else:
        inferred = nearest_speed(weighted_total / total_weight) if total_weight else prior

    segment.inferred_speed_limit = inferred
    segment.confidence_score = confidence_score(inferred, evidence)
    segment.conflict_score = conflict_score(evidence)
    segment.evidence_sources = [item.source for item in evidence if item.weight > 0.0]
    segment.issue_flags = infer_issue_flags(segment, evidence, observed_speed)
    if authoritative_record and authoritative_record.get("speed_limit") is not None:
        segment.known_speed_limit = int(authoritative_record["speed_limit"])
    return segment


def nearest_speed(value: float) -> int:
    common = (5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85)
    return min(common, key=lambda speed: abs(speed - value))


def confidence_score(inferred: int, evidence: list[Evidence]) -> float:
    reliable = [item for item in evidence if item.reliable]
    if not reliable:
        return 0.35
    total = sum(item.weight for item in evidence)
    aligned = sum(item.weight for item in evidence if abs(item.speed_limit - inferred) <= 5)
    source_bonus = min(len({item.source for item in reliable}) * 0.05, 0.15)
    return round(min(1.0, aligned / total + source_bonus), 3)


def conflict_score(evidence: list[Evidence]) -> float:
    speeds = [item.speed_limit for item in evidence if item.reliable]
    if len(speeds) < 2:
        return 0.0
    spread = max(speeds) - min(speeds)
    return round(min(1.0, spread / 30.0), 3)


def infer_issue_flags(segment: RoadSegment, evidence: list[Evidence], observed_speed: ObservedSpeed | None) -> list[str]:
    flags: list[str] = []
    reliable = [item for item in evidence if item.reliable]
    if not reliable:
        flags.append("MISSING_SPEED_LIMIT")
    if segment.confidence_score < 0.80:
        flags.append("LOW_CONFIDENCE_INFERENCE")
    if segment.conflict_score > 0.30:
        flags.append("CONFLICTING_SOURCES")
    if any(item.source != "road_class_prior" and not item.reliable for item in evidence):
        flags.append("LOW_SIGN_MATCH_CONFIDENCE")
    if observed_speed and segment.inferred_speed_limit is not None:
        if observed_speed.percentile_85_speed - segment.inferred_speed_limit > 12:
            flags.append("OBSERVED_SPEED_ANOMALY")
    return flags
