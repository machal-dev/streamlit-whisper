import sounddevice as sd
import numpy as np
import whisper
import tempfile
from scipy.io.wavfile import write
import os
import streamlit as st

# 설정
SAMPLE_RATE = 16000
DURATION = 2

model = whisper.load_model("base")

st.title("🎙 실시간 Whisper STT (에러 없는 버전)")

if "text_buffer" not in st.session_state:
    st.session_state.text_buffer = ""

if st.button("🎤 음성 녹음 및 인식"):
    # 마이크 녹음
    audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype="int16")
    sd.wait()

    audio_np = np.squeeze(audio)

    # WAV 파일 저장
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
        tmp_path = tmpfile.name

    write(tmp_path, SAMPLE_RATE, audio_np)  # ❗ write는 with 바깥에서 호출
    try:
        result = model.transcribe(tmp_path, language="ko")
        text = result["text"].strip()
        if text:
            st.session_state.text_buffer += text + " "
        os.remove(tmp_path)  # 삭제는 끝나고 나서 안전하게
    except Exception as e:
        st.error(f"🚨 Whisper 처리 실패: {e}")
        st.stop()

st.markdown("### 📝 인식된 자막:")
st.write(st.session_state.text_buffer)
