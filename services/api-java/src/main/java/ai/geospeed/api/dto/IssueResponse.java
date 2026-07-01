package ai.geospeed.api.dto;

public record IssueResponse(
    String id,
    String segmentId,
    String severity,
    String category,
    String description
) {
}

