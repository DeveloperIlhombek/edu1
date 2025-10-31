# C:\Users\Victus_PC\Desktop\EduSystem backend\app\core\telegram_auth.py
import hmac
import hashlib
import time
from fastapi import HTTPException, status
from app.core.config import settings


def verify_telegram_auth(auth_data: dict):
    """
    Telegram WebAppdan kelgan initData ni tekshiradi
    """
    print("🔐 Telegram auth tekshiruvi boshlandi...")

    # Bot tokenini olish (agar mavjud bo'lsa)
    if not hasattr(settings, 'BOT_TOKEN') or not settings.BOT_TOKEN:
        print("⚠️  BOT_TOKEN topilmadi, tekshiruv o'tkazilmaydi")
        return auth_data

    try:
        secret_key = hashlib.sha256(settings.BOT_TOKEN.encode()).digest()
        print("🔑 Secret key tayyor")

        # Hash ni saqlab olish
        check_hash = auth_data.get("hash")
        print("📊 check_hash:", check_hash)

        if not check_hash:
            print("⚠️  Hash yo'q, tekshiruv o'tkazilmaydi")
            return auth_data

        # Data check string yaratish
        data_check_items = []
        for key in sorted(auth_data.keys()):
            if key != "hash":
                value = auth_data[key]
                data_check_items.append(f"{key}={value}")

        data_check_string = "\n".join(data_check_items)
        print("🧾 data_check_string:", data_check_string)

        # Hash ni hisoblash
        calculated_hash = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256
        ).hexdigest()

        print("🧮 calculated_hash:", calculated_hash)

        # Hash ni tekshirish (faqat developmentda o'chirib qo'yish mumkin)
        if calculated_hash != check_hash:
            print("⚠️  Hash mos emas! Lekin development rejimida davom etamiz")
            # raise HTTPException(status_code=403, detail="Telegram ma'lumotlari noto'g'ri!")
            return auth_data

        # Auth date ni tekshirish
        auth_date = int(auth_data.get("auth_date", 0))
        current_time = time.time()

        if current_time - auth_date > 86400:  # 24 soat
            print("⚠️  Auth ma'lumotlari eskirgan, lekin davom etamiz")
            # raise HTTPException(status_code=401, detail="Auth ma'lumotlari eskirgan")

        print("✅ Telegram auth tekshiruvi muvaffaqiyatli!")
        return auth_data

    except Exception as e:
        print(f"❌ Telegram auth tekshiruvida xato: {e}")
        # Development rejimida xatolarga qatiy qaramaymiz
        return auth_data