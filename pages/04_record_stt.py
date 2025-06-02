import whisper
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
import torch

def record_audio(duration=5, samplerate=16000):
    print(f"🎤 {duration}초 동안 녹음을 시작합니다...")
    audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    print("✅ 녹음 완료")
    return audio, samplerate

def save_wav(audio, samplerate, path):
    write(path, samplerate, audio)

def transcribe_with_whisper(wav_path):
    print("🧠 Whisper 모델 로딩 중...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("✔ 선택된 디바이스:", device)

    model = whisper.load_model("base", device=device)

    # 디바이스 확인
    print("✔ 모델 디바이스:", next(model.parameters()).device)
    print("🔍 인식 중...")
    result = model.transcribe(wav_path, language="ko")
    return result["text"]

def main():
    duration_sec = 5  # 원하는 녹음 시간
    audio, rate = record_audio(duration=duration_sec)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
        save_wav(audio, rate, tmpfile.name)
        print(f"📁 WAV 파일 저장 위치: {tmpfile.name}")

        text = transcribe_with_whisper(tmpfile.name)

    print("\n📝 인식 결과:")
    print("-" * 30)
    print(text)
    print("-" * 30)

if __name__ == "__main__":
    main()
