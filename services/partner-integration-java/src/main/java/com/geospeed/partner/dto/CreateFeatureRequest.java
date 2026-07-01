package com.geospeed.partner.dto;

public record CreateFeatureRequest(
    String partnerId,
    String title,
    String description,
    String affectedUseCase,
    int priorityScore,
    String productArea,
    String requestedRelease
) {
}

