import { useEffect, useRef, useState } from "react";
import maplibregl, { type GeoJSONSourceSpecification, type LineLayerSpecification } from "maplibre-gl";
import type { Feature, LineString, Position } from "geojson";
import {
  confidenceColor,
  qualityIssues,
  releaseMilestones,
  roadSegments,
  trafficSigns
} from "./mockData";
import type { PageKey, RoadSegment } from "./mockData";

type SegmentFeatureProperties = {
  id: string;
};

const pages: { key: PageKey; label: string }[] = [
  { key: "overview", label: "Overview" },
  { key: "map", label: "Map Explorer" },
  { key: "segment", label: "Segment Detail" },
  { key: "issues", label: "Quality Issues" },
  { key: "release", label: "Release Readiness" }
];

export function App() {
  const [activePage, setActivePage] = useState<PageKey>("overview");
  const [selectedSegmentId, setSelectedSegmentId] = useState(roadSegments[0].id);
  const selectedSegment = roadSegments.find((segment) => segment.id === selectedSegmentId) ?? roadSegments[0];

  return (
    <main className="app-shell">
      <aside className="sidebar" aria-label="Dashboard navigation">
        <div className="brand-lockup">
          <span className="brand-mark">GS</span>
          <div>
            <h1>GeoSpeed AI</h1>
            <p>Speed-limit intelligence</p>
          </div>
        </div>
        <nav className="page-nav" aria-label="Pages">
          {pages.map((page) => (
            <button
              key={page.key}
              className={activePage === page.key ? "nav-button active" : "nav-button"}
              type="button"
              onClick={() => setActivePage(page.key)}
            >
              {page.label}
            </button>
          ))}
        </nav>
        <div className="sidebar-status">
          <span>Mock API</span>
          <strong>{roadSegments.length} segments</strong>
        </div>
      </aside>

      <section className="workspace">
        <Header activePage={activePage} selectedSegment={selectedSegment} />
        {activePage === "overview" && (
          <OverviewPage selectedSegmentId={selectedSegmentId} onSelectSegment={setSelectedSegmentId} />
        )}
        {activePage === "map" && (
          <MapExplorer selectedSegmentId={selectedSegmentId} onSelectSegment={setSelectedSegmentId} />
        )}
        {activePage === "segment" && (
          <SegmentDetail segment={selectedSegment} onSelectSegment={setSelectedSegmentId} />
        )}
        {activePage === "issues" && <QualityIssues />}
        {activePage === "release" && <ReleaseReadiness />}
      </section>
    </main>
  );
}

function Header({ activePage, selectedSegment }: { activePage: PageKey; selectedSegment: RoadSegment }) {
  const title = pages.find((page) => page.key === activePage)?.label ?? "Overview";
  return (
    <header className="workspace-header">
      <div>
        <span className="eyebrow">Sample operations workspace</span>
        <h2>{title}</h2>
      </div>
      <div className="header-summary" aria-label="Selected segment">
        <span>Selected</span>
        <strong>{selectedSegment.roadName}</strong>
      </div>
    </header>
  );
}

function OverviewPage({
  selectedSegmentId,
  onSelectSegment
}: {
  selectedSegmentId: string;
  onSelectSegment: (segmentId: string) => void;
}) {
  const averageConfidence = average(roadSegments.map((segment) => segment.confidence));
  const averageCoverage = average(roadSegments.map((segment) => segment.coverage));
  const releaseReadiness = average(roadSegments.map((segment) => segment.readiness));

  return (
    <div className="page-grid overview-grid">
      <MetricTile label="Coverage" value={`${Math.round(averageCoverage * 100)}%`} tone="green" />
      <MetricTile label="Confidence" value={`${Math.round(averageConfidence * 100)}%`} tone="blue" />
      <MetricTile label="Open Issues" value={String(qualityIssues.length)} tone="amber" />
      <MetricTile label="Release Readiness" value={`${Math.round(releaseReadiness * 100)}%`} tone="red" />

      <section className="panel wide">
        <PanelHeader title="Network Confidence" caption="Road segments colored by inference confidence" />
        <SegmentList selectedSegmentId={selectedSegmentId} onSelectSegment={onSelectSegment} />
      </section>

      <section className="panel">
        <PanelHeader title="Coverage" caption="Sample trace coverage by segment" />
        <BarChart
          values={roadSegments.map((segment) => ({
            label: segment.id.replace("seg-sample-", "S"),
            value: segment.coverage,
            color: confidenceColor(segment.coverage)
          }))}
        />
      </section>

      <section className="panel">
        <PanelHeader title="Confidence Distribution" caption="Baseline speed-limit inference confidence" />
        <DistributionChart values={roadSegments.map((segment) => segment.confidence)} />
      </section>
    </div>
  );
}

