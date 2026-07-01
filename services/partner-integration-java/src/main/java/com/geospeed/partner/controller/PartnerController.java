package com.geospeed.partner.controller;

import com.geospeed.partner.dto.CreateFeatureRequest;
import com.geospeed.partner.dto.CreateIssueRequest;
import com.geospeed.partner.dto.TriageIssueRequest;
import com.geospeed.partner.model.FeatureRequest;
import com.geospeed.partner.model.LaunchReadiness;
import com.geospeed.partner.model.PartnerIssue;
import com.geospeed.partner.model.PartnerScenario;
import com.geospeed.partner.service.PartnerService;
import java.util.List;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/partner")
public class PartnerController {
    private final PartnerService partnerService;

    public PartnerController(PartnerService partnerService) {
        this.partnerService = partnerService;
    }

    @GetMapping("/health")
    public Map<String, String> health() {
        return Map.of("status", "ok", "service", "partner-integration-java");
    }

    @GetMapping("/scenarios")
    public List<PartnerScenario> scenarios() {
        return partnerService.scenarios();
    }

    @GetMapping("/scenarios/{id}")
    public PartnerScenario scenario(@PathVariable String id) {
        return partnerService.scenario(id);
    }

    @GetMapping("/issues")
    public List<PartnerIssue> issues() {
        return partnerService.issues();
    }

    @PostMapping("/issues")
    @ResponseStatus(HttpStatus.CREATED)
    public PartnerIssue createIssue(@RequestBody CreateIssueRequest request) {
        return partnerService.createIssue(request);
    }

    @PatchMapping("/issues/{id}/triage")
    public PartnerIssue triageIssue(@PathVariable String id, @RequestBody TriageIssueRequest request) {
        return partnerService.triageIssue(id, request);
    }

    @GetMapping("/launch-readiness")
    public LaunchReadiness launchReadiness() {
        return partnerService.launchReadiness();
    }

    @PostMapping("/feature-requests")
    @ResponseStatus(HttpStatus.CREATED)
    public FeatureRequest createFeatureRequest(@RequestBody CreateFeatureRequest request) {
        return partnerService.createFeatureRequest(request);
    }

    @GetMapping("/roadmap-feedback")
    public List<FeatureRequest> roadmapFeedback() {
        return partnerService.roadmapFeedback();
    }
}

