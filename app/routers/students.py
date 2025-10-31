from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentResponse
from app.core.permissions import admin_required  # 🟢 yangi
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/students", tags=["Students"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🟢 faqat ADMIN student qo'sha oladi
@router.post("/", response_model=StudentResponse)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    new_student = Student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


# 🟡 barcha userlar (admin, teacher, student) o‘qiy oladi
@router.get("/", response_model=list[StudentResponse])
def get_students(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Student).all()


# 🟡 barcha userlar o‘zini yoki istalgan studentni ko‘rishi mumkin (keyinchalik cheklaymiz)
@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student
