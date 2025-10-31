from pydantic import BaseModel
from uuid import UUID
from datetime import date
from enum import Enum


class PaymentStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    late = "late"


class PaymentBase(BaseModel):
    student_id: UUID
    amount: float
    month: str
    payment_date: date | None = None
    status: PaymentStatus = PaymentStatus.pending


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    status: PaymentStatus


class PaymentResponse(PaymentBase):
    id: UUID

    class Config:
        from_attributes = True
