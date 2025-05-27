# modules/ai_utils.py

import whisper

def hello_ai(name):
    return f"안녕하세요, {name}님! AI가 인사합니다 :)"

def whisper_transcribe(audio_path, lang='ko'):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, language=lang)
    return result["text"]