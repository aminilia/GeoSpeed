package ai.geospeed.api.controller;

import ai.geospeed.api.dto.QualitySummaryResponse;
import ai.geospeed.api.service.QualityService;
import io.swagger.v3.oas.annotations.Operation;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/quality")
public class QualityController {
    private final QualityService qualityService;

    public QualityController(QualityService qualityService) {
        this.qualityService = qualityService;
    }

    @Operation(summary = "Summarize road segment quality metrics")
    @GetMapping("/summary")
    public QualitySummaryResponse summary() {
        return qualityService.getSummary();
    }
}

