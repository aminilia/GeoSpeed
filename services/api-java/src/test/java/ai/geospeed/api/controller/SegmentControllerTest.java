package ai.geospeed.api.controller;

import static org.hamcrest.Matchers.equalTo;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import ai.geospeed.api.dto.CoordinateDto;
import ai.geospeed.api.dto.SegmentResponse;
import ai.geospeed.api.service.SegmentService;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.http.HttpStatus;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.web.server.ResponseStatusException;

@WebMvcTest(SegmentController.class)
class SegmentControllerTest {
    @Autowired
    private MockMvc mockMvc;

    @MockitoBean
    private SegmentService segmentService;

    @Test
    void listSegmentsReturnsSegmentDtos() throws Exception {
        when(segmentService.listSegments()).thenReturn(List.of(segment()));

        mockMvc.perform(get("/api/v1/segments"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$[0].id", equalTo("seg-syn-001")))
            .andExpect(jsonPath("$[0].polyline[0].lon", equalTo(-74.0063)));
    }

    @Test
    void getSegmentReturnsOneSegment() throws Exception {
        when(segmentService.getSegment("seg-syn-001")).thenReturn(segment());

        mockMvc.perform(get("/api/v1/segments/seg-syn-001"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.roadName", equalTo("Synthetic Main Street")));
    }

    @Test
    void getSegmentReturnsNotFound() throws Exception {
        when(segmentService.getSegment("missing"))
            .thenThrow(new ResponseStatusException(HttpStatus.NOT_FOUND, "segment not found: missing"));

        mockMvc.perform(get("/api/v1/segments/missing"))
            .andExpect(status().isNotFound());
    }

    private SegmentResponse segment() {
        return new SegmentResponse(
            "seg-syn-001",
            "Synthetic Main Street",
            "25 mph",
            0.94,
            List.of(new CoordinateDto(-74.0063, 40.7125)));
    }
}

