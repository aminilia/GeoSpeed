# Code Review Guide

## Python

- Validate typed function signatures.
- Keep pipeline steps deterministic.
- Preserve observed-speed-as-validation-only semantics.
- Test quality rules and report generation.

## Java

- Keep controllers thin.
- Use DTOs at API boundaries.
- Cover service behavior separately from controller serialization.
- Document new endpoints in OpenAPI.

## C++

- Validate geometry edge cases.
- Keep numeric assumptions explicit.
- Add tests for heading wraparound and empty inputs.
- Avoid hidden global state.

## TypeScript

- Keep mock API data typed.
- Verify responsive layout.
- Avoid text overflow in dashboard cards.
- Keep map interactions accessible where possible.

## Geospatial Pipelines

- Track source and update date.
- Do not mix coordinate orders.
- Preserve geometry validity.
- Avoid huge checked-in extracts.

## ML / Inference Logic

- Explain every score with evidence sources.
- Do not infer legal limits directly from observed speeds.
- Flag conflict and freshness issues.
- Keep baselines reproducible.

## API Changes

- Version breaking changes.
- Update tests and docs.
- Include example payloads.

## Performance

- Avoid repeated full scans for large future datasets.
- Keep demo paths lightweight.
- Prefer spatial indexes when scaling matcher workloads.

## Security

- Do not commit secrets.
- Avoid proprietary data.
- Validate external file inputs.

