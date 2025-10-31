from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class StudentXPBase(BaseModel):
    student_id: UUID
    rule_id: UUID
    xp_amount: int

class StudentXPCreate(StudentXPBase):
    pass

class StudentXPResponse(StudentXPBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
