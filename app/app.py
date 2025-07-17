import streamlit as st
import requests
import streamlit.components.v1 as components

API_URL = "http://localhost:8000"
st.set_page_config(page_title="AI 유틸리티", page_icon="🤖")


def show_whisper_page():
    st.header("🎙️ 음성 인식 + 번역")
    st.caption("업로드한 음성을 Whisper 모델로 인식하고 번역합니다.")

    uploaded_file = st.file_uploader(
        "음성 파일 업로드", type=["wav", "mp3", "m4a"],
        help="200MB 이하의 wav, mp3, m4a 형식 지원"
    )

    if uploaded_file:
        st.audio(uploaded_file)
        st.success(f"파일 업로드됨: {uploaded_file.name}")

    if st.button("🧠 인식 시작"):
        if uploaded_file:
            try:
                with st.spinner("인식 중..."):
                    files = {"file": uploaded_file.getvalue()}
                    response = requests.post(f"{API_URL}/transcribe", files=files)

                    if response.status_code == 200:
                        result = response.json()
                        st.success("인식 완료!")
                        st.write("📝 한글:", result["korean"])
                        st.write("🌐 영어:", result["english"])
                    else:
                        st.error("인식 실패: 서버 응답 오류")
            except Exception as e:
                st.error(f"에러 발생: {e}")
        else:
            st.warning("음성 파일을 먼저 업로드해주세요.")


def show_llama_page():
    st.header("🦙 LLaMA 모델 텍스트 생성")
    prompt = st.text_area("프롬프트 입력", placeholder="예: 한국의 수도는 어디인가요?\n답:")
    max_tokens = st.slider("최대 토큰 수", 16, 256, 64)
    temperature = st.slider("창의성 (Temperature)", 0.1, 1.5, 0.7)

    if st.button("🚀 텍스트 생성"):
        if prompt.strip():
            try:
                with st.spinner("LLaMA 생성 중..."):
                    res = requests.post(
                        f"{API_URL}/llama/generate",
                        json={
                            "prompt": prompt,
                            "max_new_tokens": max_tokens,
                            "temperature": temperature,
                            "do_sample": True
                        },
                        timeout=120
                    )
                    if res.status_code == 200:
                        output = res.json()["result"]
                        st.success("생성 완료!")
                        st.code(output)
                    else:
                        st.error("⚠️ 응답 실패. 서버 확인 필요.")
            except Exception as e:
                st.error(f"에러 발생: {e}")
        else:
            st.warning("프롬프트를 입력해주세요.")


def main():
    st.sidebar.title("🧭 기능 선택")
    page = st.sidebar.radio("페이지 이동", ["Whisper 인식", "LLaMA 텍스트 생성"])

    if page == "Whisper 인식":
        show_whisper_page()
    elif page == "LLaMA 텍스트 생성":
        show_llama_page()


if __name__ == "__main__":
    main()
