### 📦 backend/db_pack/session.py

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# 환경변수에서 DB URL 읽기
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy 엔진 및 세션 구성
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 (모델 정의 시 상속)
Base = declarative_base()

# FastAPI용 의존성 주입 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 단독 실행 시 DB 연결 및 테이블 생성
if __name__ == "__main__":
    from db_pack.models import Base

    try:
        with engine.connect() as conn:
            print("✅ DB 연결 성공!")
        Base.metadata.create_all(bind=engine)
        print("✅ 테이블 생성 완료!")
    except Exception as e:
        print("❌ DB 연결 실패:", e)