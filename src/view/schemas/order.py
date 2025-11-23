from pydantic import BaseModel, Field
from typing import Optional

from src.domain.entities.order import FreightTypeEnum

class OrderCreate(BaseModel):
    origin_zip: str = Field(min_length=8, max_length=9)
    destination_zip: str = Field(min_length=8, max_length=9)
    weight: float = Field(..., gt=0)
    freight_type: FreightTypeEnum


class OrderOut(BaseModel):
    id: int
    origin_zip: str
    destination_zip: str
    distance_km: float
    weight: float
    freight_type: FreightTypeEnum
    freight_value: float
    payment_method: Optional[str]

    class Config:
        from_attributes = True


class OrderListOut(BaseModel):
    id: int
    origin_zip: str
    destination_zip: str
    freight_value: float
    weight: float
    freight_type: FreightTypeEnum

    class Config:
        from_attributes = True


class OrderDeliveryInfoOut(BaseModel):
    order_id: int
    origin_zip: str
    destination_zip: str
    sender_name: str
    sender_phone: Optional[str]


class OrdersTodayResponse(BaseModel):
    total_orders: int
