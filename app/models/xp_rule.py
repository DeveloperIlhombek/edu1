from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base import Base

class XPRule(Base):
    __tablename__ = "xp_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    action = Column(String, unique=True, nullable=False)   # masalan: "attendance_present", "attendance_absent", "payment_on_time"
    description = Column(String, nullable=True)
    xp_value = Column(Integer, nullable=False, default=0)
