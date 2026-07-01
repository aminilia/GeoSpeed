package ai.geospeed.api.service;

import static org.assertj.core.api.Assertions.assertThat;

import ai.geospeed.api.model.Coordinate;
import ai.geospeed.api.model.Issue;
import ai.geospeed.api.model.RoadSegment;
import ai.geospeed.api.repository.IssueRepository;
import ai.geospeed.api.repository.RoadSegmentRepository;
import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.Test;

class QualityServiceTest {
    @Test
    void summaryCalculatesReadinessFromSyntheticData() {
        QualityService service = new QualityService(new FakeRoadSegmentRepository(), new FakeIssueRepository());

        var summary = service.getSummary();

        assertThat(summary.segmentCount()).isEqualTo(2);
        assertThat(summary.openIssueCount()).isEqualTo(1);
        assertThat(summary.averageMatchConfidence()).isEqualTo(0.9);
        assertThat(summary.releaseReadinessScore()).isEqualTo(0.85);
    }

    private static class FakeRoadSegmentRepository implements RoadSegmentRepository {
        @Override
        public List<RoadSegment> findAll() {
            return List.of(
                segment("seg-1", 0.8),
                segment("seg-2", 1.0));
        }

        @Override
        public Optional<RoadSegment> findById(String id) {
            return findAll().stream().filter(segment -> segment.id().equals(id)).findFirst();
        }

        private RoadSegment segment(String id, double confidence) {
            return new RoadSegment(
                id,
                "Synthetic Road",
                "25 mph",
                confidence,
                List.of(new Coordinate(-74.0, 40.0), new Coordinate(-74.1, 40.1)));
        }
    }

    private static class FakeIssueRepository implements IssueRepository {
        @Override
        public List<Issue> findAll() {
            return List.of(new Issue("issue-1", "seg-1", "low", "low_confidence", "Synthetic issue"));
        }
    }
}

