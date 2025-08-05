# backend/llama_pack/config.py

"""
LLaMA 패키지 설정값 관리 모듈
"""

# Hugging Face 모델 ID (GPTQ 버전)
MODEL_ID = "TheBloke/Llama-2-7B-Chat-GPTQ"

# 모델 내부에 포함된 weight 파일의 이름
# 예시: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GPTQ
MODEL_BASENAME = "gptq_model-4bit-128g"

# 디바이스 설정: "cuda:0" 또는 "cpu"
DEVICE = "cuda:0"

# 시스템 프롬프트 기본값 (없을 경우 None)
DEFAULT_SYSTEM_PROMPT = "당신은 정중하고 지적인 한국어 어시스턴트입니다."

# 로깅 설정 (추후 loglevel 등에 사용 가능)
LOG_TAG = "[🦙 LLaMA]"
