import streamlit as st
import requests

st.set_page_config(page_title="STT & 번역", layout="centered")

st.title("🎙️ 음성 인식 + 영어 번역")
st.markdown("업로드한 음성을 Whisper 모델로 인식하고 번역합니다.")

# 파일 업로드
uploaded_file = st.file_uploader("음성 파일 업로드", type=["wav", "mp3", "m4a"])

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/wav")

    if st.button("🧠 인식 시작"):
        with st.spinner("Whisper로 처리 중..."):
            files = {"file": uploaded_file.getvalue()}
            try:
                response = requests.post("http://localhost:8000/transcribe", files={"file": uploaded_file})
                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ 처리 완료!")
                    st.subheader("🗣️ 인식된 한국어:")
                    st.write(data.get("korean", ""))

                    st.subheader("🌍 번역된 영어:")
                    st.write(data.get("english", ""))
                else:
                    st.error(f"오류 발생: {response.status_code}")
            except Exception as e:
                st.error(f"연결 실패: {e}")
