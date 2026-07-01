package ai.geospeed.api.service;

import ai.geospeed.api.dto.ReleaseCandidateRequest;
import ai.geospeed.api.dto.ReleaseCandidateResponse;
import ai.geospeed.api.repository.RoadSegmentRepository;
import java.time.Instant;
import java.util.List;
import java.util.UUID;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

@Service
public class ReleaseCandidateService {
    private final RoadSegmentRepository roadSegmentRepository;

    public ReleaseCandidateService(RoadSegmentRepository roadSegmentRepository) {
        this.roadSegmentRepository = roadSegmentRepository;
    }

    public ReleaseCandidateResponse createReleaseCandidate(ReleaseCandidateRequest request) {
        if (request.name() == null || request.name().isBlank()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "release candidate name is required");
        }

        List<String> segmentIds = request.segmentIds() == null ? List.of() : request.segmentIds();
        for (String segmentId : segmentIds) {
            if (roadSegmentRepository.findById(segmentId).isEmpty()) {
                throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "unknown segment id: " + segmentId);
            }
        }

        return new ReleaseCandidateResponse(
            "rc-" + UUID.randomUUID(),
            request.name(),
            "created",
            segmentIds,
            Instant.now());
    }
}

