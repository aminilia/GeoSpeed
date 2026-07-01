package com.geospeed.partner.repository;

import com.geospeed.partner.model.FeatureRequest;
import com.geospeed.partner.model.PartnerIssue;
import com.geospeed.partner.model.PartnerScenario;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import org.springframework.stereotype.Repository;

@Repository
public class PartnerRepository {
    private final List<PartnerScenario> scenarios = new ArrayList<>(List.of(
        new PartnerScenario("oem_speed_alert_demo", "partner-nova-auto", "route-dc-demo-001", "Speed-limit alert demo", "Show alert above 25 mph", List.of(), "none"),
        new PartnerScenario("adas_speed_mismatch", "partner-nova-auto", "route-dc-demo-002", "ADAS cruise-control mismatch", "Flag ADAS set speed above posted limit", List.of("ADAS_SIGNAL_MISMATCH"), "requires_partner_triage"),
        new PartnerScenario("stale_map_data_launch_blocker", "partner-europa-mobility", "route-stale-map-001", "Stale map-data blocker", "Block launch readiness", List.of("STALE_OBSERVATION"), "launch_blocker")
    ));

    private final List<PartnerIssue> issues = new ArrayList<>(List.of(
        new PartnerIssue("pi-001", "partner-nova-auto", "ADAS set speed exceeds limit", "Cruise set speed remains above inferred speed limit.", "ADAS_SIGNAL_MISMATCH", "high", "open", "ADAS Integrations", "vehicle_signal_mapping", "vehicle-signals-python", Instant.parse("2026-07-01T12:00:00Z"), Instant.parse("2026-07-01T12:00:00Z"), true, "Validate signal mapping and partner cruise-control policy."),
        new PartnerIssue("pi-002", "partner-europa-mobility", "Stale speed-limit source", "Freshness score below launch threshold.", "MAP_DATA_GAP", "medium", "triage", "Map Data Quality", "source_freshness", "pipelines", Instant.parse("2026-07-01T12:05:00Z"), Instant.parse("2026-07-01T12:05:00Z"), false, "Refresh authoritative open-data extract.")
    ));

    private final List<FeatureRequest> featureRequests = new ArrayList<>(List.of(
        new FeatureRequest("fr-001", "partner-nova-auto", "Confidence-aware ADAS suppression", "Expose confidence thresholds in partner SDK response.", "ADAS", 88, "partner_api", "2026-Q4", "under_review")
    ));

    public List<PartnerScenario> scenarios() {
        return scenarios;
    }

    public Optional<PartnerScenario> scenario(String id) {
        return scenarios.stream().filter(scenario -> scenario.scenarioId().equals(id)).findFirst();
    }

    public List<PartnerIssue> issues() {
        return issues;
    }

    public PartnerIssue addIssue(PartnerIssue issue) {
        issues.add(issue);
        return issue;
    }

    public Optional<PartnerIssue> triageIssue(String id, String status, String ownerTeam, String rootCauseCategory) {
        for (int index = 0; index < issues.size(); index++) {
            PartnerIssue issue = issues.get(index);
            if (issue.issueId().equals(id)) {
                PartnerIssue updated = issue.withTriage(status, ownerTeam, rootCauseCategory);
                issues.set(index, updated);
                return Optional.of(updated);
            }
        }
        return Optional.empty();
    }

    public List<FeatureRequest> featureRequests() {
        return featureRequests;
    }

    public FeatureRequest addFeatureRequest(String partnerId, String title, String description, String affectedUseCase, int priorityScore, String productArea, String requestedRelease) {
        FeatureRequest request = new FeatureRequest("fr-" + UUID.randomUUID(), partnerId, title, description, affectedUseCase, priorityScore, productArea, requestedRelease, "new");
        featureRequests.add(request);
        return request;
    }
}

