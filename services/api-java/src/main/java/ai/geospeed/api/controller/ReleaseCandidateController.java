package ai.geospeed.api.controller;

import ai.geospeed.api.dto.ReleaseCandidateRequest;
import ai.geospeed.api.dto.ReleaseCandidateResponse;
import ai.geospeed.api.service.ReleaseCandidateService;
import io.swagger.v3.oas.annotations.Operation;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/release-candidate")
public class ReleaseCandidateController {
    private final ReleaseCandidateService releaseCandidateService;

    public ReleaseCandidateController(ReleaseCandidateService releaseCandidateService) {
        this.releaseCandidateService = releaseCandidateService;
    }

    @Operation(summary = "Create a synthetic release candidate review")
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public ReleaseCandidateResponse create(@RequestBody ReleaseCandidateRequest request) {
        return releaseCandidateService.createReleaseCandidate(request);
    }
}

