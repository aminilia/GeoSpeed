from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from geospeed_pipeline.models import ObservedSpeed, RoadSegment, TrafficSignObservation


def read_geojson(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if data.get("type") != "FeatureCollection":
        raise ValueError(f"{path} must be a GeoJSON FeatureCollection")
    return data


def write_geojson(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")


def load_road_segments(path: Path) -> list[RoadSegment]:
    data = read_geojson(path)
    segments: list[RoadSegment] = []
    for feature in data["features"]:
        props = feature.get("properties", {})
        segments.append(
            RoadSegment(
                segment_id=props["segment_id"],
                source=props.get("source", "unknown"),
                road_name=props.get("road_name", "Unnamed road"),
                road_class=props.get("road_class", "unknown"),
                geometry=feature["geometry"],
                direction=props.get("direction", "unknown"),
                known_speed_limit=props.get("osm_maxspeed"),
                last_updated=props.get("last_updated", ""),
                evidence_sources=["osm_maxspeed"] if props.get("osm_maxspeed") else [],
            )
        )
    return segments


def load_authoritative_speed_limits(path: Path) -> dict[str, dict[str, Any]]:
    data = read_geojson(path)
    records: dict[str, dict[str, Any]] = {}
    for feature in data["features"]:
        props = feature.get("properties", {})
        records[props["segment_id"]] = props
    return records


def load_sign_observations(path: Path) -> list[TrafficSignObservation]:
    data = read_geojson(path)
    observations: list[TrafficSignObservation] = []
    for feature in data["features"]:
        props = feature.get("properties", {})
        lon, lat = feature["geometry"]["coordinates"]
        observations.append(
            TrafficSignObservation(
                sign_id=props["sign_id"],
                lon=float(lon),
                lat=float(lat),
                detected_speed_limit=props.get("detected_speed_limit"),
                detection_confidence=float(props.get("detection_confidence", 0.0)),
                heading=float(props.get("heading", 0.0)),
                image_id=props.get("image_id", ""),
                capture_date=props.get("capture_date", ""),
                source=props.get("source", "unknown"),
                matched_segment_id=props.get("matched_segment_id"),
                road_match_confidence=float(props.get("road_match_confidence", 0.0)),
            )
        )
    return observations


def load_observed_speeds(path: Path) -> dict[str, ObservedSpeed]:
    records: dict[str, ObservedSpeed] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records[row["segment_id"]] = ObservedSpeed(
                segment_id=row["segment_id"],
                timestamp=row["timestamp"],
                average_speed=float(row["average_speed"]),
                percentile_50_speed=float(row["percentile_50_speed"]),
                percentile_85_speed=float(row["percentile_85_speed"]),
                source=row["source"],
            )
    return records


def segment_to_feature(segment: RoadSegment) -> dict[str, Any]:
    return {
        "type": "Feature",
        "properties": {
            "segment_id": segment.segment_id,
            "source": segment.source,
            "road_name": segment.road_name,
            "road_class": segment.road_class,
            "direction": segment.direction,
            "known_speed_limit": segment.known_speed_limit,
            "inferred_speed_limit": segment.inferred_speed_limit,
            "speed_unit": segment.speed_unit,
            "confidence_score": segment.confidence_score,
            "freshness_score": segment.freshness_score,
            "conflict_score": segment.conflict_score,
            "release_ready": segment.release_ready,
            "evidence_sources": segment.evidence_sources,
            "issue_flags": segment.issue_flags,
            "last_updated": segment.last_updated,
        },
        "geometry": segment.geometry,
    }

