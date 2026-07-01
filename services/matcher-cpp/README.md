# matcher-cpp

C++17 sign-to-road matcher library and CLI demo.

## API

- `RoadSegment` contains an `id` and a polyline of `{lon, lat}` coordinates.
- `Observation` contains `lon`, `lat`, `heading`, and source `confidence`.
- `MatchResult` returns `segment_id`, `distance_m`, `heading_delta_deg`, and `match_confidence`.
- `matchObservationToRoadSegments(observation, segments)` chooses the best segment using distance and heading alignment.

## Build and Test

```bash
cmake -S services/matcher-cpp -B services/matcher-cpp/build
cmake --build services/matcher-cpp/build
ctest --test-dir services/matcher-cpp/build --output-on-failure
```

The test target uses GoogleTest via CMake FetchContent.

## CLI Demo

```bash
services/matcher-cpp/build/matcher_demo sample-data/synthetic_match_request.json
```

The demo reads the synthetic JSON fixture and writes the selected match as JSON.
