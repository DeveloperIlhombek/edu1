from fastapi import Depends, HTTPException, status
from app.core.security import get_current_user
from app.models.user import User, Role

def admin_required(current_user: User = Depends(get_current_user)):
    if current_user.role != Role.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu amal faqat admin uchun ruxsat etilgan!"
        )
    return current_user

def teacher_required(current_user: User = Depends(get_current_user)):
    if current_user.role != Role.teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu amal faqat o‘qituvchi uchun ruxsat etilgan!"
        )
    return current_user

def student_required(current_user: User = Depends(get_current_user)):
    if current_user.role != Role.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu amal faqat talaba uchun ruxsat etilgan!"
        )
    return current_user
