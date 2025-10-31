from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID

class AnswerBase(BaseModel):
    text: str
    is_correct: bool

class QuestionBase(BaseModel):
    text: str
    answers: List[AnswerBase]

class TestCreate(BaseModel):
    title: str
    subject_id: UUID
    questions: List[QuestionBase]

class TestUpdate(BaseModel):
    title: Optional[str] = None
    subject_id: Optional[UUID] = None

class TestResponse(BaseModel):
    id: UUID
    title: str
    subject_id: UUID
    created_by: UUID

    class Config:
        from_attributes = True
