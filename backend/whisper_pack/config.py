# backend/whisper_pack/config.py

# 모델 ID 또는 로컬 경로 (Hugging Face or local)
# MODEL_ID = "openai/whisper-medium"  # 또는 "openai/whisper-base", "openai/whisper-large-v2" 등
# whisper.load_model() 함수는 Hugging Face 경로 스타일인 "openai/whisper-medium" 같은 건 지원하지 않고, 내장된 이름 문자열만 지원
MODEL_ID = "medium"

# 사용할 디바이스
DEVICE = "cuda"  # or "cpu"

# 로그 태그
LOG_TAG = "[🔊 Whisper]"
