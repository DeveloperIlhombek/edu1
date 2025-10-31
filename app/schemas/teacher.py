from pydantic import BaseModel
from datetime import date
from uuid import UUID

class TeacherBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date | None = None
    phone_number: str | None = None
    address: str | None = None
    specialization: str | None = None

class TeacherCreate(TeacherBase):
    user_id: UUID

class TeacherResponse(TeacherBase):
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True  # pydantic v2 uchun
