import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# .env 파일 로드
load_dotenv()

# 환경변수에서 DB URL 가져오기
DATABASE_URL = os.getenv("DATABASE_URL")

# DB 연결 엔진 생성
engine = create_engine(DATABASE_URL, echo=True)

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM 모델 베이스 클래스
Base = declarative_base()

# 의존성 주입용 DB 세션 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 단독 실행 시 DB 연결 + 테이블 생성
if __name__ == "__main__":
    from models.user import Base  # 여기서만 import (실행 시점)

    try:
        with engine.connect() as conn:
            print("✅ DB 연결 성공!")

        Base.metadata.create_all(bind=engine)
        print("✅ 테이블 생성 완료!")

    except Exception as e:
        print("❌ DB 연결 실패:", e)
