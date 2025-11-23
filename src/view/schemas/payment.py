from pydantic import BaseModel
from src.models import PaymentMethod

class Payment(BaseModel):
    method: PaymentMethod