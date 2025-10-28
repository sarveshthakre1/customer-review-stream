# Customer-Review Stream (FastAPI + Redis + Worker + PostgreSQL)

Small but production‑flavored microservice system:
- **FastAPI** for ingest + aggregation endpoints
- **Redis** queue for decoupled processing
- **Worker** analyzes sentiment via TextBlob
- **PostgreSQL** persistence
- **Prometheus** metrics for operational visibility
- **GitHub Actions** CI for lint/test/build

## Run locally
```bash
cp .env.example .env
docker compose up --build
```
Visit `http://localhost:8000/docs` for interactive API.

### Endpoints
- `POST /reviews` — submit `{ customer_id, product_id, text }` → returns `{ request_id }`
- `GET /reviews/{request_id}` — fetch processed review (if ready)
- `GET /stats/sentiment` — aggregate sentiment by product
- `GET /healthz` — liveness
- `GET /metrics` — Prometheus metrics

## Why this matches SDE internship
- Microservices & distributed processing
- Cloud‑native containers (Docker)
- Operational excellence (health checks, metrics)
- CI/CD with tests and linting
- Clean code & docs (OpenAPI)

## Deploy ideas
- Push images to GHCR, deploy to AWS ECS Fargate.
