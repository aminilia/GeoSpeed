package ai.geospeed.api.model;

public record Issue(
    String id,
    String segmentId,
    String severity,
    String category,
    String description
) {
}

