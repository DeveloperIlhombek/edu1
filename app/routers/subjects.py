# app/routers/subjects.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.subject import Subject
from app.schemas.subject import SubjectCreate, SubjectResponse, SubjectUpdate
from typing import List

# ruxsat uchun: admin yoki teacher yaratishi mumkin (qo'shimcha)
from app.core.permissions import admin_required, teacher_required
from app.core.security import get_current_user

router = APIRouter(prefix="/api/subjects", tags=["Subjects"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create subject: faqat admin yoki teacher yaratishi mumkin.
@router.post("/", response_model=SubjectResponse,
             status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(admin_required)])  # agar teacher ham yaratishiga ruxsat berilsa, o'zgartiring
def create_subject(subject: SubjectCreate, db: Session = Depends(get_db)):
    # nom unique ekanligini tekshirish
    existing = db.query(Subject).filter(Subject.name.ilike(subject.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bu nomdagi fan allaqachon mavjud.")
    new = Subject(**subject.model_dump())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new

# List all subjects — hamma ko'ra oladi
@router.get("/", response_model=List[SubjectResponse])
def get_subjects(db: Session = Depends(get_db)):
    return db.query(Subject).all()

# Get single subject
@router.get("/{subject_id}", response_model=SubjectResponse)
def get_subject(subject_id: str, db: Session = Depends(get_db)):
    s = db.query(Subject).filter(Subject.id == subject_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Subject not found")
    return s

# Update subject (admin required)
@router.put("/{subject_id}", response_model=SubjectResponse, dependencies=[Depends(admin_required)])
def update_subject(subject_id: str, payload: SubjectUpdate, db: Session = Depends(get_db)):
    s = db.query(Subject).filter(Subject.id == subject_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Subject not found")
    data = payload.model_dump(exclude_none=True)
    for k, v in data.items():
        setattr(s, k, v)
    db.add(s)
    db.commit()
    db.refresh(s)
    return s

# Delete subject (admin required)
@router.delete("/{subject_id}", dependencies=[Depends(admin_required)])
def delete_subject(subject_id: str, db: Session = Depends(get_db)):
    s = db.query(Subject).filter(Subject.id == subject_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Subject not found")
    db.delete(s)
    db.commit()
    return {"message": "Subject deleted successfully"}
