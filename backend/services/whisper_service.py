import whisper
import os
import uuid
import torch

# # 모델 로딩 (전역)
# device = "cuda" if torch.cuda.is_available() else "cpu"
# model = whisper.load_model("medium", device=device)

async def transcribe_audio(file):
    temp_dir = "temp_audio"
    os.makedirs(temp_dir, exist_ok=True)

    file_id = str(uuid.uuid4())
    temp_path = os.path.join(temp_dir, f"{file_id}.wav")

    with open(temp_path, "wb") as f:
        f.write(await file.read())

    # 모델 로딩 (초기화 안전)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model("medium", device=device)

    # 1차: 한국어 전사 (task=transcribe)
    original_result = model.transcribe(temp_path, language="ko", task="transcribe")
    korean_text = original_result.get("text", "")

    # 2차: 영어 번역 (task=translate)
    translated_result = model.transcribe(temp_path, task="translate")
    english_text = translated_result.get("text", "")

    os.remove(temp_path)

    return {
        "korean": korean_text.strip(),
        "english": english_text.strip()
    }
