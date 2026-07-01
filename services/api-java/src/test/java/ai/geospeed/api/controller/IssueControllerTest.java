package ai.geospeed.api.controller;

import static org.hamcrest.Matchers.equalTo;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import ai.geospeed.api.dto.IssueResponse;
import ai.geospeed.api.service.IssueService;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(IssueController.class)
class IssueControllerTest {
    @Autowired
    private MockMvc mockMvc;

    @MockitoBean
    private IssueService issueService;

    @Test
    void listIssuesReturnsIssueDtos() throws Exception {
        when(issueService.listIssues()).thenReturn(List.of(
            new IssueResponse("issue-1", "seg-1", "medium", "heading_mismatch", "Synthetic issue")));

        mockMvc.perform(get("/api/v1/issues"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$[0].id", equalTo("issue-1")))
            .andExpect(jsonPath("$[0].segmentId", equalTo("seg-1")));
    }
}

