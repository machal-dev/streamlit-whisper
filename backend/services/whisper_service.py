import whisper
import os
import uuid
import torch
import logging

logger = logging.getLogger(__name__)

# 📌 전역 설정 및 모델 로딩
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_SIZE = "medium"
WHISPER_MODEL = whisper.load_model(MODEL_SIZE, device=DEVICE)
TEMP_DIR = "temp_audio"
os.makedirs(TEMP_DIR, exist_ok=True)


def save_temp_audio(file_bytes: bytes) -> str:
    """임시 wav 파일 저장 후 경로 반환"""
    file_id = str(uuid.uuid4())
    temp_path = os.path.join(TEMP_DIR, f"{file_id}.wav")
    with open(temp_path, "wb") as f:
        f.write(file_bytes)
    logger.debug(f"[🔊 Audio Saved] {temp_path}")
    return temp_path


def delete_temp_audio(path: str):
    """임시 파일 삭제"""
    try:
        os.remove(path)
        logger.debug(f"[🧹 Audio Deleted] {path}")
    except Exception as e:
        logger.warning(f"[⚠️ Delete Failed] {path} - {e}")


def run_whisper(path: str, task: str, language: str = None) -> str:
    """Whisper 모델 실행"""
    logger.debug(f"[🚀 Whisper Run] task={task}, lang={language}")
    result = WHISPER_MODEL.transcribe(path, task=task, language=language)
    return result.get("text", "").strip()


async def transcribe_audio(file, target_lang: str = "ko") -> dict:
    """Whisper 전사/번역 메인 로직 (언어 지정 기반)"""
    logger.info(f"[🎧 Start Transcription] Target Language: {target_lang}")

    file_bytes = await file.read()
    temp_path = save_temp_audio(file_bytes)

    try:
        if target_lang == "ko":
            text = run_whisper(temp_path, task="transcribe", language="ko")
        elif target_lang == "en":
            text = run_whisper(temp_path, task="translate")
        elif target_lang == "jp":
            text = run_whisper(temp_path, task="transcribe", language="ja")
        else:
            logger.warning(f"[❌ Unsupported Language] {target_lang}")
            return {"error": f"Unsupported language: {target_lang}"}

        logger.info(f"[✅ Transcription Success] lang={target_lang}, length={len(text)}")
        return {
            "text": text,
            "lang": target_lang
        }

    finally:
        delete_temp_audio(temp_path)
