# 🧠 FastAPI + Streamlit 기반 STT 음성 인식 웹앱

Whisper 모델 기반으로 음성 입력을 텍스트로 전사하고,  
자동으로 영어 번역까지 처리하는 AI 음성 인식 웹 애플리케이션입니다.

백엔드는 FastAPI, 프론트는 Streamlit으로 구성되었으며  
JWT 인증, GPU 연산 지원, 향후 GPT 분석 및 자막 생성 등 다양한 확장도 고려됩니다.

---

## 📁 프로젝트 구조

```

fastapi-streamlit-stt/
├── app/                    # Streamlit 프론트엔드
│   └── app.py
├── backend/                # FastAPI 백엔드
│   ├── main.py             # FastAPI 앱 엔트리포인트
│   ├── routers/            # API 라우터 (stt, auth)
│   ├── services/           # Whisper, 인증 등 비즈니스 로직
│   └── models/             # Pydantic 스키마
├── .env                    # 환경 변수 설정
├── requirements.txt        # 패키지 목록
└── README.md

````

---

## 🧩 주요 기능

- 🎙️ 음성 파일을 텍스트로 전사 (Whisper 기반)
- 🌍 자동 영어 번역 포함
- 🔐 로그인 기반 JWT 인증
- 🖼️ Streamlit 기반 웹 인터페이스
- ⚙️ GPU 지원 가능 (CUDA 환경 구성 시)

---

## 🚀 실행 방법

### 1. 가상환경 설정

```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows
````

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

---

### 3. `.env` 파일 생성

루트 디렉토리에 아래 내용을 가진 `.env` 파일을 생성합니다:

```env
SECRET_KEY=sk_your_super_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

✅ **주의**: `.env` 파일은 Git에 포함되지 않도록 `.gitignore`로 관리됩니다.

---

### 4. FastAPI 서버 실행

```bash
uvicorn backend.main:frontend --reload
```

* API 문서 확인: [http://localhost:8000/docs](http://localhost:8000/docs)
* `/login` → JWT 토큰 발급
* 인증 필요한 API → `Authorization: Bearer <access_token>` 헤더 필요

---

### 5. Streamlit 앱 실행

```bash
streamlit run frontend/frontend.py
```

* 음성 파일 업로드 → STT 처리 결과 확인 가능

---

## ⚙️ PyTorch 설치 안내 (CPU vs GPU 환경)

기본 `requirements.txt`에는 **CPU 전용 torch**가 포함되어 있습니다.
GPU 환경 사용자는 자신의 CUDA 버전에 맞는 torch를 **직접 설치**해야 합니다.

---

### ✅ 내 GPU 환경 확인

```bash
nvidia-smi
```

* 출력의 CUDA 버전을 확인하세요 (예: CUDA 12.8)

---

### ✅ 공식 설치 가이드 링크

👉 [PyTorch 설치 페이지](https://pytorch.org/get-started/locally/)
→ OS, Package manager, CUDA version을 선택하면 명령어가 자동 생성됩니다.

---

### 💡 예시 설치 명령어

| 환경                      | 설치 명령어                                                                                        |
| ----------------------- | --------------------------------------------------------------------------------------------- |
| CPU 전용                  | `pip install torch torchvision torchaudio`                                                    |
| CUDA 11.8               | `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118` |

### ✅ CUDA 12.8 (예: RTX 3060 등) 사용자용 설치 명령어

```bash
pip install torch==2.7.0 torchvision==0.22.0 torchaudio==2.7.0 \
--index-url https://download.pytorch.org/whl/cu128
```

> ⚠️ 주의: 위 명령어는 PyTorch 공식 다운로드 경로 기준이며,
> CUDA 12.8이 **사전 설치된 환경**이어야 제대로 작동합니다.

* 설치 전 `nvidia-smi` 명령어로 CUDA 버전이 12.8인지 확인하세요.
* 기존 torch가 설치되어 있다면, 먼저 제거해 주세요:

```bash
pip uninstall torch torchvision torchaudio
```

---

## 🔮 개발 예정 기능

* ⏱️ SRT 자막 파일 자동 생성
* 📊 Whisper segment 시각화
* 🤖 GPT 기반 텍스트 요약 / 감정 분석
* 🔊 TTS 변환으로 음성 재생
* 🚀 Docker 기반 배포 자동화

---

## 🛠️ 기술 스택

| 영역   | 기술                               |
| ---- | -------------------------------- |
| 백엔드  | FastAPI, Uvicorn, Whisper        |
| 프론트  | Streamlit                        |
| 인증   | JWT (python-jose), python-dotenv |
| 음성처리 | torchaudio, pydub                |
| 번역   | Whisper 내부 기능                    |
| 모델   | openai-whisper (medium 권장)       |

---

## 📄 License

MIT License

---

> 💬 문의 및 피드백: [깃허브 이슈](https://github.com/machal-dev/streamlit-whisper/issues)
