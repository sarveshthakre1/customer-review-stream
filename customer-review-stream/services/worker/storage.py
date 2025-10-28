import os
import psycopg2

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    dbname=os.getenv("POSTGRES_DB"),
)
conn.autocommit = True

def set_sentiment(id_, score: float):
    with conn.cursor() as cur:
        cur.execute("UPDATE reviews SET sentiment=%s WHERE id=%s", (score, str(id_)))
