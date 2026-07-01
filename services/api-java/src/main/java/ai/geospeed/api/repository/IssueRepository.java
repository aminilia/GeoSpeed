package ai.geospeed.api.repository;

import ai.geospeed.api.model.Issue;
import java.util.List;

public interface IssueRepository {
    List<Issue> findAll();
}

