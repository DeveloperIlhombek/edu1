from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.enrollment import Enrollment
from app.schemas.enrollment import EnrollmentCreate, EnrollmentResponse
from app.core.permissions import admin_required

router = APIRouter(prefix="/api/enrollments", tags=["Enrollments"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=EnrollmentResponse, dependencies=[Depends(admin_required)])
def create_enrollment(enrollment: EnrollmentCreate, db: Session = Depends(get_db)):
    new_enrollment = Enrollment(**enrollment.dict())
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    return new_enrollment

@router.get("/", response_model=list[EnrollmentResponse])
def get_enrollments(db: Session = Depends(get_db)):
    return db.query(Enrollment).all()

@router.get("/student/{student_id}", response_model=list[EnrollmentResponse])
def get_student_enrollments(student_id: str, db: Session = Depends(get_db)):
    return db.query(Enrollment).filter(Enrollment.student_id == student_id).all()

@router.get("/group/{group_id}", response_model=list[EnrollmentResponse])
def get_group_enrollments(group_id: str, db: Session = Depends(get_db)):
    return db.query(Enrollment).filter(Enrollment.group_id == group_id).all()
