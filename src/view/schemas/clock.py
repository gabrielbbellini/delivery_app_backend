from pydantic import BaseModel
from typing import Optional

class ClockInRequest(BaseModel):
    timestamp: Optional[str]


class ClockOutRequest(BaseModel):
    timestamp: Optional[str]


class ClockRecordOut(BaseModel):
    id: int
    employee_id: int
    timestamp: str
    type: str

    class Config:
        from_attributes = True
