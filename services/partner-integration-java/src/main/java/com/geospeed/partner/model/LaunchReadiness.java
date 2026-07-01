package com.geospeed.partner.model;

public record LaunchReadiness(
    String partnerId,
    double routeCoverageScore,
    double speedLimitQualityScore,
    int openBlockerCount,
    int unresolvedHighSeverityIssues,
    String sdkIntegrationStatus,
    String infotainmentValidationStatus,
    String adasValidationStatus,
    boolean launchReady
) {
}

