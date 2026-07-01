package com.geospeed.partner.model;

import java.util.List;

public record PartnerScenario(
    String scenarioId,
    String partnerId,
    String routeId,
    String description,
    String expectedBehavior,
    List<String> issueFlags,
    String launchReadinessImpact
) {
}

