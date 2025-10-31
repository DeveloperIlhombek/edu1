from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.xp_transaction import XPTransaction
from app.schemas.xp_transaction_schema import XPTransactionCreate, XPTransactionResponse
from app.models.student import Student
from datetime import datetime
from app.core.security import get_current_user
from app.models.user import Role

router = APIRouter(prefix="/api/xp-transactions", tags=["XP Transactions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=XPTransactionResponse)
def create_xp_transaction(data: XPTransactionCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # Faqat admin yoki teacher XP qo‘sha oladi
    if current_user.role not in [Role.admin, Role.teacher]:
        raise HTTPException(status_code=403, detail="Faqat admin yoki o‘qituvchi XP qo‘sha oladi")

    student = db.query(Student).filter(Student.id == data.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student topilmadi")

    xp = XPTransaction(
        student_id=data.student_id,
        rule_id=data.rule_id,
        amount=data.amount,
        reason=data.reason,
        created_at=datetime.utcnow()
    )
    db.add(xp)
    db.commit()
    db.refresh(xp)
    return xp

@router.get("/student/{student_id}", response_model=list[XPTransactionResponse])
def get_student_xp_transactions(student_id: str, db: Session = Depends(get_db)):
    return db.query(XPTransaction).filter(XPTransaction.student_id == student_id).all()
