from __future__ import annotations

from pydantic import BaseModel, Field


class VehicleSignalSnapshot(BaseModel):
    timestamp: str
    latitude: float
    longitude: float
    heading: float = Field(ge=0.0, le=360.0)
    vehicle_speed: float = Field(ge=0.0)
    cruise_control_speed_set: float | None = Field(default=None, ge=0.0)
    cruise_control_active: bool = False
    speed_limit_assist_active: bool = True
    active_route_id: str
    current_gear: str = "D"
    matched_road_segment: str
    speed_limit: int | None = None
    speed_unit: str = "mph"
    alert_status: str = "normal"
    adas_mismatch_flag: bool = False


class ScenarioRequest(BaseModel):
    scenario_id: str = "oem_speed_alert_demo"


class ReplayRequest(BaseModel):
    route_id: str = "route-dc-demo-001"
    steps: int = Field(default=5, ge=1, le=100)
    start_speed: float = Field(default=22.0, ge=0.0)


class ReplayResponse(BaseModel):
    route_id: str
    replay: list[VehicleSignalSnapshot]


class AdasStatusResponse(BaseModel):
    cruise_control_active: bool
    speed_limit_assist_active: bool
    cruise_control_speed_set: float | None
    current_speed_limit: int | None
    adas_mismatch_flag: bool
    status: str

