from __future__ import annotations

from datetime import datetime, timedelta, timezone

from geospeed_vehicle.schemas import ReplayRequest, VehicleSignalSnapshot


def current_signal() -> VehicleSignalSnapshot:
    return VehicleSignalSnapshot(
        timestamp=datetime.now(timezone.utc).isoformat(),
        latitude=38.90735,
        longitude=-77.0365,
        heading=45.0,
        vehicle_speed=32.0,
        cruise_control_speed_set=35.0,
        cruise_control_active=True,
        speed_limit_assist_active=True,
        active_route_id="route-dc-demo-001",
        current_gear="D",
        matched_road_segment="dc_road_001",
        speed_limit=25,
        alert_status="speed_limit_alert",
        adas_mismatch_flag=True,
    )


def generate_replay(request: ReplayRequest) -> list[VehicleSignalSnapshot]:
    start = datetime(2026, 7, 1, 12, 0, tzinfo=timezone.utc)
    replay: list[VehicleSignalSnapshot] = []
    for index in range(request.steps):
        speed = request.start_speed + index * 2.5
        speed_limit = 25 if index < request.steps - 1 else 35
        cruise_set = 35.0
        mismatch = cruise_set > speed_limit
        replay.append(
            VehicleSignalSnapshot(
                timestamp=(start + timedelta(seconds=index * 5)).isoformat(),
                latitude=38.9071 + index * 0.00012,
                longitude=-77.0368 + index * 0.00014,
                heading=45.0,
                vehicle_speed=round(speed, 1),
                cruise_control_speed_set=cruise_set,
                cruise_control_active=True,
                speed_limit_assist_active=True,
                active_route_id=request.route_id,
                current_gear="D",
                matched_road_segment="dc_road_001" if index < request.steps - 1 else "dc_road_002",
                speed_limit=speed_limit,
                alert_status="speed_limit_alert" if speed > speed_limit else "normal",
                adas_mismatch_flag=mismatch,
            )
        )
    return replay

