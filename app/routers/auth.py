from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import SessionLocal
from app.models.user import User,Role
from app.schemas.user_schema import UserCreate
from app.core.security import get_password_hash, verify_password, create_access_token,decode_access_token

router = APIRouter(prefix="/api/auth", tags=["Auth"])

# Database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------
# Register Endpoint
# -----------------------
class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    role: str = "student"


@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Bu email allaqachon mavjud")
    if len(user_data.password) > 72:
        raise HTTPException(
            status_code=400,
            detail="Parol uzunligi 72 belgidan oshmasligi kerak."
        )
    # app/routers/auth.py (register ichida, hashingdan oldin)
    print("DEBUG password repr:", repr(user_data.password))
    print("DEBUG type:", type(user_data.password))
    print("DEBUG len(chars):", len(user_data.password))
    print("DEBUG len(bytes utf-8):", len(user_data.password.encode("utf-8")))

    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        password_hash=hashed_password,
        role=user_data.role or Role.student
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Foydalanuvchi muvaffaqiyatli ro‘yxatdan o‘tkazildi ✅",
        "id": str(new_user.id),
        "email": new_user.email,
        "role": new_user.role
    }
# -----------------------
# Login Endpoint
# -----------------------
class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if not existing_user or not verify_password(user.password, existing_user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email yoki parol noto‘g‘ri")

    token = create_access_token({"sub": existing_user.email})
    return {"access_token": token, "token_type": "bearer"}
