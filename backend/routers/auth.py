from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from sqlalchemy.orm import Session
from core.db import get_db
from core.redis import redis_client
from schemas.auth import LoginRequest, TokenResponse
from services.auth_service import authenticate_user, create_session

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(
    payload: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    print("🟦 [Server] /login 진입")
    print(f"🟦 [Server] 요청 이메일: {payload.email}")

    user = authenticate_user(payload.email, payload.password, db)
    if not user:
        print("🟥 [Server] 로그인 실패: 사용자 인증 실패")
        raise HTTPException(status_code=401, detail="잘못된 이메일 또는 비밀번호입니다.")

    session_token = create_session(user.id)

    print(f"🟢 [Server] 로그인 성공 → 세션 토큰 발급: {session_token}")

    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        max_age=1800,  # 30분 TTL
        samesite="lax"
    )

    return {"access_token": session_token, "token_type": "bearer"}


@router.get("/restore")
def restore_session(session_token: str = Cookie(None), db: Session = Depends(get_db)):
    print("🟦 [Server] /restore 진입")

    if not session_token:
        print("🟥 [Server] 세션 토큰 없음 → 401 반환")
        raise HTTPException(status_code=401, detail="No session token")

    user_id = redis_client.get(f"session:{session_token}")
    if not user_id:
        print("🟥 [Server] Redis에 세션 없음 → 401 반환")
        raise HTTPException(status_code=401, detail="Session expired")

    print(f"🟩 [Server] 세션 유효 → 유저 ID: {user_id}")
    return {"logged_in": True, "user_id": user_id}
