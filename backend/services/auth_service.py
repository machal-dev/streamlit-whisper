from datetime import datetime, timedelta, timezone
from jose import jwt
from pydantic import EmailStr
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

from models.user import User
from core.db import get_db  # 의존성 주입 시에는 Depends 사용

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))


def authenticate_user(email: EmailStr, password: str, db: Session) -> User | None:
    user = db.query(User).filter(User.email == email).first()
    if not user or not bcrypt.verify(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
