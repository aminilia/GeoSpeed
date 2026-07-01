#pragma once

#include <string>
#include <vector>

namespace geospeed {

// Coordinates use longitude, latitude order to match GeoJSON and most map APIs.
struct Coordinate {
    double lon;
    double lat;
};

struct RoadSegment {
    std::string id;
    std::vector<Coordinate> polyline;
};

struct Observation {
    double lon;
    double lat;
    double heading;
    double confidence;
};

struct MatchResult {
    std::string segment_id;
    double distance_m;
    double heading_delta_deg;
    double match_confidence;
};

// Great-circle distance between two coordinates.
double haversineDistanceMeters(Coordinate a, Coordinate b);

// Smallest absolute difference between two headings, normalized to 0..180.
double headingDeltaDegrees(double observation_heading, double segment_heading);

// Scores every segment by nearest polyline distance, heading alignment, and source confidence.
MatchResult matchObservationToRoadSegments(
    const Observation& observation,
    const std::vector<RoadSegment>& segments);

}  // namespace geospeed
