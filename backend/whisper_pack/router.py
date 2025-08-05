# backend/whisper_pack/router.py

"""
Whisper API 라우터
- 음성 파일 업로드 후 텍스트 변환 요청 처리
"""

import logging
import shutil
import uuid
from fastapi import APIRouter, UploadFile, File, Form
from backend.whisper_pack.service import transcribe_audio
from pathlib import Path
import os

logger = logging.getLogger(__name__)
router = APIRouter()

# 임시 저장 경로
TEMP_DIR = Path("temp_audio")
TEMP_DIR.mkdir(exist_ok=True)


@router.post("/transcribe")
async def whisper_transcribe(
    file: UploadFile = File(..., description="음성 파일 (wav, mp3 등)"),
    language: str = Form("ko", description="언어 코드 (기본: 한국어)")
):
    """
    Whisper를 사용해 음성 파일을 텍스트로 변환합니다.
    """
    logger.info("🟦 [API] /whisper/transcribe 호출됨")

    # 임시 파일 경로 생성
    file_ext = Path(file.filename).suffix
    temp_filename = f"{uuid.uuid4()}{file_ext}"
    temp_path = TEMP_DIR / temp_filename

    # 파일 저장
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 텍스트 변환 수행
    try:
        text = transcribe_audio(str(temp_path), language=language)
    finally:
        # 변환이 끝나면 임시 파일 삭제
        if temp_path.exists():
            os.remove(temp_path)

    return {"result": text}
