# 🎙️ Streamlit Whisper STT Demo

Whisper + Streamlit 기반의 **유사 실시간 음성 인식(STT)** 웹앱입니다.  
마이크 입력 또는 파일 업로드를 통해 음성을 텍스트로 변환하고, 향후 자막 생성·GPT 연동·TTS 등으로 확장 가능하도록 설계되었습니다.

---

## 🧭 프로젝트 설명

본 프로젝트는 개인 포트폴리오 용도로, 실제 업무에 가까운 형태로 다음을 목표로 구성되었습니다:

- Whisper 모델 기반의 **실시간 또는 유사 실시간 STT 웹앱**
- **마이크 입력 또는 파일 업로드**를 통한 텍스트 변환 → 자막/분석 처리까지 확장 가능
- **Streamlit 단독 구성**, 백엔드/프론트 구분 없이 동작
- 추후 TTS, GPT, 다국어 대화 분석 기능으로 확장 가능
- 실제 배포 및 문서화까지 고려된 실무형 구조

---

## 🚀 주요 기능

- 🎧 **파일 업로드 음성 인식** (`.wav`, `.mp3` 등 지원)
- 🎙️ **마이크 입력 기반 near-real-time transcription (진행 중)**
- 📃 Whisper 기반 텍스트 출력 (한국어 포함 다국어 자동 인식)
- 📂 결과 저장/다운로드, 향후 SRT 자막 출력 확장 고려
- 🧱 실무형 구조: `pages/`, `modules/`, `static/` 분리 설계

---

## 🧠 기술 스택

| 분야       | 기술/도구                    |
|------------|------------------------------|
| UI         | Streamlit                    |
| 음성입력   | sounddevice, ffmpeg-python   |
| 모델       | OpenAI Whisper               |
| 언어       | Python 3.11                  |
| 구조화     | 모듈 분리 / 페이지 기반 구성 |

---

## 🗂️ 프로젝트 구조

```
streamlit-whisper/
├─ app.py                      # Streamlit 메인 앱
├─ requirements.txt            # 의존성 목록
├─ .gitignore
├─ data/
│   └─ sample.csv              # 예제 입력 데이터
├─ modules/
│   └─ ai_utils.py             # Whisper 호출 유틸 함수
├─ pages/
│   ├─ 01_dashboard.py         # 대시보드 (탭 1)
│   └─ 02_speech_to_text.py    # STT 메인 기능 탭
├─ static/
│   └─ logo.png                # 로고 등 정적 리소스
```

---

## ⚙️ 설치 & 실행 가이드

### 1. Python 환경 설정
```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

> 📦 **requirements.txt**에는 공용 환경 기준 필수 패키지만 포함되어 있습니다.  
> CUDA 등 환경별 패키지는 아래 설명 참고.

---

### 2. CUDA 환경 안내 (선택적 구성)

본 프로젝트는 Whisper 모델이 GPU(CUDA)를 사용할 경우 성능이 향상됩니다.  
하지만 CUDA 환경은 사용자의 GPU/드라이버에 따라 다르므로, 아래 방법 중 하나를 선택해서 별도 설치하세요.

#### ✅ 방법 A: pip 설치
CUDA 드라이버와 버전에 맞는 PyTorch + CUDA 조합을 직접 설치

```bash
# 예: CUDA 12.1을 사용하는 경우
pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cu121
```

▶ CUDA 버전 확인 및 설치: [PyTorch 설치 가이드](https://pytorch.org/get-started/locally/)

#### ✅ 방법 B: Conda 사용 (추천)
```bash
conda create -n whisper python=3.11
conda activate whisper
conda install pytorch pytorch-cuda=12.1 -c pytorch -c nvidia
pip install -r requirements.txt
```

---

### 3. FastAPI 또는 Streamlit 실행

#### 📍 Streamlit (UI 앱 실행)
```bash
streamlit run app.py
```

---

## 📌 개발 중인 기능 (Work in Progress)

- [ ] 실시간 마이크 입력 → Chunk 기반 transcription 안정화
- [ ] Whisper 추론 속도 개선 (faster-whisper 도입 가능성)
- [ ] transcription 결과 SRT 변환 + 다운로드
- [ ] OpenAI GPT 연동 → 대화 분석 / 요약
- [ ] TTS(음성 합성) 연계로 텍스트 → 음성 변환

---

## 🧪 테스트 및 로깅

- 현재 `logs/` 디렉토리는 미사용 상태 (추후 세션별 로그 저장 설계 예정)
- 개발자용 유틸 함수는 `modules/` 폴더 하위에 구성

---

## 📄 라이선스

MIT License — 자유롭게 활용 가능하며, 인용 시 출처를 밝혀주세요 🙌

---

> 문서 최종 업데이트: 2025-06-02
