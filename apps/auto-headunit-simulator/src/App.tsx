import { useState } from "react";
import { replay } from "./api/mockData";
import { LaunchReadinessView } from "./screens/LaunchReadinessView";
import { NavigationView } from "./screens/NavigationView";
import { PartnerDebugPanel } from "./screens/PartnerDebugPanel";
import { SpeedLimitAlert } from "./screens/SpeedLimitAlert";
import { VehicleSignalsPanel } from "./screens/VehicleSignalsPanel";

export function App() {
  const [frameIndex, setFrameIndex] = useState(1);
  const frame = replay[frameIndex];

  return (
    <main className="headunit-shell">
      <section className="cluster">
        <header className="top-bar">
          <div>
            <span>GeoSpeed Auto FDE</span>
            <h1>Partner Head Unit Simulator</h1>
          </div>
          <div className="scenario-chip">{frame.scenarioId}</div>
        </header>
        <NavigationView frame={frame} />
        <SpeedLimitAlert frame={frame} />
      </section>
      <aside className="side-stack">
        <VehicleSignalsPanel frame={frame} frameIndex={frameIndex} setFrameIndex={setFrameIndex} />
        <PartnerDebugPanel frame={frame} />
        <LaunchReadinessView />
      </aside>
    </main>
  );
}

