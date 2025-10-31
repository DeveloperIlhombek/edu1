from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class XPTransactionBase(BaseModel):
    student_id: UUID
    rule_id: UUID | None = None
    amount: int
    reason: str

class XPTransactionCreate(XPTransactionBase):
    pass

class XPTransactionResponse(XPTransactionBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
