from __future__ import annotations

from dataclasses import dataclass

from app.schemas import SpeedLimitInferenceRequest, SpeedLimitInferenceResponse

COMMON_SPEED_LIMITS_MPH = (5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85)
ROAD_CLASS_PRIORS_MPH = {
    "motorway": 65,
    "primary": 45,
    "secondary": 35,
    "residential": 25,
    "service": 15,
    "unknown": 30,
}


@dataclass(frozen=True)
class EvidenceVote:
    source: str
    speed_mph: int
    weight: float


class BaselineSpeedLimitModel:
    """Deterministic baseline that blends map tags, sign evidence, traces, and road priors."""

    def infer(self, request: SpeedLimitInferenceRequest) -> SpeedLimitInferenceResponse:
        votes = self._build_votes(request)
        total_weight = sum(vote.weight for vote in votes)
        if total_weight <= 0.0:
            inferred_speed = ROAD_CLASS_PRIORS_MPH["unknown"]
            confidence = 0.0
        else:
            weighted_speed = sum(vote.speed_mph * vote.weight for vote in votes) / total_weight
            inferred_speed = nearest_common_speed(weighted_speed)
            confidence = self._confidence_for_speed(inferred_speed, votes, total_weight)

        issue_flags = self._issue_flags(request, votes, inferred_speed)
        if issue_flags:
            confidence *= max(0.55, 1.0 - len(issue_flags) * 0.08)

        return SpeedLimitInferenceResponse(
            inferred_speed_limit=inferred_speed,
            confidence_score=round(clamp(confidence), 3),
            evidence_sources=[vote.source for vote in votes if vote.weight > 0.0],
            issue_flags=issue_flags,
        )

    def _build_votes(self, request: SpeedLimitInferenceRequest) -> list[EvidenceVote]:
        votes: list[EvidenceVote] = []

        if request.known_speed_tag_mph is not None:
            tag_weight = 0.45 + 0.25 * request.sign_to_road_match_confidence
            votes.append(EvidenceVote("known_speed_tag", request.known_speed_tag_mph, tag_weight))

        sign_weight = 0.35 * request.sign_detection_confidence * request.sign_to_road_match_confidence
        if request.known_speed_tag_mph is not None and sign_weight > 0.0:
            votes.append(EvidenceVote("sign_detection", request.known_speed_tag_mph, sign_weight))

        trace = request.trace_speed_stats
        if trace.sample_count > 0:
            trace_speed = nearest_common_speed(trace.p85_mph)
            sample_weight = min(trace.sample_count / 40.0, 1.0)
            variance_penalty = max(0.25, 1.0 - trace.stddev_mph / 30.0)
            votes.append(EvidenceVote("trace_speed_statistics", trace_speed, 0.3 * sample_weight * variance_penalty))

        prior_speed = ROAD_CLASS_PRIORS_MPH[request.road_class]
        votes.append(EvidenceVote("road_class_prior", prior_speed, 0.2))
        return votes

    def _confidence_for_speed(self, speed_mph: int, votes: list[EvidenceVote], total_weight: float) -> float:
        aligned_weight = sum(vote.weight for vote in votes if abs(vote.speed_mph - speed_mph) <= 5)
        spread_penalty = self._speed_spread(votes) / 80.0
        return clamp((aligned_weight / total_weight) * (1.0 - min(spread_penalty, 0.45)))

    def _issue_flags(
        self,
        request: SpeedLimitInferenceRequest,
        votes: list[EvidenceVote],
        inferred_speed: int,
    ) -> list[str]:
        flags: list[str] = []
        trace = request.trace_speed_stats

        if request.known_speed_tag_mph is None:
            flags.append("missing_known_speed_tag")
        if request.sign_detection_confidence < 0.6:
            flags.append("low_sign_detection_confidence")
        if request.sign_to_road_match_confidence < 0.6:
            flags.append("low_sign_to_road_match_confidence")
        if trace.sample_count < 10:
            flags.append("low_trace_sample_count")
        if trace.stddev_mph > 18.0:
            flags.append("high_trace_speed_variance")
        if abs(trace.p85_mph - inferred_speed) > 15.0 and trace.sample_count >= 10:
            flags.append("trace_speed_outlier")
        if self._speed_spread(votes) > 20:
            flags.append("conflicting_evidence")

        return flags

    def _speed_spread(self, votes: list[EvidenceVote]) -> int:
        speeds = [vote.speed_mph for vote in votes if vote.weight > 0.0]
        if not speeds:
            return 0
        return max(speeds) - min(speeds)


def nearest_common_speed(speed_mph: float) -> int:
    return min(COMMON_SPEED_LIMITS_MPH, key=lambda candidate: abs(candidate - speed_mph))


def clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, value))

