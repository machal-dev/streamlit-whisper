from fastapi import APIRouter, UploadFile, File, Query
from services.whisper_service import transcribe_audio
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class TranscriptionLang(str, Enum):
    ko = "ko"
    en = "en"
    jp = "jp"  # 향후 테스트용 확장


router = APIRouter()


@router.post("/transcribe")
async def transcribe(
    file: UploadFile = File(...),
    target_lang: TranscriptionLang = Query(TranscriptionLang.ko, description="출력 언어: ko(한글 전사), en(영어 번역), jp(일본어 추론)")
):
    logger.info(f"[📥 /transcribe 요청] target_lang={target_lang}")
    result = await transcribe_audio(file, target_lang=target_lang.value)
    logger.info(f"[📤 /transcribe 응답 완료] lang={target_lang}, length={len(result.get('text', ''))}")
    return result
