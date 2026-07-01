from __future__ import annotations

from fastapi import FastAPI, HTTPException

from geospeed_vehicle.scenario_player import load_scenario_replay
from geospeed_vehicle.schemas import AdasStatusResponse, ReplayRequest, ReplayResponse, ScenarioRequest, VehicleSignalSnapshot
from geospeed_vehicle.signal_simulator import current_signal, generate_replay
from geospeed_vehicle.vss_schema import VSS_SIGNALS

app = FastAPI(title="GeoSpeed Vehicle Signals", version="0.1.0")


@app.get("/health")
def health() -> dict[str, object]:
    return {"status": "ok", "service": "vehicle-signals-python", "vss_signal_count": len(VSS_SIGNALS)}


@app.get("/signals/current")
def signals_current() -> VehicleSignalSnapshot:
    return current_signal()


@app.post("/signals/scenario")
def signals_scenario(request: ScenarioRequest) -> ReplayResponse:
    try:
        replay = load_scenario_replay(request.scenario_id)
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    route_id = replay[0].active_route_id if replay else request.scenario_id
    return ReplayResponse(route_id=route_id, replay=replay)


@app.post("/signals/replay")
def signals_replay(request: ReplayRequest) -> ReplayResponse:
    return ReplayResponse(route_id=request.route_id, replay=generate_replay(request))


@app.get("/signals/adas-status")
def signals_adas_status() -> AdasStatusResponse:
    signal = current_signal()
    status = "mismatch" if signal.adas_mismatch_flag else "nominal"
    return AdasStatusResponse(
        cruise_control_active=signal.cruise_control_active,
        speed_limit_assist_active=signal.speed_limit_assist_active,
        cruise_control_speed_set=signal.cruise_control_speed_set,
        current_speed_limit=signal.speed_limit,
        adas_mismatch_flag=signal.adas_mismatch_flag,
        status=status,
    )

