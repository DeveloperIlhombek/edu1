# app/schemas/subject.py
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional

class SubjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None

class SubjectCreate(SubjectBase):
    pass

class SubjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None

class SubjectResponse(SubjectBase):
    id: UUID

    class Config:
        from_attributes = True   # pydantic v2: This is like orm_mode
