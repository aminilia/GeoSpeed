package com.geospeed.partner.dto;

public record CreateIssueRequest(
    String partnerId,
    String title,
    String description,
    String issueType,
    String severity,
    String affectedComponent,
    boolean launchBlocker
) {
}

