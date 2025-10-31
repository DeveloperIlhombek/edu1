from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.payment import Payment, PaymentStatus
from app.schemas.payment import PaymentCreate, PaymentResponse, PaymentUpdate
from app.core.permissions import admin_required
from app.core.security import get_current_user
from app.models.user import User
from app.models.student_xp import StudentXP  # XP integratsiya uchun
from app.models.xp_rule import XPRule  # XP qoida

router = APIRouter(prefix="/api/payments", tags=["Payments"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔹 To‘lov yaratish (faqat admin)
@router.post("/", response_model=PaymentResponse, dependencies=[Depends(admin_required)])
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    new_payment = Payment(**payment.dict())
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment


# 🔹 Barcha to‘lovlarni olish (faqat admin)
@router.get("/", response_model=list[PaymentResponse], dependencies=[Depends(admin_required)])
def get_payments(db: Session = Depends(get_db)):
    return db.query(Payment).all()


# 🔹 Talabaning barcha to‘lovlari
@router.get("/student/{student_id}", response_model=list[PaymentResponse])
def get_student_payments(student_id: str, db: Session = Depends(get_db)):
    payments = db.query(Payment).filter(Payment.student_id == student_id).all()
    if not payments:
        raise HTTPException(status_code=404, detail="Ushbu talabaga to‘lovlar topilmadi.")
    return payments



@router.put("/{payment_id}", response_model=PaymentResponse, dependencies=[Depends(admin_required)])
def update_payment(payment_id: str, update_data: PaymentUpdate, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="To‘lov topilmadi.")

    payment.status = update_data.status
    db.commit()
    db.refresh(payment)

    # 🟢 XP avtomatik qo‘shish — faqat "paid" bo‘lsa
    if payment.status == PaymentStatus.paid:
        rule = db.query(XpRule).filter(XpRule.action == "on_time_payment").first()
        if rule:
            # Dublikatsiyani oldini olish
            existing_xp = db.query(StudentXP).filter(
                StudentXP.student_id == payment.student_id,
                StudentXP.rule_id == rule.id
            ).first()
            if not existing_xp:
                student_xp = StudentXP(
                    student_id=payment.student_id,
                    rule_id=rule.id,
                    earned_xp=rule.xp_value
                )
                db.add(student_xp)
                db.commit()

    return payment
# 🔹 To‘lovni o‘chirish
@router.delete("/{payment_id}", dependencies=[Depends(admin_required)])
def delete_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="To‘lov topilmadi.")
    db.delete(payment)
    db.commit()
    return {"message": "To‘lov muvaffaqiyatli o‘chirildi ✅"}
