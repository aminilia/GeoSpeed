# ml-python

FastAPI service for baseline speed-limit inference using synthetic-safe inputs.

## Endpoints

- `GET /health`
- `POST /infer/speed-limit`
- `POST /evaluate`
- `POST /quality-score`

## Inference Inputs

The baseline model combines:

- Known speed tag
- Sign detection confidence
- Sign-to-road match confidence
- Trace speed statistics
- Road class prior

Responses include `inferred_speed_limit`, `confidence_score`, `evidence_sources`, and `issue_flags`.

## Run

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Test

```bash
python -m pytest
```

