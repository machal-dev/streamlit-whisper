# 🧠 fastapi-streamlit-stt

Whisper 기반 음성 인식, 영어 번역 및 GPT 분석 확장 가능한  
**FastAPI + Streamlit 기반 음성 처리 프로젝트**입니다.

---

## 📦 주요 기능

- 🎙️ 음성 파일 업로드 → Whisper로 텍스트 전사
- 🌍 영어 번역 (Whisper translate 기능 활용)
- 🖥️ Streamlit UI로 결과 확인
- 🧠 GPT 분석 / 요약 기능 연동 예정
- 🔊 TTS, 자막(SRT) 생성 등 확장 가능

---

## 📁 프로젝트 구조

```

fastapi-streamlit-stt/
├── app/               # Streamlit 프론트엔드
│   ├── app.py
│   ├── pages/
│   └── static/
├── backend/           # FastAPI 백엔드
│   ├── main.py
│   ├── routers/
│   └── services/
├── shared/            # 공용 유틸/모듈 (선택)
├── .venv/             # 통합 가상환경
├── requirements.txt
└── README.md

````

---

## ⚙️ 환경 설정

### 1. 가상환경 생성 및 패키지 설치

```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\Activate.ps1       # Windows PowerShell

pip install -r requirements.txt
````

> `requirements.txt`에는 CPU-only 버전의 torch가 포함되어 있습니다.

---

## ⚡ CUDA (GPU) 환경용 PyTorch 설치

CUDA를 사용하는 환경에서는 아래 명령어로 GPU 지원 버전을 설치하세요:
(CUDA 12.8 기준)

```bash
pip install torch==2.7.0 torchvision==0.22.0 torchaudio==2.7.0 --index-url https://download.pytorch.org/whl/cu128
```

👉 [공식 PyTorch 설치 가이드 보기](https://pytorch.org/get-started/locally/)

---

## 🚀 실행

### 1. FastAPI 백엔드 실행

```bash
uvicorn backend.main:app --reload
```

→ Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

### 2. Streamlit 프론트 실행

```bash
streamlit run app/app.py
```

---

## 🧠 향후 개발 예정 기능

* [ ] Whisper 결과 기반 SRT 자막 자동 생성
* [ ] GPT 요약/분석 기능 연동
* [ ] 마이크 실시간 입력 처리 마무리
* [ ] TTS(Text-to-Speech) 기능 확장
* [ ] Docker 기반 배포 지원

---

## 🙋 사용 기술

* Python
* FastAPI
* Streamlit
* Whisper
* PyTorch
* (향후) GPT-4 / OpenAI API

---