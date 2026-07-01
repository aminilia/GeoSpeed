import { launchChecks } from "../api/mockData";

export function LaunchReadinessView() {
  return (
    <section className="panel">
      <h2>Launch Readiness</h2>
      <div className="checks">
        {launchChecks.map((check) => (
          <div className={`check ${check.status}`} key={check.label}>
            <span>{check.label}</span>
            <strong>{check.value}</strong>
          </div>
        ))}
      </div>
    </section>
  );
}

