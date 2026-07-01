package ai.geospeed.api.repository;

import ai.geospeed.api.model.Coordinate;
import ai.geospeed.api.model.RoadSegment;
import java.util.List;
import java.util.Optional;
import org.springframework.stereotype.Repository;

@Repository
public class InMemoryRoadSegmentRepository implements RoadSegmentRepository {
    private final List<RoadSegment> segments = List.of(
        new RoadSegment(
            "seg-syn-001",
            "Synthetic Main Street",
            "25 mph",
            0.94,
            List.of(
                new Coordinate(-74.0063, 40.7125),
                new Coordinate(-74.0057, 40.7131))),
        new RoadSegment(
            "seg-syn-002",
            "Synthetic Market Avenue",
            "stop_controlled",
            0.82,
            List.of(
                new Coordinate(-74.0059, 40.7127),
                new Coordinate(-74.0052, 40.7134))),
        new RoadSegment(
            "seg-syn-003",
            "Synthetic River Road",
            "yield_controlled",
            0.76,
            List.of(
                new Coordinate(-74.0068, 40.7122),
                new Coordinate(-74.0060, 40.7129)))
    );

    @Override
    public List<RoadSegment> findAll() {
        return segments;
    }

    @Override
    public Optional<RoadSegment> findById(String id) {
        return segments.stream()
            .filter(segment -> segment.id().equals(id))
            .findFirst();
    }
}

