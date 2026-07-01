#include "geospeed/matcher.hpp"

#include <algorithm>
#include <cmath>
#include <limits>
#include <stdexcept>

namespace geospeed {
namespace {
constexpr double kEarthRadiusMeters = 6371000.0;
constexpr double kPi = 3.14159265358979323846;
constexpr double kMetersPerDegreeLat = 111320.0;

double radians(double degrees) {
    return degrees * kPi / 180.0;
}

double degrees(double radians_value) {
    return radians_value * 180.0 / kPi;
}

double normalizeHeading(double heading) {
    double normalized = std::fmod(heading, 360.0);
    if (normalized < 0.0) {
        normalized += 360.0;
    }
    return normalized;
}

double bearingDegrees(Coordinate from, Coordinate to) {
    const double lat1 = radians(from.lat);
    const double lat2 = radians(to.lat);
    const double dlon = radians(to.lon - from.lon);
    const double y = std::sin(dlon) * std::cos(lat2);
    const double x = std::cos(lat1) * std::sin(lat2) -
        std::sin(lat1) * std::cos(lat2) * std::cos(dlon);
    return normalizeHeading(degrees(std::atan2(y, x)));
}

struct NearestPoint {
    double distance_m;
    double heading_deg;
};

NearestPoint nearestPointOnEdge(Coordinate observation, Coordinate start, Coordinate end) {
    const double mean_lat = radians((observation.lat + start.lat + end.lat) / 3.0);
    const double meters_per_degree_lon = kMetersPerDegreeLat * std::cos(mean_lat);

    const double sx = (start.lon - observation.lon) * meters_per_degree_lon;
    const double sy = (start.lat - observation.lat) * kMetersPerDegreeLat;
    const double ex = (end.lon - observation.lon) * meters_per_degree_lon;
    const double ey = (end.lat - observation.lat) * kMetersPerDegreeLat;
    const double vx = ex - sx;
    const double vy = ey - sy;
    const double length_squared = vx * vx + vy * vy;

    double t = 0.0;
    if (length_squared > 0.0) {
        t = std::clamp(-(sx * vx + sy * vy) / length_squared, 0.0, 1.0);
    }

    const Coordinate projected{
        start.lon + (end.lon - start.lon) * t,
        start.lat + (end.lat - start.lat) * t,
    };

    return NearestPoint{
        haversineDistanceMeters(observation, projected),
        bearingDegrees(start, end),
    };
}

double scoreMatch(double observation_confidence, double distance_m, double heading_delta_deg) {
    const double distance_score = std::max(0.0, 1.0 - distance_m / 50.0);
    const double heading_score = std::max(0.0, 1.0 - heading_delta_deg / 90.0);
    const double confidence = std::clamp(observation_confidence, 0.0, 1.0);
    return std::clamp(confidence * (0.65 * distance_score + 0.35 * heading_score), 0.0, 1.0);
}
}  // namespace

double haversineDistanceMeters(Coordinate a, Coordinate b) {
    const double dlat = radians(b.lat - a.lat);
    const double dlon = radians(b.lon - a.lon);
    const double lat1 = radians(a.lat);
    const double lat2 = radians(b.lat);

    const double sin_dlat = std::sin(dlat / 2.0);
    const double sin_dlon = std::sin(dlon / 2.0);
    const double h = sin_dlat * sin_dlat + std::cos(lat1) * std::cos(lat2) * sin_dlon * sin_dlon;
    return 2.0 * kEarthRadiusMeters * std::asin(std::sqrt(h));
}

double headingDeltaDegrees(double observation_heading, double segment_heading) {
    const double lhs = normalizeHeading(observation_heading);
    const double rhs = normalizeHeading(segment_heading);
    const double raw_delta = std::fabs(lhs - rhs);
    return std::min(raw_delta, 360.0 - raw_delta);
}

MatchResult matchObservationToRoadSegments(
    const Observation& observation,
    const std::vector<RoadSegment>& segments) {
    if (segments.empty()) {
        throw std::invalid_argument("segments must not be empty");
    }

    const Coordinate observation_point{observation.lon, observation.lat};
    MatchResult best{"", std::numeric_limits<double>::max(), 180.0, 0.0};

    for (const auto& segment : segments) {
        if (segment.id.empty()) {
            throw std::invalid_argument("segment id must not be empty");
        }
        if (segment.polyline.empty()) {
            throw std::invalid_argument("segment polyline must not be empty");
        }

        NearestPoint nearest{haversineDistanceMeters(observation_point, segment.polyline.front()), 0.0};
        if (segment.polyline.size() == 1) {
            nearest.heading_deg = observation.heading;
        } else {
            for (std::size_t index = 1; index < segment.polyline.size(); ++index) {
                const auto candidate = nearestPointOnEdge(
                    observation_point,
                    segment.polyline[index - 1],
                    segment.polyline[index]);
                if (candidate.distance_m < nearest.distance_m) {
                    nearest = candidate;
                }
            }
        }

        const double heading_delta = headingDeltaDegrees(observation.heading, nearest.heading_deg);
        const double confidence = scoreMatch(observation.confidence, nearest.distance_m, heading_delta);

        if (confidence > best.match_confidence ||
            (confidence == best.match_confidence && nearest.distance_m < best.distance_m)) {
            best = MatchResult{segment.id, nearest.distance_m, heading_delta, confidence};
        }
    }

    return best;
}

}  // namespace geospeed
