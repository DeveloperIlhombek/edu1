from pydantic import BaseModel
from datetime import date
from uuid import UUID

class EnrollmentBase(BaseModel):
    student_id: UUID
    group_id: UUID
    subject_id: UUID | None = None

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentResponse(EnrollmentBase):
    id: UUID
    enrolled_date: date

    class Config:
        from_attributes = True
