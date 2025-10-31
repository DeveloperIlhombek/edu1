# C:\Users\Victus_PC\Desktop\EduSystem backend\app\core\db_test.py
from fastapi import APIRouter
from sqlalchemy import text
from app.db.session import SessionLocal
from app.models.user import User
from app.core.config import settings
from app.core.security import create_access_token
from datetime import timedelta

router = APIRouter(prefix="/api/debug", tags=["Debug"])


@router.get("/db-status")
async def db_status():
    """Database connection va ma'lumotlarni tekshirish"""
    print("🔍 Database status tekshirilmoqda...")

    db = SessionLocal()
    try:
        # Connection test - text() funksiyasidan foydalanish
        db.execute(text("SELECT 1"))
        connection_ok = True
        print("✅ Database connection muvaffaqiyatli!")

        # User jadvalidagi ma'lumotlarni hisoblash
        user_count = db.query(User).count()
        telegram_users = db.query(User).filter(User.telegram_id.isnot(None)).count()

        # Bir nechta foydalanuvchilarni ko'rish
        recent_users = db.query(User).order_by(User.created_at.desc()).limit(5).all()

        users_info = []
        for user in recent_users:
            users_info.append({
                "id": str(user.id),
                "email": user.email,
                "telegram_id": user.telegram_id,
                "first_name": user.first_name,
                "role": user.role.value,
                "created_at": user.created_at.isoformat() if user.created_at else None
            })

        return {
            "database_connection": "OK",
            "total_users": user_count,
            "telegram_users": telegram_users,
            "recent_users": users_info,
            "config": {
                "database_url": settings.DATABASE_URL[:30] + "...",
                "jwt_algorithm": settings.JWT_ALGORITHM,
                "token_expire_minutes": settings.ACCESS_TOKEN_EXPIRE_MINUTES
            }
        }

    except Exception as e:
        print(f"❌ Database xatosi: {e}")
        return {
            "error": str(e),
            "database_connection": "ERROR"
        }
    finally:
        db.close()


@router.get("/test-token")
async def test_token():
    """Test token yaratish"""
    try:
        test_data = {
            "sub": "test@edusystem.com",
            "user_id": "test-user-id",
            "telegram_id": "123456789",
            "role": "student"
        }

        token = create_access_token(test_data)

        return {
            "success": True,
            "token": token,
            "test_data": test_data,
            "config": {
                "algorithm": settings.JWT_ALGORITHM,
                "expire_minutes": settings.ACCESS_TOKEN_EXPIRE_MINUTES
            }
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


@router.get("/create-test-user")
async def create_test_user():
    """Test foydalanuvchi yaratish"""
    db = SessionLocal()
    try:
        from uuid import uuid4
        import datetime

        test_user = User(
            first_name="Test",
            last_name="User",
            email=f"test_{uuid4()}@edusystem.com",
            password_hash="test_password_hash",
            role="student",
            telegram_id="123456789",
            created_at=datetime.datetime.now()
        )

        db.add(test_user)
        db.commit()
        db.refresh(test_user)

        return {
            "success": True,
            "user": {
                "id": str(test_user.id),
                "email": test_user.email,
                "telegram_id": test_user.telegram_id,
                "first_name": test_user.first_name,
                "last_name": test_user.last_name,
                "role": test_user.role.value,
                "created_at": test_user.created_at.isoformat() if test_user.created_at else None
            }
        }

    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "error": str(e)
        }
    finally:
        db.close()


@router.get("/users-list")
async def users_list():
    """Barcha foydalanuvchilarni ko'rish"""
    db = SessionLocal()
    try:
        users = db.query(User).all()

        users_list = []
        for user in users:
            users_list.append({
                "id": str(user.id),
                "email": user.email,
                "telegram_id": user.telegram_id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role.value,
                "created_at": user.created_at.isoformat() if user.created_at else None
            })

        return {
            "success": True,
            "total_users": len(users_list),
            "users": users_list
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    finally:
        db.close()