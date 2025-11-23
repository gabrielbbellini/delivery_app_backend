import enum
from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from ...database import Base

class FreightTypeEnum(str, enum.Enum):
    normal = "normal"
    sedex = "sedex"
    sedex10 = "sedex10"

class PaymentMethod(str, enum.Enum):
    pix = "pix"
    credit_card = "credit_card"
    debit_card = "debit_card"

class OrderStatus(enum.Enum):
    confirmed = "confirmed"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    origin_zip = Column(String, nullable=False)
    destination_zip = Column(String, nullable=False)
    weight = Column(Float, nullable=False)
    freight_type = Column(Enum(FreightTypeEnum), nullable=False)
    distance_km = Column(Float, nullable=False)
    freight_value = Column(Float, nullable=False)

    payment_method = Column(Enum(PaymentMethod), nullable=True)
    status = Column(Enum(OrderStatus))

    created_at = Column(DateTime, default=datetime.utcnow)
    paid_at = Column(DateTime, nullable=True)
    shipped_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="orders")