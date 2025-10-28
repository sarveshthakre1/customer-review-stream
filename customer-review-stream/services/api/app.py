import os
from uuid import uuid4
from fastapi import FastAPI, Response
from redis import Redis
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from models import ReviewIn
import storage
from metrics import requests_total, request_latency

app = FastAPI(title="Customer Review API", version="0.1.0")
redis = Redis(host=os.getenv("REDIS_HOST", "redis"), port=int(os.getenv("REDIS_PORT", 6379)), decode_responses=True)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.post("/reviews")
def create_review(payload: ReviewIn):
    with request_latency.labels("/reviews").time():
        rid = uuid4()
        storage.insert_review(rid, payload.customer_id, payload.product_id, payload.text)
        redis.lpush("review_jobs", str(rid))
        requests_total.labels("/reviews", "POST", 200).inc()
        return {"request_id": str(rid)}

@app.get("/reviews/{request_id}")
def get_review(request_id: str):
    data = storage.get_review(request_id)
    status = 200 if data else 404
    requests_total.labels("/reviews/{id}", "GET", status).inc()
    return (data or {"error": "not found"})

@app.get("/stats/sentiment")
def sentiment_stats():
    rows = storage.get_sentiment_by_product()
    return {"products": [{"product_id": r[0], "avg_sentiment": float(r[1])} for r in rows]}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
