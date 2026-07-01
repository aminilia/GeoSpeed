package ai.geospeed.api.repository;

import ai.geospeed.api.model.Issue;
import java.util.List;
import org.springframework.stereotype.Repository;

@Repository
public class InMemoryIssueRepository implements IssueRepository {
    private final List<Issue> issues = List.of(
        new Issue(
            "issue-syn-001",
            "seg-syn-002",
            "medium",
            "heading_mismatch",
            "Synthetic stop sign observation is offset from the expected segment heading."),
        new Issue(
            "issue-syn-002",
            "seg-syn-003",
            "low",
            "low_confidence",
            "Synthetic yield sign match is below the preferred confidence threshold.")
    );

    @Override
    public List<Issue> findAll() {
        return issues;
    }
}

