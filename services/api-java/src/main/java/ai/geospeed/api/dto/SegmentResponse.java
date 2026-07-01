package ai.geospeed.api.dto;

import java.util.List;

public record SegmentResponse(
    String id,
    String roadName,
    String speedLimit,
    double matchConfidence,
    List<CoordinateDto> polyline
) {
}

