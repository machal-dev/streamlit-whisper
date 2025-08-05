# backend/whisper_pack/controller.py

"""
Whisper 모델 컨트롤러
- 모델 로딩, 언로딩, 상태 확인 (Lazy Loading)
"""

import logging
import torch
import whisper
from backend.whisper_pack import config

logger = logging.getLogger(__name__)

# 전역 객체
_model = None
_is_loaded = False


def load_model():
    """Whisper 모델을 lazy-loading 방식으로 로딩한다."""
    global _model, _is_loaded

    if _is_loaded:
        logger.info(f"{config.LOG_TAG} 🔄 이미 로딩된 모델 사용")
        return

    logger.info(f"{config.LOG_TAG} 🟡 모델 로딩 중...")

    _model = whisper.load_model(config.MODEL_ID, device=config.DEVICE)

    _is_loaded = True
    logger.info(f"{config.LOG_TAG} ✅ Whisper 모델 로딩 완료")


def unload_model():
    """Whisper 모델을 언로딩하고 GPU 메모리를 정리한다."""
    global _model, _is_loaded

    if not _is_loaded:
        logger.info(f"{config.LOG_TAG} 🚫 언로드할 모델이 없습니다.")
        return

    del _model
    torch.cuda.empty_cache()
    _is_loaded = False
    logger.info(f"{config.LOG_TAG} 🧹 모델 언로드 및 GPU 메모리 정리 완료")


def is_model_loaded() -> bool:
    """모델 로딩 여부 확인"""
    return _is_loaded


def get_model():
    """Whisper 모델 인스턴스를 반환. 미로딩 시 예외 발생."""
    if not _is_loaded:
        raise RuntimeError("Whisper 모델이 로드되지 않았습니다. 먼저 load_model()을 호출하세요.")
    return _model
