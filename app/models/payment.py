from sqlalchemy import Column, String, Date, Float, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from datetime import datetime
from app.db.base import Base


class PaymentStatus(str, enum.Enum):
    pending = "pending"
    paid = "paid"
    late = "late"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    amount = Column(Float, nullable=False)
    month = Column(String, nullable=False)  # masalan: "October 2025"
    payment_date = Column(Date, default=datetime.utcnow)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.pending)
    created_at = Column(Date, default=datetime.utcnow)

    # Aloqa
    student = relationship("Student", backref="payments")
