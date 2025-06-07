from fastapi import APIRouter, UploadFile, File
from services.whisper_service import transcribe_audio

router = APIRouter()

@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    return await transcribe_audio(file)
