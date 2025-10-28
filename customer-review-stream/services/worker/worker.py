import os
from redis import Redis
from textblob import TextBlob
from prometheus_client import start_http_server, Counter
import storage

jobs_processed = Counter("worker_jobs_processed_total", "Total jobs processed")

redis = Redis(host=os.getenv("REDIS_HOST", "redis"), port=int(os.getenv("REDIS_PORT", 6379)), decode_responses=True)

# expose Prometheus on 8001
start_http_server(8001)

print("Worker started")
while True:
    job = redis.brpop("review_jobs", timeout=5)
    if not job:
        continue
    _, review_id = job
    try:
        # NOTE: For a more realistic worker, you would fetch review text from DB.
        # Here we just compute a placeholder polarity from the ID string for simplicity.
        score = float(TextBlob(review_id).sentiment.polarity)
        storage.set_sentiment(review_id, score)
        jobs_processed.inc()
    except Exception as e:
        print("Error processing", review_id, e)
