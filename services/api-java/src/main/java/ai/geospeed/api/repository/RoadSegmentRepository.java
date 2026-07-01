package ai.geospeed.api.repository;

import ai.geospeed.api.model.RoadSegment;
import java.util.List;
import java.util.Optional;

public interface RoadSegmentRepository {
    List<RoadSegment> findAll();

    Optional<RoadSegment> findById(String id);
}

