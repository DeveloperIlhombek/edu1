from pydantic import BaseModel
from datetime import date
from uuid import UUID
from typing import Optional

class StudentBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: Optional[date] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

class StudentCreate(StudentBase):
    user_id: UUID

class StudentResponse(StudentBase):
    id: UUID
    user_id: UUID

    class Config:
        orm_mode = True
