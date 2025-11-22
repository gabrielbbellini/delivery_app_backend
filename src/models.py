from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .database import Base

# Enums
class FreightTypeEnum(str, enum.Enum):
    normal = "normal"
    sedex = "sedex"
    sedex10 = "sedex10"

class UserRole(enum.Enum):
    user = "user"
    manager = "manager"
    deliverer = "deliverer"

class JobRole(enum.Enum):
    manager = "manager"
    deliverer = "deliverer"

class OrderStatus(enum.Enum):
    confirmed = "confirmed"

class PaymentMethod(str, enum.Enum):
    pix = "pix"
    credit_card = "credit_card"
    debit_card = "debit_card"

class PointType(enum.Enum):
    check_in = "check_in"
    check_out = "check_out"

# USER
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    orders = relationship("Order", back_populates="user")


# EMPLOYEES (MANAGERS & DELIVERERS)
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    job_role = Column(Enum(JobRole), nullable=False)
    registry_number = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=True)

    points = relationship("EmployeePoint", back_populates="employee")


# ORDERS
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

    payment_method = Column(String, nullable=True)
    status = Column(Enum(OrderStatus))

    created_at = Column(DateTime, default=datetime.utcnow)
    paid_at = Column(DateTime, nullable=True)
    shipped_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="orders")

# EMPLOYEE CHECK-IN / CHECK-OUT
class EmployeePoint(Base):
    __tablename__ = "employee_points"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    point_type = Column(Enum(PointType), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    employee = relationship("Employee", back_populates="points")