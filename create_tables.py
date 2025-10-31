# create_tables.py
"""
Ishlatish:
  - Virtualenv faollashtirilgan holda loyiha ildizidan ishga tushiring:
      python create_tables.py

Bu skript:
  - barcha model fayllarini import qilib, SQLAlchemy Base.metadata.create_all() orqali
    jadvallarni yaratadi (agar ular mavjud bo'lmasa).
  - bajarilgandan so'ng mavjud jadvallar ro'yxatini chiqaradi.
"""

import sys
import traceback
from sqlalchemy import inspect
from app.db.base import Base
from app.db.session import engine

# --- MUHIM: barcha model modullarini shu yerda import qiling ---
#  Agar yangi model qo'shsangiz, shu yerga qo'shishni unutmang.
#  Misol: from app.models.teacher import Teacher
try:
    # import qilish orqali modellarning metadata ga yozilishi ta'minlanadi
    from app.models.user import User
    from app.models.student import Student
    from app.models.teacher import Teacher
    from app.models.group import Group
    from app.models.enrollment import Enrollment
    from app.models.subject import Subject
    from app.models.attendance import Attendance
    from app.models.xp_rule import XPRule
    from app.models.student_xp import StudentXP
    from app.models.test import Test
    from app.models.result import Result
    from app.models.xp_transaction import XPTransaction
    from app.models.payment import Payment

except Exception:
    print("⚠️ Model importida xatolik yuz berdi:")
    traceback.print_exc()
    sys.exit(1)

def main():
    try:
        print("⏳ Jadval(lar) yaratish jarayoni boshlandi...")
        Base.metadata.create_all(bind=engine)
        print("✅ Barcha jadvallar yaratildi (yoki allaqachon mavjud edi).")

        # Jadval nomlarini ko'rsatish
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        if tables:
            print("\n📋 Bazadagi jadvallar:")
            for t in tables:
                print("  -", t)
        else:
            print("⚠️ Diqqat: bazada hali birorta jadval topilmadi.")
    except Exception:
        print("❌ Jadval yaratishda xatolik yuz berdi:")
        traceback.print_exc()
        sys.exit(2)

if __name__ == "__main__":
    main()
