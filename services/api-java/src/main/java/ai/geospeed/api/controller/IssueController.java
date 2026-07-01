package ai.geospeed.api.controller;

import ai.geospeed.api.dto.IssueResponse;
import ai.geospeed.api.service.IssueService;
import io.swagger.v3.oas.annotations.Operation;
import java.util.List;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/issues")
public class IssueController {
    private final IssueService issueService;

    public IssueController(IssueService issueService) {
        this.issueService = issueService;
    }

    @Operation(summary = "List open synthetic data quality issues")
    @GetMapping
    public List<IssueResponse> listIssues() {
        return issueService.listIssues();
    }
}

