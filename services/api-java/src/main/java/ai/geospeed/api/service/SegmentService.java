package ai.geospeed.api.service;

import ai.geospeed.api.dto.CoordinateDto;
import ai.geospeed.api.dto.SegmentResponse;
import ai.geospeed.api.model.Coordinate;
import ai.geospeed.api.model.RoadSegment;
import ai.geospeed.api.repository.RoadSegmentRepository;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

@Service
public class SegmentService {
    private final RoadSegmentRepository roadSegmentRepository;

    public SegmentService(RoadSegmentRepository roadSegmentRepository) {
        this.roadSegmentRepository = roadSegmentRepository;
    }

    public List<SegmentResponse> listSegments() {
        return roadSegmentRepository.findAll().stream()
            .map(this::toResponse)
            .toList();
    }

    public SegmentResponse getSegment(String id) {
        return roadSegmentRepository.findById(id)
            .map(this::toResponse)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "segment not found: " + id));
    }

    private SegmentResponse toResponse(RoadSegment segment) {
        return new SegmentResponse(
            segment.id(),
            segment.roadName(),
            segment.speedLimit(),
            segment.matchConfidence(),
            segment.polyline().stream().map(this::toCoordinateDto).toList());
    }

    private CoordinateDto toCoordinateDto(Coordinate coordinate) {
        return new CoordinateDto(coordinate.lon(), coordinate.lat());
    }
}

