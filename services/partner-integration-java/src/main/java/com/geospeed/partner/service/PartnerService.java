package com.geospeed.partner.service;

import com.geospeed.partner.dto.CreateFeatureRequest;
import com.geospeed.partner.dto.CreateIssueRequest;
import com.geospeed.partner.dto.TriageIssueRequest;
import com.geospeed.partner.model.FeatureRequest;
import com.geospeed.partner.model.LaunchReadiness;
import com.geospeed.partner.model.PartnerIssue;
import com.geospeed.partner.model.PartnerScenario;
import com.geospeed.partner.repository.PartnerRepository;
import java.time.Instant;
import java.util.List;
import java.util.UUID;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

@Service
public class PartnerService {
    private final PartnerRepository repository;

    public PartnerService(PartnerRepository repository) {
        this.repository = repository;
    }

    public List<PartnerScenario> scenarios() {
        return repository.scenarios();
    }

    public PartnerScenario scenario(String id) {
        return repository.scenario(id).orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "scenario not found"));
    }

    public List<PartnerIssue> issues() {
        return repository.issues();
    }

    public PartnerIssue createIssue(CreateIssueRequest request) {
        PartnerIssue issue = new PartnerIssue(
            "pi-" + UUID.randomUUID(),
            request.partnerId(),
            request.title(),
            request.description(),
            request.issueType(),
            request.severity(),
            "open",
            "FDE Intake",
            "untriaged",
            request.affectedComponent(),
            Instant.now(),
            Instant.now(),
            request.launchBlocker(),
            "Triage with partner scenario replay and assign owner team.");
        return repository.addIssue(issue);
    }

    public PartnerIssue triageIssue(String id, TriageIssueRequest request) {
        return repository.triageIssue(id, request.status(), request.ownerTeam(), request.rootCauseCategory())
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "issue not found"));
    }

    public LaunchReadiness launchReadiness() {
        int blockers = (int) repository.issues().stream().filter(PartnerIssue::isLaunchBlocker).filter(issue -> !"closed".equals(issue.status())).count();
        int highSeverity = (int) repository.issues().stream().filter(issue -> List.of("critical", "high").contains(issue.severity())).filter(issue -> !"closed".equals(issue.status())).count();
        boolean ready = blockers == 0 && highSeverity == 0;
        return new LaunchReadiness("partner-nova-auto", 0.91, 0.86, blockers, highSeverity, "validated", "validated", highSeverity == 0 ? "validated" : "needs_review", ready);
    }

    public FeatureRequest createFeatureRequest(CreateFeatureRequest request) {
        return repository.addFeatureRequest(request.partnerId(), request.title(), request.description(), request.affectedUseCase(), request.priorityScore(), request.productArea(), request.requestedRelease());
    }

    public List<FeatureRequest> roadmapFeedback() {
        return repository.featureRequests();
    }
}

