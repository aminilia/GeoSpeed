package ai.geospeed.api.model;

import java.util.List;

public record RoadSegment(
    String id,
    String roadName,
    String speedLimit,
    double matchConfidence,
    List<Coordinate> polyline
) {
}

