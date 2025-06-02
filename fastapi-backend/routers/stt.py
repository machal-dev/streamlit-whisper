from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from services import whisper_service
import uuid
import aiofiles
import os

router = APIRouter()

@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    try:
        # 임시 파일로 저장
        temp_filename = f"temp_{uuid.uuid4()}.wav"
        async with aiofiles.open(temp_filename, "wb") as out_file:
            content = await file.read()
            await out_file.write(content)

        # 🧠 비동기 함수 호출
        korean_text = await whisper_service.transcribe_async(temp_filename)
        english_text = await whisper_service.transcribe_async(temp_filename, translate=True)

        os.remove(temp_filename)

        return JSONResponse(content={
            "korean": korean_text,
            "english": english_text
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
