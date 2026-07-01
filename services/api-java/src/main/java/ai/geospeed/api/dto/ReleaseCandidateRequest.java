package ai.geospeed.api.dto;

import java.util.List;

public record ReleaseCandidateRequest(
    String name,
    List<String> segmentIds,
    String requestedBy
) {
}

