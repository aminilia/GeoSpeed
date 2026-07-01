package ai.geospeed.api.controller;

import static org.hamcrest.Matchers.equalTo;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import ai.geospeed.api.dto.ReleaseCandidateRequest;
import ai.geospeed.api.dto.ReleaseCandidateResponse;
import ai.geospeed.api.service.ReleaseCandidateService;
import java.time.Instant;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(ReleaseCandidateController.class)
class ReleaseCandidateControllerTest {
    @Autowired
    private MockMvc mockMvc;

    @MockitoBean
    private ReleaseCandidateService releaseCandidateService;

    @Test
    void createReleaseCandidateReturnsCreated() throws Exception {
        when(releaseCandidateService.createReleaseCandidate(any(ReleaseCandidateRequest.class)))
            .thenReturn(new ReleaseCandidateResponse(
                "rc-123",
                "Synthetic July Review",
                "created",
                List.of("seg-syn-001"),
                Instant.parse("2026-07-01T12:00:00Z")));

        mockMvc.perform(post("/api/v1/release-candidate")
                .contentType(MediaType.APPLICATION_JSON)
                .content("""
                    {
                      "name": "Synthetic July Review",
                      "segmentIds": ["seg-syn-001"],
                      "requestedBy": "qa"
                    }
                    """))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.id", equalTo("rc-123")))
            .andExpect(jsonPath("$.status", equalTo("created")));
    }
}

