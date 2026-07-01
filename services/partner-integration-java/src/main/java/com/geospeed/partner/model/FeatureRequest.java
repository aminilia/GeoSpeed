package com.geospeed.partner.model;

public record FeatureRequest(
    String requestId,
    String partnerId,
    String title,
    String description,
    String affectedUseCase,
    int priorityScore,
    String productArea,
    String requestedRelease,
    String roadmapStatus
) {
}

