# api-java

Spring Boot REST API for GeoSpeed sample/open-data-compatible road quality workflows.

## Endpoints

- `GET /api/v1/health`
- `GET /api/v1/segments`
- `GET /api/v1/segments/{id}`
- `GET /api/v1/quality/summary`
- `GET /api/v1/issues`
- `POST /api/v1/release-candidate`

## OpenAPI

When the service is running:

- Swagger UI: `http://localhost:8080/swagger-ui/index.html`
- OpenAPI JSON: `http://localhost:8080/v3/api-docs`

## Development

```bash
mvn test
mvn spring-boot:run
```

The first repository implementation is intentionally in memory and uses only small sample/open-data-compatible data.
