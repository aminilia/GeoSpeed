from __future__ import annotations

from geospeed_vehicle.scenario_player import load_scenario_replay
from geospeed_vehicle.signal_simulator import current_signal, generate_replay
from geospeed_vehicle.schemas import ReplayRequest


def test_current_signal_has_adas_mismatch() -> None:
    signal = current_signal()

    assert signal.matched_road_segment == "dc_road_001"
    assert signal.adas_mismatch_flag is True


def test_generate_replay_returns_requested_steps() -> None:
    replay = generate_replay(ReplayRequest(route_id="route-test", steps=3, start_speed=26))

    assert len(replay) == 3
    assert replay[0].active_route_id == "route-test"
    assert any(point.alert_status == "speed_limit_alert" for point in replay)


def test_load_partner_scenario_replay() -> None:
    replay = load_scenario_replay("adas_speed_mismatch")

    assert replay[0].active_route_id == "route-dc-demo-002"
    assert replay[0].adas_mismatch_flag is True
