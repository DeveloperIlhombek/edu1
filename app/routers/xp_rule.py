from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.xp_rule import XPRule
from app.schemas.xp_rule import XPRuleCreate, XPRuleResponse, XPRuleUpdate
from app.core.permissions import admin_required

router = APIRouter(prefix="/api/xp-rules", tags=["XP Rules"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ 1. Admin XP qoidasini qo‘shadi
@router.post("/", response_model=XPRuleResponse, dependencies=[Depends(admin_required)])
def create_xp_rule(rule: XPRuleCreate, db: Session = Depends(get_db)):
    existing = db.query(XPRule).filter(XPRule.action == rule.action).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bu action uchun XP qoidasi allaqachon mavjud.")
    new_rule = XPRule(**rule.dict())
    db.add(new_rule)
    db.commit()
    db.refresh(new_rule)
    return new_rule

# 📋 2. Barcha XP qoidalarini olish
@router.get("/", response_model=list[XPRuleResponse])
def get_xp_rules(db: Session = Depends(get_db)):
    return db.query(XPRule).all()

# ✏️ 3. XP qiymatini yangilash
@router.put("/{rule_id}", response_model=XPRuleResponse, dependencies=[Depends(admin_required)])
def update_xp_rule(rule_id: str, update_data: XPRuleUpdate, db: Session = Depends(get_db)):
    rule = db.query(XPRule).filter(XPRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="XP qoidasi topilmadi.")
    rule.xp_value = update_data.xp_value
    db.commit()
    db.refresh(rule)
    return rule

# ❌ 4. Qoida o‘chirish
@router.delete("/{rule_id}", dependencies=[Depends(admin_required)])
def delete_xp_rule(rule_id: str, db: Session = Depends(get_db)):
    rule = db.query(XPRule).filter(XPRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="XP qoidasi topilmadi.")
    db.delete(rule)
    db.commit()
    return {"message": "XP qoidasi o‘chirildi ✅"}
