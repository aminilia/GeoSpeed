package ai.geospeed.api.controller;

import static org.hamcrest.Matchers.equalTo;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import ai.geospeed.api.dto.QualitySummaryResponse;
import ai.geospeed.api.service.QualityService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(QualityController.class)
class QualityControllerTest {
    @Autowired
    private MockMvc mockMvc;

    @MockitoBean
    private QualityService qualityService;

    @Test
    void summaryReturnsQualityMetrics() throws Exception {
        when(qualityService.getSummary()).thenReturn(new QualitySummaryResponse(3, 2, 0.84, 0.74));

        mockMvc.perform(get("/api/v1/quality/summary"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.segmentCount", equalTo(3)))
            .andExpect(jsonPath("$.openIssueCount", equalTo(2)))
            .andExpect(jsonPath("$.averageMatchConfidence", equalTo(0.84)));
    }
}

