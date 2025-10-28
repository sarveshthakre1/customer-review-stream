import os
import psycopg2
import psycopg2.extras
from uuid import UUID

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    dbname=os.getenv("POSTGRES_DB"),
)
conn.autocommit = True

def insert_review(id_, customer_id, product_id, text):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO reviews(id, customer_id, product_id, text) VALUES(%s,%s,%s,%s)",
            (str(id_), customer_id, product_id, text),
        )

def get_review(id_: str):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("SELECT * FROM reviews WHERE id=%s", (str(id_),))
        row = cur.fetchone()
        return dict(row) if row else None

def get_sentiment_by_product():
    with conn.cursor() as cur:
        cur.execute("SELECT product_id, AVG(sentiment) FROM reviews WHERE sentiment IS NOT NULL GROUP BY product_id")
        return cur.fetchall()
