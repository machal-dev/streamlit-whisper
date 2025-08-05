import streamlit as st
import requests
import tempfile
import os

def render():
    st.header("🗣️ 음성 인식 (Whisper)")

    # 오디오 업로드 UI
    uploaded_file = st.file_uploader(
        "음성 파일 업로드 (mp3, wav 등)",
        type=["mp3", "wav", "m4a"],
        key="whisper_only_file_uploader"
    )

    language = st.selectbox(
        "언어 선택",
        options=["ko", "en"],
        index=0,
        key="whisper_only_language_select"
    )

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(uploaded_file.read())
            temp_path = tmp.name

        st.audio(temp_path, format="audio/mp3", start_time=0)

        if st.button("📝 텍스트로 변환", key="whisper_only_submit_button"):
            try:
                with open(temp_path, "rb") as f:
                    files = {"file": (os.path.basename(temp_path), f, uploaded_file.type)}
                    response = requests.post(
                        "http://localhost:8000/whisper/transcribe",
                        files=files,
                        data={"language": language},
                    )

                if response.status_code == 200:
                    result = response.json()["result"]
                    st.success("✅ 변환 완료")
                    st.text_area("🧾 인식 결과", result, height=200, key="whisper_only_output")
                else:
                    st.error(f"❌ 오류 발생: {response.text}")
            except Exception as e:
                st.error(f"예외 발생: {e}")
            finally:
                os.remove(temp_path)
