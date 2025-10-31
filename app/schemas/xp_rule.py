from pydantic import BaseModel
from uuid import UUID

class XPRuleBase(BaseModel):
    action: str
    description: str | None = None
    xp_value: int

class XPRuleCreate(XPRuleBase):
    pass

class XPRuleUpdate(BaseModel):
    xp_value: int

class XPRuleResponse(XPRuleBase):
    id: UUID

    class Config:
        from_attributes = True
