package ai.geospeed.api.service;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import ai.geospeed.api.dto.ReleaseCandidateRequest;
import ai.geospeed.api.model.Coordinate;
import ai.geospeed.api.model.RoadSegment;
import ai.geospeed.api.repository.RoadSegmentRepository;
import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.Test;
import org.springframework.web.server.ResponseStatusException;

class ReleaseCandidateServiceTest {
    @Test
    void createReleaseCandidateValidatesSegments() {
        ReleaseCandidateService service = new ReleaseCandidateService(new FakeRoadSegmentRepository());

        var response = service.createReleaseCandidate(
            new ReleaseCandidateRequest("Synthetic Release", List.of("seg-1"), "qa"));

        assertThat(response.id()).startsWith("rc-");
        assertThat(response.segmentIds()).containsExactly("seg-1");
        assertThat(response.status()).isEqualTo("created");
    }

    @Test
    void createReleaseCandidateRejectsUnknownSegments() {
        ReleaseCandidateService service = new ReleaseCandidateService(new FakeRoadSegmentRepository());

        assertThatThrownBy(() -> service.createReleaseCandidate(
            new ReleaseCandidateRequest("Synthetic Release", List.of("missing"), "qa")))
            .isInstanceOf(ResponseStatusException.class)
            .hasMessageContaining("unknown segment id");
    }

    private static class FakeRoadSegmentRepository implements RoadSegmentRepository {
        @Override
        public List<RoadSegment> findAll() {
            return List.of(segment());
        }

        @Override
        public Optional<RoadSegment> findById(String id) {
            return "seg-1".equals(id) ? Optional.of(segment()) : Optional.empty();
        }

        private RoadSegment segment() {
            return new RoadSegment(
                "seg-1",
                "Synthetic Road",
                "25 mph",
                0.9,
                List.of(new Coordinate(-74.0, 40.0), new Coordinate(-74.1, 40.1)));
        }
    }
}

