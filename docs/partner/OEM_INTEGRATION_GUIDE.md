# OEM Integration Guide

## Overview

GeoSpeed Auto FDE is an open simulator and partner-integration framework for speed-limit intelligence. It does not use proprietary Google, OEM, or paid SDKs.

## Integration Architecture

Partner apps consume speed-limit and launch-readiness contracts from the Java partner service, vehicle replay signals from the Python vehicle service, and mock route data from scenario JSON files.

## API Contract

- `GET /api/v1/partner/scenarios`
- `GET /api/v1/partner/issues`
- `POST /api/v1/partner/issues`
- `PATCH /api/v1/partner/issues/{id}/triage`
- `GET /api/v1/partner/launch-readiness`
- `POST /api/v1/partner/feature-requests`

## Speed-Limit Data Contract

Every displayed speed limit should include speed unit, confidence score, evidence sources, issue flags, and stale-data status.

## Confidence Metadata

Partners should suppress ADAS or legal-display behaviors when confidence is low or issue flags indicate missing or stale data.

## Error Handling

Return actionable partner-facing errors with affected component, owner team, and recommended action.

## Launch-Readiness Checklist

- Route coverage is acceptable.
- Speed-limit quality score is above threshold.
- No launch blockers remain.
- Infotainment and ADAS validation are complete.

