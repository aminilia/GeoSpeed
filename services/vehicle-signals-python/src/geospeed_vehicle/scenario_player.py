from __future__ import annotations

import json
from pathlib import Path

from geospeed_vehicle.schemas import VehicleSignalSnapshot


def scenario_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "simulations" / "partner_scenarios"
        if candidate.exists():
            return candidate
    raise FileNotFoundError("simulations/partner_scenarios directory not found")


def load_scenario_replay(scenario_id: str) -> list[VehicleSignalSnapshot]:
    path = scenario_root() / f"{scenario_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"scenario not found: {scenario_id}")
    data = json.loads(path.read_text(encoding="utf-8"))
    speed_limit_data = data.get("speed_limit_data", {})
    replay: list[VehicleSignalSnapshot] = []
    for raw in data.get("vehicle_signals", []):
        segment_id = data.get("road_segments", ["unknown"])[0]
        speed_record = speed_limit_data.get(segment_id, {})
        speed_limit = speed_record.get("speed_limit")
        cruise_set = raw.get("adas_cruise_speed_set")
        mismatch = bool(cruise_set and speed_limit and cruise_set > speed_limit)
        alert = "speed_limit_alert" if speed_limit and raw["vehicle_speed"] > speed_limit else "normal"
        replay.append(
            VehicleSignalSnapshot(
                timestamp=raw["timestamp"],
                latitude=raw["lat"],
                longitude=raw["lon"],
                heading=raw.get("heading", 0.0),
                vehicle_speed=raw["vehicle_speed"],
                cruise_control_speed_set=cruise_set,
                cruise_control_active=raw.get("adas_cruise_active", False),
                speed_limit_assist_active=raw.get("speed_limit_assist_active", True),
                active_route_id=data["route_id"],
                current_gear=raw.get("current_gear", "D"),
                matched_road_segment=segment_id,
                speed_limit=speed_limit,
                speed_unit=speed_record.get("speed_unit", "mph"),
                alert_status=alert,
                adas_mismatch_flag=mismatch,
            )
        )
    return replay
