import enum
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from src.database import Base

class JobRole(enum.Enum):
    manager = "manager"
    deliverer = "deliverer"
    
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    job_role = Column(Enum(JobRole), nullable=False)
    registry_number = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=True)

    points = relationship("EmployeePoint", back_populates="employee")