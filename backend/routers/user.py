from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.db import get_db
from models.user import User
from schemas.user import UserCreate, UserOut
from passlib.hash import bcrypt
from datetime import datetime

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    # 이메일 중복 확인
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="이미 가입된 이메일입니다.")

    # 비밀번호 해싱
    hashed_pw = bcrypt.hash(payload.password)

    # 유저 생성
    user = User(
        email=payload.email,
        hashed_password=hashed_pw,
        created_at=datetime.utcnow()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
