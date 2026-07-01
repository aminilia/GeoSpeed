package ai.geospeed.api.controller;

import ai.geospeed.api.dto.SegmentResponse;
import ai.geospeed.api.service.SegmentService;
import io.swagger.v3.oas.annotations.Operation;
import java.util.List;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/segments")
public class SegmentController {
    private final SegmentService segmentService;

    public SegmentController(SegmentService segmentService) {
        this.segmentService = segmentService;
    }

    @Operation(summary = "List synthetic road segments")
    @GetMapping
    public List<SegmentResponse> listSegments() {
        return segmentService.listSegments();
    }

    @Operation(summary = "Get a synthetic road segment by id")
    @GetMapping("/{id}")
    public SegmentResponse getSegment(@PathVariable String id) {
        return segmentService.getSegment(id);
    }
}

