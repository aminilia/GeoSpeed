package ai.geospeed.api.service;

import static org.assertj.core.api.Assertions.assertThat;

import ai.geospeed.api.model.Issue;
import ai.geospeed.api.repository.IssueRepository;
import java.util.List;
import org.junit.jupiter.api.Test;

class IssueServiceTest {
    @Test
    void listIssuesMapsDomainToDto() {
        IssueService service = new IssueService(new FakeIssueRepository());

        var issues = service.listIssues();

        assertThat(issues).hasSize(1);
        assertThat(issues.getFirst().segmentId()).isEqualTo("seg-1");
    }

    private static class FakeIssueRepository implements IssueRepository {
        @Override
        public List<Issue> findAll() {
            return List.of(new Issue("issue-1", "seg-1", "low", "low_confidence", "Synthetic issue"));
        }
    }
}

