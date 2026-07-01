# Automotive Architecture

## In-Vehicle App Simulator

The auto head-unit simulator renders navigation, speed-limit alerts, ADAS mismatch state, and partner debug information.

## Partner Integration Service

The Java service models partner scenarios, issues, feature requests, roadmap feedback, and launch readiness.

## Vehicle Signal Service

The Python service emits COVESA VSS-style synthetic vehicle signals and route replays.

## Geospatial Speed-Limit API

The existing GeoSpeed API remains the map-data product API for segment speed-limit quality.

## C++ Matcher

The matcher provides deterministic road/sign matching primitives for high-throughput integration workflows.

## Data Flow

Scenario JSON -> vehicle signal replay -> partner debug API -> head-unit simulator -> launch-readiness review.

