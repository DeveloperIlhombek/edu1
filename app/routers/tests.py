from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime

from app.db.session import SessionLocal
from app.models.test import Test, Question, Answer
from app.models.teacher import Teacher
from app.schemas.test_schema import TestCreate, TestResponse, TestUpdate
from app.core.security import get_current_user
from app.models.user import Role, User

router = APIRouter(prefix="/api/tests", tags=["Tests"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🧠 1️⃣ Test yaratish (faqat teacher yoki admin)
@router.post("/", response_model=TestResponse)
def create_test(
    test_data: TestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Faqat teacher yoki admin test yarata oladi
    if current_user.role not in [Role.teacher, Role.admin]:
        raise HTTPException(status_code=403, detail="Faqat o‘qituvchi test yaratishi mumkin")

    # Teacher jadvalidan mos keladigan o‘qituvchini topamiz
    teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Siz o‘qituvchi sifatida ro‘yxatdan o‘tmagansiz")

    new_test = Test(
        title=test_data.title,
        subject_id=test_data.subject_id,
        created_by=teacher.id,
        created_at=datetime.utcnow()
    )

    db.add(new_test)
    db.flush()  # test.id ni olish uchun

    # Savollarni qo‘shamiz
    for q in test_data.questions:
        question = Question(
            text=q.text,
            test_id=new_test.id
        )
        db.add(question)
        db.flush()

        for a in q.answers:
            answer = Answer(
                text=a.text,
                is_correct=a.is_correct,
                question_id=question.id
            )
            db.add(answer)

    db.commit()
    db.refresh(new_test)
    return new_test


# 📋 2️⃣ Barcha testlarni ko‘rish (teacher va admin)
@router.get("/", response_model=list[TestResponse])
def get_tests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == Role.teacher:
        teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
        return db.query(Test).filter(Test.created_by == teacher.id).all()

    elif current_user.role == Role.admin:
        return db.query(Test).all()

    else:
        raise HTTPException(status_code=403, detail="Sizda testlarni ko‘rish uchun ruxsat yo‘q")


# 🔍 3️⃣ Bitta testni olish
@router.get("/{test_id}", response_model=TestResponse)
def get_test(test_id: UUID, db: Session = Depends(get_db)):
    test = db.query(Test).filter(Test.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test topilmadi")
    return test


# ✏️ 4️⃣ Testni tahrirlash (faqat o‘z testini teacher tahrirlay oladi)
@router.put("/{test_id}", response_model=TestResponse)
def update_test(
    test_id: UUID,
    test_data: TestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    test = db.query(Test).filter(Test.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test topilmadi")

    # Teacher o‘z testini yoki admin hammasini tahrirlay oladi
    teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
    if current_user.role == Role.teacher and test.created_by != teacher.id:
        raise HTTPException(status_code=403, detail="Bu testni tahrirlash huquqingiz yo‘q")

    test.title = test_data.title or test.title
    test.subject_id = test_data.subject_id or test.subject_id
    db.commit()
    db.refresh(test)
    return test


# 🗑️ 5️⃣ Testni o‘chirish (faqat o‘z testini teacher yoki admin)
@router.delete("/{test_id}")
def delete_test(
    test_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    test = db.query(Test).filter(Test.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test topilmadi")

    teacher = db.query(Teacher).filter(Teacher.user_id == current_user.id).first()
    if current_user.role == Role.teacher and test.created_by != teacher.id:
        raise HTTPException(status_code=403, detail="Bu testni o‘chirish huquqingiz yo‘q")

    db.delete(test)
    db.commit()
    return {"message": "Test muvaffaqiyatli o‘chirildi ✅"}
