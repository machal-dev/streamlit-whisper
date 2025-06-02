import whisper
import torch
import asyncio
import os

device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("medium", device=device)


# 🎯 동기 함수 (스크립트 실행 등에서 바로 호출 가능)
def transcribe_sync(path: str, translate: bool = False) -> str:
    task = "translate" if translate else "transcribe"
    result = model.transcribe(path, language="ko", task=task)
    return result["text"]


# ⚡ 비동기 함수 (FastAPI 등에서 사용 가능)
async def transcribe_async(path: str, translate: bool = False) -> str:
    loop = asyncio.get_event_loop()
    task = "translate" if translate else "transcribe"
    result = await loop.run_in_executor(None, lambda: model.transcribe(path, language="ko", task=task))
    return result["text"]
