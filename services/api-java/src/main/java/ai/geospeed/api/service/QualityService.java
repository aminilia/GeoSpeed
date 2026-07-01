package ai.geospeed.api.service;

import ai.geospeed.api.dto.QualitySummaryResponse;
import ai.geospeed.api.model.RoadSegment;
import ai.geospeed.api.repository.IssueRepository;
import ai.geospeed.api.repository.RoadSegmentRepository;
import java.util.List;
import org.springframework.stereotype.Service;

@Service
public class QualityService {
    private final RoadSegmentRepository roadSegmentRepository;
    private final IssueRepository issueRepository;

    public QualityService(RoadSegmentRepository roadSegmentRepository, IssueRepository issueRepository) {
        this.roadSegmentRepository = roadSegmentRepository;
        this.issueRepository = issueRepository;
    }

    public QualitySummaryResponse getSummary() {
        List<RoadSegment> segments = roadSegmentRepository.findAll();
        int issueCount = issueRepository.findAll().size();
        double averageConfidence = segments.stream()
            .mapToDouble(RoadSegment::matchConfidence)
            .average()
            .orElse(0.0);
        double readinessScore = Math.max(0.0, averageConfidence - issueCount * 0.05);

        return new QualitySummaryResponse(
            segments.size(),
            issueCount,
            roundThreeDecimals(averageConfidence),
            roundThreeDecimals(readinessScore));
    }

    private double roundThreeDecimals(double value) {
        return Math.round(value * 1000.0) / 1000.0;
    }
}

