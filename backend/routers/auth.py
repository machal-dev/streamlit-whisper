from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from core.db import get_db
from schemas.auth import LoginRequest, TokenResponse
from services.auth_service import authenticate_user, create_session
from dependencies.session import get_current_user
from schemas.user import UserOut

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(
    payload: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    user = authenticate_user(payload.email, payload.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="잘못된 이메일 또는 비밀번호입니다.")

    session_token = create_session(user.id)

    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        max_age=60,  # 1분 TTL
        samesite="lax"
    )

    return {"access_token": session_token, "token_type": "bearer"}