function MapExplorer({
  selectedSegmentId,
  onSelectSegment
}: {
  selectedSegmentId: string;
  onSelectSegment: (segmentId: string) => void;
}) {
  return (
    <div className="map-explorer">
      <section className="map-shell">
        <DashboardMap selectedSegmentId={selectedSegmentId} onSelectSegment={onSelectSegment} />
      </section>
      <aside className="map-inspector">
        <PanelHeader title="Map Layers" caption="Sample signs and colored road confidence" />
        <Legend />
        <SegmentList selectedSegmentId={selectedSegmentId} onSelectSegment={onSelectSegment} compact />
      </aside>
    </div>
  );
}

function SegmentDetail({
  segment,
  onSelectSegment
}: {
  segment: RoadSegment;
  onSelectSegment: (segmentId: string) => void;
}) {
  const segmentIssues = qualityIssues.filter((issue) => issue.segmentId === segment.id);
  return (
    <div className="page-grid detail-grid">
      <section className="panel wide">
        <PanelHeader title={segment.roadName} caption={`${segment.roadClass} road class`} />
        <div className="segment-hero">
          <MetricTile label="Speed Limit" value={`${segment.inferredSpeedLimit} mph`} tone="blue" />
          <MetricTile label="Confidence" value={`${Math.round(segment.confidence * 100)}%`} tone="green" />
          <MetricTile label="Coverage" value={`${Math.round(segment.coverage * 100)}%`} tone="amber" />
          <MetricTile label="Issues" value={String(segmentIssues.length)} tone="red" />
        </div>
      </section>
      <section className="panel">
        <PanelHeader title="Segment Picker" caption="Inspect another sample segment" />
        <SegmentList selectedSegmentId={segment.id} onSelectSegment={onSelectSegment} compact />
      </section>
      <section className="panel">
        <PanelHeader title="Evidence Mix" caption="Inputs used by baseline inference" />
        <BarChart
          values={[
            { label: "Sign", value: segment.confidence, color: "#12805c" },
            { label: "Trace", value: segment.coverage, color: "#2f6fbb" },
            { label: "Prior", value: roadClassPriorScore(segment), color: "#b7791f" },
            { label: "Gate", value: segment.readiness, color: "#c2410c" }
          ]}
        />
      </section>
      <section className="panel wide">
        <PanelHeader title="Related Issues" caption="Open quality review items for this segment" />
        <IssueTable issues={segmentIssues} emptyText="No open issues for this segment." />
      </section>
    </div>
  );
}

function QualityIssues() {
  const issueCounts = ["critical", "high", "medium", "low"].map((severity) => ({
    label: severity,
    value: qualityIssues.filter((issue) => issue.severity === severity).length,
    color: severityColor(severity)
  }));

  return (
    <div className="page-grid">
      <section className="panel">
        <PanelHeader title="Issue Counts" caption="Open items by severity" />
        <CountChart values={issueCounts} />
      </section>
      <section className="panel wide">
        <PanelHeader title="Quality Work Queue" caption="Sample review backlog" />
        <IssueTable issues={qualityIssues} emptyText="No open quality issues." />
      </section>
    </div>
  );
}

function ReleaseReadiness() {
  const readiness = average(releaseMilestones.map((milestone) => milestone.value));
  return (
    <div className="page-grid release-grid">
      <section className="panel release-panel">
        <PanelHeader title="Release Gate" caption="Sample release candidate health" />
        <Gauge value={readiness} />
      </section>
      <section className="panel wide">
        <PanelHeader title="Readiness Drivers" caption="Coverage, confidence, issue clearance, and policy checks" />
        <BarChart
          values={releaseMilestones.map((milestone) => ({
            label: milestone.label,
            value: milestone.value,
            color: confidenceColor(milestone.value)
          }))}
        />
      </section>
      <section className="panel wide">
        <PanelHeader title="Release Candidate Segments" caption="Confidence and issue gates by road segment" />
        <SegmentList selectedSegmentId="" onSelectSegment={() => undefined} />
      </section>
    </div>
  );
}

