# Customer-Review Stream (FastAPI + Redis + Worker + PostgreSQL)

![Build](https://img.shields.io/github/actions/workflow/status/sarveshthakre1/customer-review-stream/ci.yml?branch=main)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![Made with FastAPI](https://img.shields.io/badge/FastAPI-🏎️-brightgreen)
![License](https://img.shields.io/badge/license-MIT-lightgrey)
 
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

## 🧠 Architecture Diagram

```mermaid
flowchart LR
  Client -->|POST /reviews| API[FastAPI API]
  API -->|LPUSH review_jobs| Redis[(Redis Queue)]
  Worker -->|BRPOP review_jobs| Redis
  API -->|INSERT| DB[(PostgreSQL)]
  Worker -->|UPDATE sentiment| DB
  API -->|GET /stats| DB
  API -->|/metrics| Prometheus
  Worker -->|/metrics| Prometheus
