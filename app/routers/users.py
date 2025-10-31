# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import decode_access_token
from typing import Optional

router = APIRouter(prefix="/api/users", tags=["Users"])

# Session helper
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Current user helper
def get_current_user(token: str, db: Session):
    payload = decode_access_token(token)
    email: Optional[str] = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token noto‘g‘ri")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
    return user

# Get current user info
@router.get("/me")
def read_current_user(token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "role": user.role,
        "created_at": user.created_at
    }

# Update user info
from pydantic import BaseModel

class UpdateUser(BaseModel):
    first_name: str
    last_name: str

@router.put("/update")
def update_user(data: UpdateUser, token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    user.first_name = data.first_name
    user.last_name = data.last_name
    db.commit()
    db.refresh(user)
    return {"message": "Profil yangilandi", "user": user.email}
