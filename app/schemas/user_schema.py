# app/schemas/user_schema.py
from pydantic import BaseModel, EmailStr
from enum import Enum
import uuid

class Role(str, Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    telegram_id: str | None = None
    password: str
    role: Role = Role.student

class UserOut(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    email: EmailStr
    telegram_id: str | None = None
    role: Role

    model_config = {"from_attributes": True}  # pydantic v2 uchun orm_mode o'rniga

class Token(BaseModel):
    access_token: str
    token_type: str
