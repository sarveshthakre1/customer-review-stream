from pydantic import BaseModel
from uuid import UUID

class ReviewIn(BaseModel):
    customer_id: str
    product_id: str
    text: str

class ReviewOut(BaseModel):
    id: UUID
    customer_id: str
    product_id: str
    text: str
    sentiment: float | None = None
