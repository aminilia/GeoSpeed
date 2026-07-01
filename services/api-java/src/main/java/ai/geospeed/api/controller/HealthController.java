package ai.geospeed.api.controller;

import ai.geospeed.api.dto.HealthResponse;
import io.swagger.v3.oas.annotations.Operation;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/health")
public class HealthController {
    @Operation(summary = "Report API health")
    @GetMapping
    public HealthResponse health() {
        return new HealthResponse("ok", "api-java", "0.1.0");
    }
}

