from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.attendance import Attendance, AttendanceStatus
from app.schemas.attendance import AttendanceCreate, AttendanceResponse
from app.core.permissions import teacher_required
from app.models.student import Student
from app.models.group import Group

router = APIRouter(prefix="/api/attendance", tags=["Attendance"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------
# 🟢 1. Darsga qatnashuv yozish
# -------------------------------
@router.post("/", response_model=AttendanceResponse, dependencies=[Depends(teacher_required)])
def create_attendance(record: AttendanceCreate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == record.student_id).first()
    group = db.query(Group).filter(Group.id == record.group_id).first()
    if not student or not group:
        raise HTTPException(status_code=404, detail="Talaba yoki guruh topilmadi")

    # existing check
    existing = db.query(Attendance).filter(
        Attendance.student_id == record.student_id,
        Attendance.date == record.date,
        Attendance.group_id == record.group_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bu talabaga bu kunda dars belgilang")

    # 1) attendance qo'shamiz
    new_record = Attendance(
        student_id=record.student_id,
        group_id=record.group_id,
        date=record.date,
        status=record.status,
        xp_applied="no"
    )
    db.add(new_record)

    try:
        # 2) commit qilmaymiz hali, balki flush qilamiz, shunda new_record.id bo'ladi
        db.flush()    # SQLAlchemy: yangi row DB-ga push qilinadi, lekin commit qilinmaydi

        # 3) XP manager chaqiriq — u db (flush qilingan) holatiga asoslanadi
        apply_xp_for_attendance(db, new_record)

        # 4) hammasi ok bo'lsa commit qilamiz
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"XP bilan bog'liq xatolik: {str(e)}")

    db.refresh(new_record)
    return new_record

# -------------------------------
# 🟡 2. Barcha attendance larni olish
# -------------------------------
@router.get("/", response_model=list[AttendanceResponse], dependencies=[Depends(teacher_required)])
def get_all_attendance(db: Session = Depends(get_db)):
    return db.query(Attendance).all()


# -------------------------------
# 🔵 3. Bitta talabaga oid attendance lar
# -------------------------------
@router.get("/student/{student_id}", response_model=list[AttendanceResponse], dependencies=[Depends(teacher_required)])
def get_attendance_by_student(student_id: str, db: Session = Depends(get_db)):
    return db.query(Attendance).filter(Attendance.student_id == student_id).all()
