import streamlit as st
import whisper
import tempfile

st.title("🎤 음성 파일 업로드 → Whisper 텍스트 변환")

uploaded_file = st.file_uploader("WAV 음성 파일을 업로드하세요.", type=["wav"])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')
    if st.button("Whisper로 텍스트 변환"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
            tmpfile.write(uploaded_file.read())
            tmpfile_path = tmpfile.name

        with st.spinner("Whisper 인식 중..."):
            model = whisper.load_model("base")
            result = model.transcribe(tmpfile_path, language="ko")
            st.success("📝 인식 결과:")
            st.write(result["text"])

else:
    st.info("WAV 파일을 업로드하면 Whisper가 음성을 텍스트로 변환해줍니다.")

st.caption("※ Whisper 모델은 처음 실행시 다운로드 시간이 걸릴 수 있습니다.")
