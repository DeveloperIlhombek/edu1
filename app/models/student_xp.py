from sqlalchemy import Column, ForeignKey, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.db.base import Base


class StudentXP(Base):
    __tablename__ = "student_xp"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    rule_id = Column(UUID(as_uuid=True), ForeignKey("xp_rules.id"), nullable=False)
    earned_xp = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", backref="xp_records")
    rule = relationship("XPRule", backref="xp_records")
