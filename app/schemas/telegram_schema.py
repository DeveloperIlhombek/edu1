# C:\Users\Victus_PC\Desktop\EduSystem backend\app\schemas\telegram_schema.py
from pydantic import BaseModel
from typing import Optional

class TelegramAuthData(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] = ""
    username: Optional[str] = ""
    auth_date: int
    hash: str