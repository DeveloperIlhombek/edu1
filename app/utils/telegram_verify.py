# app/utils/telegram_verify.py
import hashlib
import hmac
import urllib.parse
from typing import Optional

BOT_TOKEN = "8497951622:AAG6Ry4k6sQoF0O2geWMyZsHPYxQRraW2y0"

def check_telegram_auth(init_data: str) -> Optional[dict]:
    """
    Telegram initData dan foydalanuvchini tekshiradi.
    HMAC orqali imzo tekshiriladi.
    """
    try:
        data_dict = dict(
            item.split("=") for item in init_data.split("&") if "=" in item
        )
        check_hash = data_dict.pop("hash", None)
        data_check_string = "\n".join(
            [f"{k}={v}" for k, v in sorted(data_dict.items())]
        )
        secret_key = hmac.new(
            key=b"WebAppData", msg=BOT_TOKEN.encode(), digestmod=hashlib.sha256
        ).digest()
        calculated_hash = hmac.new(
            key=secret_key, msg=data_check_string.encode(), digestmod=hashlib.sha256
        ).hexdigest()

        if calculated_hash != check_hash:
            return None
        return data_dict
    except Exception as e:
        print("❌ Telegram auth error:", e)
        return None
