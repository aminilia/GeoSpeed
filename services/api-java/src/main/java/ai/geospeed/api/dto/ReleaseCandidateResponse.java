package ai.geospeed.api.dto;

import java.time.Instant;
import java.util.List;

public record ReleaseCandidateResponse(
    String id,
    String name,
    String status,
    List<String> segmentIds,
    Instant createdAt
) {
}

