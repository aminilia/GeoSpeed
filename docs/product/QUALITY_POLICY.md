# Quality Policy

## Source Ranking

1. Authoritative city or state open speed-limit data.
2. OSM `maxspeed` tags.
3. High-confidence traffic sign observations with strong road matches.
4. Overture or road-class priors.
5. Observed speed data for validation only.
6. Synthetic traces for demo validation only.

## Confidence Thresholds

- `>= 0.90`: high confidence.
- `0.80 - 0.89`: release candidate with normal review.
- `0.60 - 0.79`: manual review.
- `< 0.60`: blocked unless overridden by policy.

## Freshness Rules

- Data updated within 18 months scores strongly.
- Data older than 36 months is stale.
- Missing dates are treated cautiously.

## Conflict Detection

Conflict score increases when authoritative data, OSM, signs, and road-class priors disagree by more than 5 mph. Observed speeds can raise anomaly flags but do not determine the legal speed limit.

## Manual Review Policy

Segments with high-severity issues or conflicting evidence should enter manual QA. Reviewers should inspect source records, sign observations, geometry, and local policy context.

## Release-Readiness Rules

A segment is release-ready only if:

- `confidence_score >= 0.80`
- no unresolved high-severity issue
- `freshness_score >= 0.60`
- `conflict_score <= 0.30`
- at least one reliable evidence source exists

