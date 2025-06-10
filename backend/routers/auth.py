from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.auth import LoginRequest, LoginResponse
from services.auth_service import authenticate_user, create_access_token
from core.db import get_db

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def login(login_req: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(login_req.email, login_req.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")

    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
