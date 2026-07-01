package ai.geospeed.api.service;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import ai.geospeed.api.model.Coordinate;
import ai.geospeed.api.model.RoadSegment;
import ai.geospeed.api.repository.RoadSegmentRepository;
import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.Test;
import org.springframework.web.server.ResponseStatusException;

class SegmentServiceTest {
    @Test
    void listSegmentsMapsPolylineCoordinates() {
        SegmentService service = new SegmentService(new FakeRoadSegmentRepository());

        var segments = service.listSegments();

        assertThat(segments).hasSize(1);
        assertThat(segments.getFirst().id()).isEqualTo("seg-1");
        assertThat(segments.getFirst().polyline()).hasSize(2);
    }

    @Test
    void getSegmentThrowsNotFoundForMissingSegment() {
        SegmentService service = new SegmentService(new FakeRoadSegmentRepository());

        assertThatThrownBy(() -> service.getSegment("missing"))
            .isInstanceOf(ResponseStatusException.class)
            .hasMessageContaining("segment not found");
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

