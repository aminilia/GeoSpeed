# ADR-003: C++ Road Matching Engine

## Status

Accepted

## Decision

Implement deterministic sign-to-road matching in C++17 with a CLI demo and tests.

## Rationale

Road matching is geometry-heavy and performance-sensitive. A standalone library keeps the logic testable and reusable.