function DashboardMap({
  selectedSegmentId,
  onSelectSegment
}: {
  selectedSegmentId: string;
  onSelectSegment: (segmentId: string) => void;
}) {
  const mapContainer = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!mapContainer.current) {
      return;
    }

    const mapCenter: [number, number] = [-74.006, 40.71275];
    const map = new maplibregl.Map({
      container: mapContainer.current,
      style: "https://demotiles.maplibre.org/style.json",
      center: mapCenter,
      zoom: 15.5
    });

    map.addControl(new maplibregl.NavigationControl({ visualizePitch: true }), "top-right");

    map.on("load", () => {
      roadSegments.forEach((segment) => {
        const sourceId = `segment-${segment.id}`;
        const coordinates: Position[] = segment.polyline.map(([longitude, latitude]) => [longitude, latitude]);
        const segmentFeature: Feature<LineString, SegmentFeatureProperties> = {
          type: "Feature",
          properties: { id: segment.id },
          geometry: {
            type: "LineString",
            coordinates
          }
        };
        const segmentSource: GeoJSONSourceSpecification = {
          type: "geojson",
          data: segmentFeature
        };
        const segmentLayer: LineLayerSpecification = {
          id: sourceId,
          type: "line",
          source: sourceId,
          paint: {
            "line-color": confidenceColor(segment.confidence),
            "line-width": segment.id === selectedSegmentId ? 8 : 5,
            "line-opacity": segment.id === selectedSegmentId ? 0.95 : 0.72
          }
        };

        map.addSource(sourceId, segmentSource);
        map.addLayer(segmentLayer);
        map.on("click", sourceId, () => onSelectSegment(segment.id));
      });

      trafficSigns.forEach((sign) => {
        const markerElement = document.createElement("button");
        markerElement.className = "sign-marker";
        markerElement.type = "button";
        markerElement.textContent = sign.label;
        markerElement.setAttribute("aria-label", `${sign.label} sign ${sign.id}`);
        markerElement.addEventListener("click", () => onSelectSegment(sign.segmentId));

        const signCoordinate: [number, number] = sign.coordinate;
        new maplibregl.Marker({ element: markerElement, anchor: "bottom" })
          .setLngLat(signCoordinate)
          .setPopup(new maplibregl.Popup().setText(`${sign.id}: ${sign.label}`))
          .addTo(map);
      });
    });

    return () => map.remove();
  }, [onSelectSegment, selectedSegmentId]);

  return <div ref={mapContainer} className="map-container" data-testid="map-container" />;
}

function SegmentList({
  selectedSegmentId,
  onSelectSegment,
  compact = false
}: {
  selectedSegmentId: string;
  onSelectSegment: (segmentId: string) => void;
  compact?: boolean;
}) {
  return (
    <div className={compact ? "segment-list compact" : "segment-list"}>
      {roadSegments.map((segment) => (
        <button
          key={segment.id}
          className={selectedSegmentId === segment.id ? "segment-row selected" : "segment-row"}
          type="button"
          onClick={() => onSelectSegment(segment.id)}
        >
          <span className="confidence-dot" style={{ backgroundColor: confidenceColor(segment.confidence) }} />
          <span>
            <strong>{segment.roadName}</strong>
            <small>{segment.id}</small>
          </span>
          <span className="row-metric">{Math.round(segment.confidence * 100)}%</span>
        </button>
      ))}
    </div>
  );
}

function MetricTile({ label, value, tone }: { label: string; value: string; tone: "green" | "blue" | "amber" | "red" }) {
  return (
    <section className={`metric-tile ${tone}`}>
      <span>{label}</span>
      <strong>{value}</strong>
    </section>
  );
}

function PanelHeader({ title, caption }: { title: string; caption: string }) {
  return (
    <div className="panel-header">
      <h3>{title}</h3>
      <p>{caption}</p>
    </div>
  );
}

