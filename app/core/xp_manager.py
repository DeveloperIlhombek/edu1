# app/core/xp_manager.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date
from app.models.xp_rule import XPRule
from app.models.student_xp import StudentXP
from app.models.attendance import Attendance
from app.models.student import Student

def apply_xp_for_attendance(db: Session, attendance: Attendance) -> None:
    """
    attendance: Attendance SQLAlchemy instance (bitta saqlangan record, db session ichida yoki sessiya bilan)
    db: aktyor session (kengaytirilgan, commit/rollback bizda)
    Natija: agar mos qoida topilsa va shu kundagi yozuv hali qo'llanilmagan bo'lsa - StudentXP yoziladi va attendance.xp_applied='yes'
    """
    # 1) action string
    action = f"attendance_{attendance.status.value}"  # e.g. attendance_present, attendance_late, attendance_absent

    # 2) topish
    xp_rule = db.query(XPRule).filter(XPRule.action == action).first()
    if not xp_rule:
        # Hech qanday qoida topilmadi — hech narsa qilmaymiz, lekin attendance saqlanadi.
        # (yoki bu yerda logger qoying)
        return

    # 3) idempotent tekshiruv:
    # Agar StudentXP jadvalida shu student + shu rule + shu kun uchun yozuv bo'lsa, qo'shmaymiz.
    # Agar StudentXP modelida attendance_id mavjud bo'lsa, shundan tekshirish aniq bo'ladi.
    exists_q = db.query(StudentXP).filter(
        StudentXP.student_id == attendance.student_id,
        StudentXP.rule_id == xp_rule.id,
        # created_at va attendance.date tengligini tekshiramiz:
        func.date(StudentXP.created_at) == attendance.date
    ).limit(1).first()

    if exists_q:
        # Allaqachon shu kun uchun shu qoida bo'yicha XP berilgan
        # biz attendance.xp_applied ni ham update qilamiz, lekin agar u allaqachon "yes" bo'lsa — qilmaymiz
        if getattr(attendance, "xp_applied", None) != "yes":
            attendance.xp_applied = "yes"
            db.add(attendance)
            # caller ga commit qilishni bizni router-da qilamiz (yoki bu funksiya ichida commit qilamiz)
        return

    # 4) yo'q bo'lsa — yaratamiz
    xp_entry = StudentXP(
        student_id=attendance.student_id,
        rule_id=xp_rule.id,
        xp_amount=xp_rule.xp_value
    )
    # Agar StudentXP modelida attendance_id mavjud bo'lsa:
    if hasattr(xp_entry, "attendance_id"):
        xp_entry.attendance_id = attendance.id

    db.add(xp_entry)

    # 5) attendance ni belgilang
    attendance.xp_applied = "yes"
    db.add(attendance)

    # NOTE: Bu funksiya DB commit/rollback qilishi mumkin yoki caller-ga qoldirishi mumkin.
    # Bizni routerda bitta commit qilishni tavsiya qilamiz.
    return
