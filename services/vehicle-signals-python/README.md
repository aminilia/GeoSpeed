# Vehicle Signals Python Service

FastAPI service that simulates COVESA VSS-style vehicle signals for GeoSpeed Auto FDE.

## Endpoints

- `GET /health`
- `GET /signals/current`
- `POST /signals/scenario`
- `POST /signals/replay`
- `GET /signals/adas-status`

## Run

```bash
uvicorn geospeed_vehicle.app:app --reload --host 0.0.0.0 --port 8010
```

Signals are simulated and designed for partner integration demos.
