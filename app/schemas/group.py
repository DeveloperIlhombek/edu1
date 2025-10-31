from pydantic import BaseModel
from uuid import UUID

class GroupBase(BaseModel):
    name: str
    description: str | None = None

class GroupCreate(GroupBase):
    pass

class GroupResponse(GroupBase):
    id: UUID

    class Config:
        from_attributes = True  # Pydantic v2 uchun
