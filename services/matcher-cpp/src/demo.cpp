#include "geospeed/matcher.hpp"

#include <fstream>
#include <iomanip>
#include <iostream>
#include <regex>
#include <sstream>
#include <stdexcept>
#include <string>

namespace {

std::string readFile(const std::string& path) {
    std::ifstream input(path);
    if (!input) {
        throw std::runtime_error("unable to open input JSON: " + path);
    }

    std::ostringstream buffer;
    buffer << input.rdbuf();
    return buffer.str();
}

double extractNumber(const std::string& json, const std::string& key) {
    const std::regex pattern("\"" + key + "\"\\s*:\\s*(-?\\d+(?:\\.\\d+)?)");
    std::smatch match;
    if (!std::regex_search(json, match, pattern)) {
        throw std::runtime_error("missing numeric key: " + key);
    }
    return std::stod(match[1].str());
}

geospeed::Observation parseObservation(const std::string& json) {
    return geospeed::Observation{
        extractNumber(json, "lon"),
        extractNumber(json, "lat"),
        extractNumber(json, "heading"),
        extractNumber(json, "confidence"),
    };
}

std::vector<geospeed::RoadSegment> parseSegments(const std::string& json) {
    const std::regex segment_pattern(
        R"json(\{\s*"id"\s*:\s*"([^"]+)"\s*,\s*"polyline"\s*:\s*\[([\s\S]*?)\]\s*\})json",
        std::regex::optimize);
    const std::regex coordinate_pattern(
        R"json(\{\s*"lon"\s*:\s*(-?\d+(?:\.\d+)?)\s*,\s*"lat"\s*:\s*(-?\d+(?:\.\d+)?)\s*\})json",
        std::regex::optimize);

    std::vector<geospeed::RoadSegment> segments;
    for (std::sregex_iterator segment_it(json.begin(), json.end(), segment_pattern), end_it;
         segment_it != end_it;
         ++segment_it) {
        geospeed::RoadSegment segment;
        segment.id = (*segment_it)[1].str();
        const std::string polyline_json = (*segment_it)[2].str();

        for (std::sregex_iterator coordinate_it(polyline_json.begin(), polyline_json.end(), coordinate_pattern);
             coordinate_it != end_it;
             ++coordinate_it) {
            segment.polyline.push_back(geospeed::Coordinate{
                std::stod((*coordinate_it)[1].str()),
                std::stod((*coordinate_it)[2].str()),
            });
        }

        segments.push_back(segment);
    }

    if (segments.empty()) {
        throw std::runtime_error("input JSON must include at least one road segment");
    }
    return segments;
}

}  // namespace

int main(int argc, char** argv) {
    const std::string path = argc > 1 ? argv[1] : "sample-data/synthetic_match_request.json";

    try {
        const std::string json = readFile(path);
        const auto observation = parseObservation(json);
        const auto segments = parseSegments(json);
        const auto match = geospeed::matchObservationToRoadSegments(observation, segments);

        std::cout << std::fixed << std::setprecision(3)
                  << "{\n"
                  << "  \"segment_id\": \"" << match.segment_id << "\",\n"
                  << "  \"distance_m\": " << match.distance_m << ",\n"
                  << "  \"heading_delta_deg\": " << match.heading_delta_deg << ",\n"
                  << "  \"match_confidence\": " << match.match_confidence << "\n"
                  << "}\n";
    } catch (const std::exception& error) {
        std::cerr << "matcher_demo: " << error.what() << '\n';
        return 1;
    }

    return 0;
}
