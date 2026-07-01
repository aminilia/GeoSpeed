#include "geospeed/matcher.hpp"

#include <gtest/gtest.h>

#include <stdexcept>
#include <vector>

namespace {

TEST(MatcherTest, MatchesNearestAlignedSegment) {
    const geospeed::Observation observation{-74.0060, 40.7128, 45.0, 0.9};
    const std::vector<geospeed::RoadSegment> segments{
        {"road-a", {{-74.0063, 40.7125}, {-74.0057, 40.7131}}},
        {"road-b", {{-74.0100, 40.7200}, {-74.0110, 40.7210}}},
    };

    const auto match = geospeed::matchObservationToRoadSegments(observation, segments);

    EXPECT_EQ(match.segment_id, "road-a");
    EXPECT_LT(match.distance_m, 5.0);
    EXPECT_LT(match.heading_delta_deg, 10.0);
    EXPECT_GT(match.match_confidence, 0.75);
}

TEST(MatcherTest, HeadingDeltaWrapsAcrossNorth) {
    EXPECT_DOUBLE_EQ(geospeed::headingDeltaDegrees(350.0, 10.0), 20.0);
    EXPECT_DOUBLE_EQ(geospeed::headingDeltaDegrees(-10.0, 10.0), 20.0);
}

TEST(MatcherTest, RejectsEmptySegments) {
    const geospeed::Observation observation{-74.0060, 40.7128, 45.0, 0.9};

    EXPECT_THROW(
        geospeed::matchObservationToRoadSegments(observation, {}),
        std::invalid_argument);
}

}  // namespace
