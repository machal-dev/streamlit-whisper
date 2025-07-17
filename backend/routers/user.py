from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies.session import get_current_user
from schemas.user import UserOut, UserCreate
from models.user import User
from core.db import get_db
from passlib.hash import bcrypt
from datetime import datetime

router = APIRouter()


@router.get("/me", response_model=UserOut)
def read_me(current_user=Depends(get_current_user)):
    print("🔍 [DEBUG] read_me session_state:")
    return current_user


@router.post("/register", response_model=UserOut)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="이미 가입된 이메일입니다.")

    hashed_pw = bcrypt.hash(payload.password)
    user = User(
        email=payload.email,
        hashed_password=hashed_pw,
        created_at=datetime.utcnow()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