function BarChart({ values }: { values: { label: string; value: number; color: string }[] }) {
  return (
    <div className="bar-chart">
      {values.map((item) => (
        <div className="bar-row" key={item.label}>
          <span>{item.label}</span>
          <div className="bar-track">
            <div className="bar-fill" style={{ width: `${Math.round(item.value * 100)}%`, backgroundColor: item.color }} />
          </div>
          <strong>{Math.round(item.value * 100)}%</strong>
        </div>
      ))}
    </div>
  );
}

function DistributionChart({ values }: { values: number[] }) {
  const buckets = [
    { label: "<65", count: values.filter((value) => value < 0.65).length, color: "#c2410c" },
    { label: "65-75", count: values.filter((value) => value >= 0.65 && value < 0.75).length, color: "#b7791f" },
    { label: "75-85", count: values.filter((value) => value >= 0.75 && value < 0.85).length, color: "#2f6fbb" },
    { label: "85+", count: values.filter((value) => value >= 0.85).length, color: "#12805c" }
  ];
  const maxCount = Math.max(...buckets.map((bucket) => bucket.count), 1);

  return (
    <div className="distribution-chart">
      {buckets.map((bucket) => (
        <div className="distribution-column" key={bucket.label}>
          <div
            className="distribution-bar"
            style={{ height: `${36 + (bucket.count / maxCount) * 130}px`, backgroundColor: bucket.color }}
          />
          <span>{bucket.label}</span>
          <strong>{bucket.count}</strong>
        </div>
      ))}
    </div>
  );
}

function CountChart({ values }: { values: { label: string; value: number; color: string }[] }) {
  const maxValue = Math.max(...values.map((item) => item.value), 1);
  return (
    <div className="count-chart">
      {values.map((item) => (
        <div className="count-row" key={item.label}>
          <span>{item.label}</span>
          <div style={{ width: `${28 + (item.value / maxValue) * 62}%`, backgroundColor: item.color }} />
          <strong>{item.value}</strong>
        </div>
      ))}
    </div>
  );
}

function Gauge({ value }: { value: number }) {
  const percentage = Math.round(value * 100);
  return (
    <div className="gauge" aria-label={`Release readiness ${percentage}%`}>
      <svg viewBox="0 0 180 110" role="img">
        <path className="gauge-track" d="M20 90 A70 70 0 0 1 160 90" />
        <path
          className="gauge-value"
          d="M20 90 A70 70 0 0 1 160 90"
          style={{ strokeDasharray: `${percentage * 2.2} 220` }}
        />
      </svg>
      <strong>{percentage}%</strong>
      <span>Ready with review</span>
    </div>
  );
}

function IssueTable({ issues, emptyText }: { issues: typeof qualityIssues; emptyText: string }) {
  if (issues.length === 0) {
    return <p className="empty-state">{emptyText}</p>;
  }

  return (
    <div className="issue-table">
      {issues.map((issue) => (
        <div className="issue-row" key={issue.id}>
          <span className="severity-pill" style={{ backgroundColor: severityColor(issue.severity) }}>
            {issue.severity}
          </span>
          <div>
            <strong>{issue.title}</strong>
            <small>
              {issue.segmentId} - {issue.owner}
            </small>
          </div>
          <span className="status-chip">{issue.status}</span>
        </div>
      ))}
    </div>
  );
}

function Legend() {
  return (
    <div className="legend">
      {[
        ["High", "#12805c"],
        ["Good", "#2f6fbb"],
        ["Review", "#b7791f"],
        ["Blocked", "#c2410c"]
      ].map(([label, color]) => (
        <span key={label}>
          <i style={{ backgroundColor: color }} />
          {label}
        </span>
      ))}
    </div>
  );
}

function average(values: number[]): number {
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

function roadClassPriorScore(segment: RoadSegment): number {
  return segment.roadClass === "residential" ? 0.9 : segment.roadClass === "primary" ? 0.8 : 0.72;
}

function severityColor(severity: string): string {
  if (severity === "critical") {
    return "#991b1b";
  }
  if (severity === "high") {
    return "#c2410c";
  }
  if (severity === "medium") {
    return "#b7791f";
  }
  return "#2f6fbb";
}
