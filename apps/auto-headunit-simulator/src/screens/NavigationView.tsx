import type { VehicleFrame } from "../api/mockData";

export function NavigationView({ frame }: { frame: VehicleFrame }) {
  return (
    <section className="nav-view">
      <div className="route-line">
        <span />
        <i />
        <span />
      </div>
      <div className="road-card">
        <span>Current segment</span>
        <strong>{frame.roadName}</strong>
        <small>{frame.roadSegment}</small>
      </div>
      <div className="speed-cluster">
        <div>
          <span>Vehicle</span>
          <strong>{frame.vehicleSpeed}</strong>
          <small>{frame.speedUnit}</small>
        </div>
        <div className="posted-limit">
          <span>Limit</span>
          <strong>{frame.speedLimit ?? "--"}</strong>
          <small>{frame.speedUnit}</small>
        </div>
      </div>
    </section>
  );
}

