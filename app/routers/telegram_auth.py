# C:\Users\Victus_PC\Desktop\EduSystem backend\app\core\telegram_auth.py
from fastapi import APIRouter, HTTPException, Request
from app.models.user import User, Role
from app.db.session import SessionLocal
from datetime import timedelta
from app.core.security import create_access_token
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/telegram", tags=["Telegram Auth"])


@router.post("/verify")
async def telegram_verify(request: Request):
    print("🚀 /api/telegram/verify endpointiga so'rov keldi!")

    try:
        # JSON ma'lumotlarni olish
        data = await request.json()
        print(f"✅ Qabul qilingan ma'lumotlar: {data}")

    except Exception as e:
        print(f"❌ JSON o'qish xatosi: {e}")
        return {"error": "Invalid JSON", "details": str(e)}

    # Majburiy maydonlarni tekshirish
    required_fields = ['id', 'hash', 'auth_date']
    for field in required_fields:
        if field not in data:
            print(f"❌ Majburiy maydon yo'q: {field}")
            return {"error": f"Missing required field: {field}"}

    telegram_id = data.get("id")
    first_name = data.get("first_name", "Telegram")
    last_name = data.get("last_name", "User")
    username = data.get("username", "")

    print(f"👤 Telegram ID: {telegram_id}")

    db = SessionLocal()

    try:
        # 1. Telegram ID bo'yicha qidirish
        user = db.query(User).filter(User.telegram_id == str(telegram_id)).first()

        # 2. Agar topilmasa, email bo'yicha qidirish
        if not user:
            user_email = f"telegram_{telegram_id}@edusystem.com"
            user = db.query(User).filter(User.email == user_email).first()

        # 3. Agar hali ham topilmasa, yangi foydalanuvchi yaratish
        if not user:
            user = User(
                first_name=first_name,
                last_name=last_name,
                email=f"telegram_{telegram_id}@edusystem.com",
                password_hash="telegram_auth_2024",
                role=Role.student,
                telegram_id=str(telegram_id),
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"✅ YANGI FOYDALANUVCHI YARATILDI: {user.id}")
        else:
            print(f"👤 MAVJUD FOYDALANUVCHI TOPILDI: {user.email}")

        # Token yaratish
        token_data = {"sub": user.email, "user_id": str(user.id)}
        token = create_access_token(token_data, expires_delta=timedelta(days=7))

        response_data = {
            "success": True,
            "message": "Telegram authentication successful",
            "user": {
                "id": str(user.id),
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "role": user.role.value,
                "telegram_id": user.telegram_id,
            },
            "access_token": token,
            "token_type": "bearer"
        }

        print(f"📤 Javob yuborilmoqda: {response_data}")
        return response_data

    except Exception as e:
        print(f"❌ DATABASE XATOSI: {e}")
        db.rollback()
        return {"error": "Database error", "details": str(e)}
    finally:
        db.close()
        print("🔚 Database connection yopildi")