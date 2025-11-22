from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from .models import PaymentMethod, UserRole, FreightTypeEnum


# USER / EMPLOYEE SCHEMAS
class UserCreate(BaseModel):
    name: str = Field(..., min_length=3)
    phone: Optional[str]
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: UserRole = UserRole.user
    registry: Optional[str]


class UserUpdate(BaseModel):
    name: Optional[str]
    phone: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]


class UserOut(BaseModel):
    id: int
    name: str
    phone: Optional[str]
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True


# LOGIN
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# FREIGHT CALCULATION SCHEMAS
class FreightCalcRequest(BaseModel):
    origin_zip: str = Field(min_length=8, max_length=9)
    destination_zip: str = Field(min_length=8, max_length=9)
    weight: float = Field(..., gt=0)
    freight_type: FreightTypeEnum


class FreightCalcResponse(BaseModel):
    distance_km: float
    value: float


# ORDER SCHEMAS
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

# USER PAYMENT
class Payment(BaseModel):
    method: PaymentMethod


# EMPLOYEE: CLOCK IN/OUT SCHEMAS
class ClockInRequest(BaseModel):
    timestamp: Optional[str]  # Filled automatically


class ClockOutRequest(BaseModel):
    timestamp: Optional[str]


class ClockRecordOut(BaseModel):
    id: int
    employee_id: int
    timestamp: str
    type: str

    class Config:
        from_attributes = True


# MANAGER METRICS
class OrdersTodayResponse(BaseModel):
    total_orders: int
