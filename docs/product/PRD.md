# Product Requirements Document

## Problem Statement

Map teams need a trustworthy way to decide which speed-limit value should ship for each road segment. Evidence often conflicts across OSM tags, authoritative open data, sign observations, and observed traffic behavior.

## Users

- Map operations analysts
- Geospatial AI engineers
- Speed-limit data product managers
- Release managers for production map-data products

## Use Cases

- Inspect segment-level speed-limit evidence.
- Generate a release candidate from open-data samples.
- Identify quality issues that block release.
- Review confidence and freshness before publication.

## MVP Scope

- Small sample ingestion pipeline.
- Segment-level inference and quality scoring.
- Java API serving mock-compatible release data.
- React dashboard using MapLibre.
- C++ sign-to-road matcher demo.

## Requirements

- Use open-data-compatible sample formats.
- Avoid proprietary or paid datasets.
- Keep first-run demo small.
- Explain inference with evidence sources and issue flags.

## Non-Goals

- Production-scale storage.
- Real-time vehicle telemetry ingestion.
- Authenticated production deployment.
- Legal certification of speed-limit values.

## Success Metrics

- Release report generated from sample data.
- Clear release-ready decisions per segment.
- API and dashboard expose the same product concepts.
- New open-data connectors can be added without changing the core model.

## Launch Criteria

- Tests cover baseline inference, quality rules, and sample validation.
- README documents setup and demo commands.
- Dashboard screenshots can be captured from local mock data.
- Quality policy is documented and implemented.

## Risks

- Open datasets vary widely by jurisdiction.
- OSM `maxspeed` tags may be stale or incomplete.
- Observed speeds can reflect behavior, congestion, or enforcement, not legal limits.
- Sign observations need careful road matching to avoid false evidence.

