import type { VehicleFrame } from "../api/mockData";

export function SpeedLimitAlert({ frame }: { frame: VehicleFrame }) {
  const overLimit = frame.speedLimit !== null && frame.vehicleSpeed > frame.speedLimit;
  return (
    <section className={overLimit || frame.staleMapData || frame.adasMismatch ? "alert-panel warning" : "alert-panel"}>
      <h2>{overLimit ? "Speed Limit Alert" : "Speed Limit Normal"}</h2>
      <div className="alert-grid">
        <span>Confidence</span>
        <strong>{Math.round(frame.confidenceScore * 100)}%</strong>
        <span>Coverage</span>
        <strong>{Math.round(frame.routeCoverage * 100)}%</strong>
      </div>
      {frame.staleMapData && <p>Stale map-data warning: partner launch requires refreshed evidence.</p>}
      {frame.adasMismatch && <p>ADAS speed mismatch: cruise-control set speed exceeds posted limit.</p>}
    </section>
  );
}

