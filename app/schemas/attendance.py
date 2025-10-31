from pydantic import BaseModel
from datetime import date
from uuid import UUID
from enum import Enum

class AttendanceStatus(str, Enum):
    present = "present"
    absent = "absent"
    late = "late"

# ------------------------
# CREATE uchun schema
# ------------------------
class AttendanceCreate(BaseModel):
    student_id: UUID
    group_id: UUID
    date: date
    status: AttendanceStatus

# ------------------------
# RESPONSE uchun schema
# ------------------------
class AttendanceResponse(BaseModel):
    id: UUID
    student_id: UUID
    group_id: UUID
    date: date
    status: AttendanceStatus
    xp_applied: str  # "yes" yoki "no"

    class Config:
        from_attributes = True
