from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from ...database import Base

class PointType(enum.Enum):
    check_in = "check_in"
    check_out = "check_out"

class EmployeePoint(Base):
    __tablename__ = "employee_points"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    point_type = Column(Enum(PointType), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    employee = relationship("Employee", back_populates="points")