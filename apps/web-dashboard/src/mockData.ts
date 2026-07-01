export type PageKey = "overview" | "map" | "segment" | "issues" | "release";

export type Coordinate = [number, number];

export type RoadSegment = {
  id: string;
  roadName: string;
  roadClass: "primary" | "secondary" | "residential" | "service";
  inferredSpeedLimit: number;
  confidence: number;
  coverage: number;
  readiness: number;
  issueCount: number;
  polyline: Coordinate[];
};

export type TrafficSign = {
  id: string;
  label: string;
  signType: string;
  coordinate: Coordinate;
  detectionConfidence: number;
  segmentId: string;
};

export type QualityIssue = {
  id: string;
  segmentId: string;
  severity: "critical" | "high" | "medium" | "low";
  title: string;
  owner: string;
  status: "open" | "triage" | "blocked";
};

export const roadSegments: RoadSegment[] = [
  {
    id: "seg-syn-001",
    roadName: "Synthetic Main Street",
    roadClass: "residential",
    inferredSpeedLimit: 25,
    confidence: 0.94,
    coverage: 0.98,
    readiness: 0.92,
    issueCount: 0,
    polyline: [
      [-74.0068, 40.71235],
      [-74.00625, 40.71275],
      [-74.0057, 40.71312]
    ]
  },
  {
    id: "seg-syn-002",
    roadName: "Synthetic Market Avenue",
    roadClass: "secondary",
    inferredSpeedLimit: 35,
    confidence: 0.81,
    coverage: 0.87,
    readiness: 0.78,
    issueCount: 2,
    polyline: [
      [-74.00615, 40.71215],
      [-74.0056, 40.71272],
      [-74.00505, 40.71334]
    ]
  },
  {
    id: "seg-syn-003",
    roadName: "Synthetic River Road",
    roadClass: "primary",
    inferredSpeedLimit: 45,
    confidence: 0.68,
    coverage: 0.74,
    readiness: 0.63,
    issueCount: 3,
    polyline: [
      [-74.00705, 40.71205],
      [-74.00642, 40.71252],
      [-74.00588, 40.71295]
    ]
  },
  {
    id: "seg-syn-004",
    roadName: "Synthetic Service Lane",
    roadClass: "service",
    inferredSpeedLimit: 15,
    confidence: 0.57,
    coverage: 0.61,
    readiness: 0.49,
    issueCount: 4,
    polyline: [
      [-74.0054, 40.71225],
      [-74.00495, 40.7126],
      [-74.00465, 40.71305]
    ]
  }
];

export const trafficSigns: TrafficSign[] = [
  {
    id: "sign-syn-001",
    label: "25 mph",
    signType: "speed_limit",
    coordinate: [-74.00628, 40.71274],
    detectionConfidence: 0.96,
    segmentId: "seg-syn-001"
  },
  {
    id: "sign-syn-002",
    label: "35 mph",
    signType: "speed_limit",
    coordinate: [-74.00562, 40.71273],
    detectionConfidence: 0.84,
    segmentId: "seg-syn-002"
  },
  {
    id: "sign-syn-003",
    label: "45 mph",
    signType: "speed_limit",
    coordinate: [-74.00641, 40.71253],
    detectionConfidence: 0.72,
    segmentId: "seg-syn-003"
  },
  {
    id: "sign-syn-004",
    label: "15 mph",
    signType: "speed_limit",
    coordinate: [-74.00496, 40.71261],
    detectionConfidence: 0.63,
    segmentId: "seg-syn-004"
  }
];

export const qualityIssues: QualityIssue[] = [
  {
    id: "issue-syn-001",
    segmentId: "seg-syn-002",
    severity: "medium",
    title: "Trace p85 is 9 mph above inferred limit",
    owner: "Map QA",
    status: "triage"
  },
  {
    id: "issue-syn-002",
    segmentId: "seg-syn-003",
    severity: "high",
    title: "Sign-to-road heading mismatch",
    owner: "Road Matching",
    status: "open"
  },
  {
    id: "issue-syn-003",
    segmentId: "seg-syn-003",
    severity: "medium",
    title: "Sparse trace coverage after midnight",
    owner: "Data Quality",
    status: "open"
  },
  {
    id: "issue-syn-004",
    segmentId: "seg-syn-004",
    severity: "critical",
    title: "Release gate failed for low confidence",
    owner: "Release Ops",
    status: "blocked"
  }
];

export const releaseMilestones = [
  { label: "Coverage", value: 0.86 },
  { label: "Confidence", value: 0.75 },
  { label: "Issues Cleared", value: 0.68 },
  { label: "Policy Checks", value: 0.91 }
];

export function confidenceColor(confidence: number): string {
  if (confidence >= 0.85) {
    return "#12805c";
  }
  if (confidence >= 0.72) {
    return "#2f6fbb";
  }
  if (confidence >= 0.62) {
    return "#b7791f";
  }
  return "#c2410c";
}

