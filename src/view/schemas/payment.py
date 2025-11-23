from pydantic import BaseModel
from src.domain.entities.order import PaymentMethod

class Payment(BaseModel):
    method: PaymentMethod