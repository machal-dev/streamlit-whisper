# FastAPI + Streamlit 기반 음성 인식 및 텍스트 생성 웹앱

이 프로젝트는 Whisper 모델로 음성을 텍스트로 변환하고, 변환된 텍스트를 LLaMA 모델로 처리해 응답을 생성하는 AI 웹 애플리케이션입니다.  
FastAPI 백엔드와 Streamlit 프론트엔드를 통합하여 직관적인 인터페이스와 빠른 응답을 제공합니다.

---

## 📁 프로젝트 구조

```
fastapi-streamlit-stt/
├── backend/                    # FastAPI 백엔드
│   ├── main.py                 # FastAPI 앱 엔트리포인트
│   ├── llama_pack/            # LLaMA 모델 관련 패키지
│   ├── whisper_pack/          # Whisper 음성 인식 관련 패키지
│   ├── db_pack/               # DB 관련 유틸리티 (SQLAlchemy)
│   ├── redis_pack/            # Redis 관련 유틸리티
├── frontend/                  # Streamlit 프론트엔드
│   ├── app.py                 # Streamlit 메인 앱
│   └── pages/                 # 기능별 탭 페이지
├── .env                       # 환경 변수 설정 파일
├── requirements.txt           # 패키지 목록
├── docker-compose.yml         # DB/Redis 실행용 도커 설정
└── README.md
```

---

## 주요 기능

- Whisper 모델로 음성 파일 텍스트 전사
- 텍스트를 LLaMA 모델에 전달해 답변 생성
- FastAPI 백엔드 API 구성
- Streamlit 기반 탭 UI 제공
- 로컬 MySQL + Redis 연동 지원
- GPU 사용 가능 (CUDA 환경 구성 시)

---

## 실행 방법

### 1. 프로젝트 클론 및 가상환경 설정

```bash
git clone https://github.com/machal-dev/streamlit-whisper.git
cd streamlit-whisper
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate         # Windows
```

---

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

---

### 3. `.env` 파일 설정

루트 디렉토리에 다음 내용을 포함한 `.env` 파일을 생성하세요:

```env
SECRET_KEY=your-super-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=3

# MySQL
MYSQL_ROOT_PASSWORD=rootpass123
MYSQL_DATABASE=stt_app
MYSQL_USER=stt_user
MYSQL_PASSWORD=sttpass123
DATABASE_URL=mysql+pymysql://stt_user:sttpass123@localhost:3306/stt_app

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
```

---

### 4. MySQL & Redis 실행 (Docker 사용)

```bash
docker-compose up -d
```

> 설치 필요 시: [Docker 설치 가이드](https://docs.docker.com/get-docker/)

---

### 5. FastAPI 서버 실행

```bash
uvicorn backend.main:frontend --reload
```

- API 문서 확인: http://localhost:8000/docs
- Whisper: POST `/whisper/transcribe`
- LLaMA: POST `/llama/generate`

---

### 6. Streamlit 앱 실행

```bash
set PYTHONPATH=.
streamlit run frontend/app.py
```

- 웹 UI 접속: http://localhost:8501
- 탭 구성:
  - LLaMA Only
  - Whisper Only
  - Voice → LLaMA

---

## PyTorch 설치 안내 (GPU 사용 시)

`requirements.txt`에는 CPU 전용 `torch`가 포함되어 있습니다.  
GPU를 사용하려면 CUDA 버전에 맞는 PyTorch를 수동 설치하세요:

### CUDA 버전 확인:

```bash
nvidia-smi
```

### 설치 예시 (CUDA 12.8 기준):

```bash
pip uninstall torch torchvision torchaudio
pip install torch==2.7.0 torchvision==0.22.0 torchaudio==2.7.0 \
--index-url https://download.pytorch.org/whl/cu128
```

> 자세한 설치 방법: https://pytorch.org/get-started/locally/

---

## 기술 스택

| 분류      | 기술                          |
|---------|-----------------------------|
| 백엔드     | FastAPI, Uvicorn              |
| 프론트엔드   | Streamlit                     |
| 모델      | Whisper, LLaMA (GPTQ)         |
| 데이터베이스 | MySQL (SQLAlchemy 기반)       |
| 캐시/세션  | Redis                         |
| 환경관리    | python-dotenv, Docker         |

---

## 향후 추가 예정 기능

- Whisper segment 시각화
- GPT 기반 감정 분석 및 요약
- SRT 자막 자동 생성
- 음성 TTS 출력
- FastAPI+Streamlit 통합 배포 자동화

---

## License

MIT License

---

## 문의 및 피드백

GitHub Issues 탭을 통해 자유롭게 제보해 주세요.  
https://github.com/machal-dev/streamlit-whisper/issues
