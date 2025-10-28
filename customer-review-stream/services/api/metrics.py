from prometheus_client import Counter, Histogram

requests_total = Counter("api_requests_total", "Total API requests", ["endpoint", "method", "status"])
request_latency = Histogram("api_request_latency_seconds", "Latency per request", ["endpoint"])
