# backend/whisper_pack/service.py

"""
Whisper 모델 서비스 로직
- 음성 파일을 텍스트로 변환
"""

import logging
from backend.whisper_pack.controller import load_model, get_model

logger = logging.getLogger(__name__)


def transcribe_audio(file_path: str, language: str = "ko") -> str:
    """
    Whisper 모델을 사용해 음성 파일을 텍스트로 변환한다.

    Args:
        file_path (str): 오디오 파일 경로 (wav, mp3 등)
        language (str): 언어 코드 (기본: 한국어 "ko")

    Returns:
        str: 인식된 텍스트
    """
    logger.info("🟨 [Whisper] 음성 인식 시작")
    logger.debug(f"파일 경로: {file_path} / 언어: {language}")

    # 모델이 로딩되지 않았다면 로드
    load_model()
    model = get_model()

    # whisper는 내부적으로 ffmpeg를 호출해서 파일을 처리
    result = model.transcribe(file_path, language=language)

    text = result.get("text", "").strip()
    logger.info("🟩 [Whisper] 음성 인식 완료")
    logger.debug(f"결과: {text[:100]}...")

    return text
