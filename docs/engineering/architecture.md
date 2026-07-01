# Architecture

## System Overview

GeoSpeed AI Platform is a polyglot monorepo for speed-limit intelligence. Python pipelines build segment-level release candidates, the Java API exposes product contracts, the Python ML service provides inference and scoring, the C++ matcher handles road/sign geometry, and the React dashboard visualizes release readiness.

## Service Boundaries

- `pipelines`: batch ingestion, transformation, validation, and reports.
- `services/api-java`: product API and release-candidate contracts.
- `services/ml-python`: speed-limit inference and evaluation.
- `services/matcher-cpp`: deterministic sign-to-road matching.
- `apps/web-dashboard`: product dashboard.

## Data Flow

1. Ingest roads, speed limits, sign observations, and observed speeds.
2. Normalize to the segment-level data model.
3. Infer speed limits with source-ranked evidence.
4. Apply quality rules and issue flags.
5. Generate a release candidate and report.
6. Serve and visualize release status.

## API Design

APIs expose segment lists, quality summary, issues, speed-limit lookups, and release-candidate creation. DTOs keep transport contracts separate from internal model records.

## Storage Design

The demo uses file-backed sample GeoJSON and in-memory repositories. Production evolution should use object storage for raw extracts, analytical tables for normalized features, and a transactional store for release workflow state.

## C++ Matcher Role

The matcher provides heading-aware nearest-road matching for traffic sign observations. Keeping this logic in C++ demonstrates a path to high-throughput batch matching without coupling it to web APIs.

## Failure Modes

- Missing or stale source data.
- Conflicting legal speed-limit sources.
- Bad geometry or low-confidence road matching.
- Observed-speed anomalies that should not override legal sources.
- Partial pipeline outputs.

## Scaling Strategy

Batch ingestion can shard by geography. Matching can be parallelized by tile or jurisdiction. API services can remain stateless over a persistent release-candidate store.

