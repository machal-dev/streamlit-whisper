from fastapi import Cookie, Depends, HTTPException
from sqlalchemy.orm import Session

from core.redis import redis_client
from core.db import get_db
from models.user import User


def get_current_user(session_token: str = Cookie(None), db: Session = Depends(get_db)) -> User:
    print("🟦 [Server] get_current_user() 진입")

    if not session_token:
        print("🟥 [Server] 세션 토큰 없음 → 401 반환")
        raise HTTPException(status_code=401, detail="No session token")

    print(f"🟦 [Server] 세션 토큰 수신: {session_token}")

    user_id = redis_client.get(f"session:{session_token}")
    if not user_id:
        print(f"🟥 [Server] Redis 세션 만료 또는 존재하지 않음 → 401 반환")
        raise HTTPException(status_code=401, detail="Session expired or invalid")

    print(f"🟩 [Server] Redis 세션 유효 → user_id: {user_id}")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        print(f"🟥 [Server] DB에 해당 유저 없음 → 404 반환")
        raise HTTPException(status_code=404, detail="User not found")

    print(f"🟩 [Server] 유저 정보 조회 성공 → 이메일: {user.email}")
    return user
