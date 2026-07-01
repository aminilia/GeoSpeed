package ai.geospeed.api.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {
    @Bean
    OpenAPI geoSpeedOpenApi() {
        return new OpenAPI()
            .info(new Info()
                .title("GeoSpeed API")
                .version("0.1.0")
                .description("REST API for synthetic geospatial road segment quality workflows."));
    }
}

