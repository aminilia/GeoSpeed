import type { VehicleFrame } from "../api/mockData";
import { replay } from "../api/mockData";

export function VehicleSignalsPanel({
  frame,
  frameIndex,
  setFrameIndex
}: {
  frame: VehicleFrame;
  frameIndex: number;
  setFrameIndex: (index: number) => void;
}) {
  return (
    <section className="panel">
      <h2>Vehicle Signals</h2>
      <label>
        Replay frame
        <input
          max={replay.length - 1}
          min={0}
          type="range"
          value={frameIndex}
          onChange={(event) => setFrameIndex(Number(event.target.value))}
        />
      </label>
      <dl>
        <dt>Vehicle.Speed</dt>
        <dd>{frame.vehicleSpeed} mph</dd>
        <dt>Vehicle.Heading</dt>
        <dd>45 deg</dd>
        <dt>ActiveRouteId</dt>
        <dd>route-demo</dd>
        <dt>Transmission.CurrentGear</dt>
        <dd>D</dd>
      </dl>
    </section>
  );
}

