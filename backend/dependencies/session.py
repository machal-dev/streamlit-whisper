# core/session.py 또는 dependencies/session.py

from fastapi import Cookie, Depends, HTTPException
from sqlalchemy.orm import Session

from core.redis import redis_client
from core.db import get_db
from models.user import User


def get_current_user(session_token: str = Cookie(None), db: Session = Depends(get_db)) -> User:
    if not session_token:
        raise HTTPException(status_code=401, detail="No session token")

    user_id = redis_client.get(f"session:{session_token}")
    if not user_id:
        raise HTTPException(status_code=401, detail="Session expired or invalid")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
