# services/auth_service.py

from datetime import datetime, timedelta, timezone
from jose import jwt
from pydantic import EmailStr
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
import secrets
from passlib.hash import bcrypt

from core.redis import redis_client
from models.user import User

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))


def authenticate_user(email: EmailStr, password: str, db: Session) -> User | None:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not bcrypt.verify(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_session(user_id: int, expire_seconds: int = None) -> str:
    token = secrets.token_hex(32)
    if expire_seconds is None:
        expire_seconds = ACCESS_TOKEN_EXPIRE_MINUTES * 60
    redis_key = f"session:{token}"
    redis_client.setex(redis_key, expire_seconds, str(user_id))
    return token
