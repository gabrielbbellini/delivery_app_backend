from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from ...models import UserRole

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