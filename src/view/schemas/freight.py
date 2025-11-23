from pydantic import BaseModel, Field

from src.domain.entities.order import FreightTypeEnum

class FreightCalcRequest(BaseModel):
    origin_zip: str = Field(min_length=8, max_length=9)
    destination_zip: str = Field(min_length=8, max_length=9)
    weight: float = Field(..., gt=0)
    freight_type: FreightTypeEnum


class FreightCalcResponse(BaseModel):
    distance_km: float
    value: float
