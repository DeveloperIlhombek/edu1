# app/models/subject.py
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base import Base

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

    # agar fanni bevosita teacher bilan bog'lamoqchi bo'lsangiz:
    # teacher_id = Column(UUID(as_uuid=True), ForeignKey("teachers.id"), nullable=True)
    # teacher = relationship("Teacher", back_populates="subjects")
