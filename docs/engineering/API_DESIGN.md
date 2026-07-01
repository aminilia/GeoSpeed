# API Design

## Java API

- `GET /api/v1/health`
- `GET /api/v1/segments`
- `GET /api/v1/segments/{segmentId}`
- `GET /api/v1/speed-limits?bbox=`
- `GET /api/v1/quality/summary`
- `GET /api/v1/issues`
- `POST /api/v1/release-candidate`

## Python ML API

- `GET /health`
- `POST /infer/speed-limit`
- `POST /quality-score`
- `POST /evaluate`

## Contract Principles

- Return evidence and issue flags with inferred values.
- Do not expose proprietary data assumptions.
- Keep DTO names aligned with the segment-level data model.

