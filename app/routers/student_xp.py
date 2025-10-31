from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.student_xp import StudentXP
from app.models.xp_rule import XPRule
from app.models.student import Student
from app.schemas.student_xp import StudentXPCreate, StudentXPResponse
from app.core.permissions import teacher_required, admin_required

router = APIRouter(prefix="/api/student-xp", tags=["Student XP"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🟢 XP qo‘shish (faqat teacher yoki admin)
@router.post("/", response_model=StudentXPResponse, dependencies=[Depends(teacher_required)])
def add_xp(data: StudentXPCreate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == data.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Talaba topilmadi.")

    rule = db.query(XPRule).filter(XPRule.id == data.rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="XP qoidasini topib bo‘lmadi.")

    # XP yozuvini yaratish
    new_xp = StudentXP(
        student_id=data.student_id,
        rule_id=data.rule_id,
        xp_amount=data.xp_amount or rule.xp_value
    )
    db.add(new_xp)
    db.commit()
    db.refresh(new_xp)
    return new_xp

# 📋 Talabaning barcha XP yozuvlari
@router.get("/student/{student_id}", response_model=list[StudentXPResponse])
def get_student_xp(student_id: str, db: Session = Depends(get_db)):
    return db.query(StudentXP).filter(StudentXP.student_id == student_id).all()

# 💎 XP umumiy hisobini chiqarish
@router.get("/student/{student_id}/total")
def get_total_xp(student_id: str, db: Session = Depends(get_db)):
    total = db.query(StudentXP).filter(StudentXP.student_id == student_id).all()
    xp_sum = sum(x.xp_amount for x in total)
    return {"student_id": student_id, "total_xp": xp_sum}
