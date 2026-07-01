package com.geospeed.partner.model;

import java.time.Instant;

public record PartnerIssue(
    String issueId,
    String partnerId,
    String title,
    String description,
    String issueType,
    String severity,
    String status,
    String ownerTeam,
    String rootCauseCategory,
    String affectedComponent,
    Instant createdAt,
    Instant updatedAt,
    boolean isLaunchBlocker,
    String recommendedAction
) {
    public PartnerIssue withTriage(String status, String ownerTeam, String rootCauseCategory) {
        return new PartnerIssue(
            issueId,
            partnerId,
            title,
            description,
            issueType,
            severity,
            status,
            ownerTeam,
            rootCauseCategory,
            affectedComponent,
            createdAt,
            Instant.now(),
            isLaunchBlocker,
            recommendedAction);
    }
}

