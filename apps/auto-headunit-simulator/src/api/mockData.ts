export type VehicleFrame = {
  timestamp: string;
  roadSegment: string;
  roadName: string;
  vehicleSpeed: number;
  speedLimit: number | null;
  speedUnit: string;
  confidenceScore: number;
  evidenceSources: string[];
  issueFlags: string[];
  staleMapData: boolean;
  adasMismatch: boolean;
  routeCoverage: number;
  partnerId: string;
  scenarioId: string;
};

export const replay: VehicleFrame[] = [
  {
    timestamp: "12:00:00",
    roadSegment: "dc_road_001",
    roadName: "Sample Main Street NW",
    vehicleSpeed: 23,
    speedLimit: 25,
    speedUnit: "mph",
    confidenceScore: 0.94,
    evidenceSources: ["dc_open_data_sample", "osm_maxspeed"],
    issueFlags: [],
    staleMapData: false,
    adasMismatch: false,
    routeCoverage: 0.91,
    partnerId: "partner-nova-auto",
    scenarioId: "oem_speed_alert_demo"
  },
  {
    timestamp: "12:00:05",
    roadSegment: "dc_road_001",
    roadName: "Sample Main Street NW",
    vehicleSpeed: 32,
    speedLimit: 25,
    speedUnit: "mph",
    confidenceScore: 0.94,
    evidenceSources: ["dc_open_data_sample", "osm_maxspeed"],
    issueFlags: ["SPEED_LIMIT_ALERT"],
    staleMapData: false,
    adasMismatch: true,
    routeCoverage: 0.91,
    partnerId: "partner-nova-auto",
    scenarioId: "adas_speed_mismatch"
  },
  {
    timestamp: "12:08:00",
    roadSegment: "nyc_road_001",
    roadName: "Sample Brooklyn Street",
    vehicleSpeed: 31,
    speedLimit: 25,
    speedUnit: "mph",
    confidenceScore: 0.86,
    evidenceSources: ["nyc_open_data_sample"],
    issueFlags: ["STALE_OBSERVATION"],
    staleMapData: true,
    adasMismatch: false,
    routeCoverage: 0.74,
    partnerId: "partner-europa-mobility",
    scenarioId: "stale_map_data_launch_blocker"
  }
];

export const launchChecks = [
  { label: "Route Coverage", status: "pass", value: "91%" },
  { label: "Speed Quality", status: "pass", value: "86%" },
  { label: "Open Blockers", status: "fail", value: "1" },
  { label: "ADAS Validation", status: "review", value: "Needs review" },
  { label: "Infotainment Validation", status: "pass", value: "Validated" }
];

