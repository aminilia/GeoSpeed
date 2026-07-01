# Data Model

## RoadSegment

- `segment_id`
- `source`
- `road_name`
- `road_class`
- `geometry`
- `direction`
- `known_speed_limit`
- `inferred_speed_limit`
- `speed_unit`
- `confidence_score`
- `freshness_score`
- `conflict_score`
- `release_ready`
- `evidence_sources`
- `issue_flags`
- `last_updated`

## TrafficSignObservation

- `sign_id`
- `lon`
- `lat`
- `detected_speed_limit`
- `detection_confidence`
- `heading`
- `image_id`
- `capture_date`
- `source`

## ObservedSpeed

- `segment_id`
- `timestamp`
- `average_speed`
- `percentile_50_speed`
- `percentile_85_speed`
- `source`

## QualityIssue

- `issue_id`
- `segment_id`
- `issue_type`
- `severity`
- `description`
- `recommended_action`

