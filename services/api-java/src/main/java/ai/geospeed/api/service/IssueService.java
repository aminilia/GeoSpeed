package ai.geospeed.api.service;

import ai.geospeed.api.dto.IssueResponse;
import ai.geospeed.api.model.Issue;
import ai.geospeed.api.repository.IssueRepository;
import java.util.List;
import org.springframework.stereotype.Service;

@Service
public class IssueService {
    private final IssueRepository issueRepository;

    public IssueService(IssueRepository issueRepository) {
        this.issueRepository = issueRepository;
    }

    public List<IssueResponse> listIssues() {
        return issueRepository.findAll().stream()
            .map(this::toResponse)
            .toList();
    }

    private IssueResponse toResponse(Issue issue) {
        return new IssueResponse(
            issue.id(),
            issue.segmentId(),
            issue.severity(),
            issue.category(),
            issue.description());
    }
}

