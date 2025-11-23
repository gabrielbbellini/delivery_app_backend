import enum
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base

class UserRole(enum.Enum):
    user = "user"
    manager = "manager"
    deliverer = "deliverer"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    orders = relationship("Order", back_populates="user")