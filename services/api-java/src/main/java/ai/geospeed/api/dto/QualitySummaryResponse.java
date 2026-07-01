package ai.geospeed.api.dto;

public record QualitySummaryResponse(
    int segmentCount,
    int openIssueCount,
    double averageMatchConfidence,
    double releaseReadinessScore
) {
}

