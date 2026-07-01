import type { VehicleFrame } from "../api/mockData";

export function PartnerDebugPanel({ frame }: { frame: VehicleFrame }) {
  return (
    <section className="panel debug-panel">
      <h2>Partner Debug</h2>
      <dl>
        <dt>Partner</dt>
        <dd>{frame.partnerId}</dd>
        <dt>Scenario</dt>
        <dd>{frame.scenarioId}</dd>
        <dt>Evidence</dt>
        <dd>{frame.evidenceSources.join(", ")}</dd>
        <dt>Issue Flags</dt>
        <dd>{frame.issueFlags.length ? frame.issueFlags.join(", ") : "none"}</dd>
      </dl>
    </section>
  );
}

