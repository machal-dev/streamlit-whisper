import streamlit as st
import requests
import tempfile
import os

def render():
    from backend.llama_pack.service import generate_text

    st.header("🎙️ 음성으로 질문 → LLaMA 응답")

    # 오디오 업로드 UI
    uploaded_file = st.file_uploader(
        "음성 파일 업로드 (mp3, wav 등)",
        type=["mp3", "wav", "m4a"],
        key="voice_to_llm_file_uploader"
    )

    language = st.selectbox(
        "언어 선택",
        options=["ko", "en"],
        index=0,
        key="voice_to_llm_language_select"
    )

    max_tokens = st.slider(
        "응답 최대 토큰 수",
        16, 512, 64,
        key="voice_to_llm_max_tokens"
    )

    temperature = st.slider(
        "창의성 (temperature)",
        0.0, 1.0, 0.7,
        key="voice_to_llm_temperature"
    )

    do_sample = st.checkbox(
        "샘플링 사용",
        value=True,
        key="voice_to_llm_do_sample"
    )

    extract_answer = st.checkbox(
        "답: 이후만 추출",
        value=True,
        key="voice_to_llm_extract_answer"
    )

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(uploaded_file.read())
            temp_path = tmp.name

        st.audio(temp_path, format="audio/mp3", start_time=0)

        if st.button("🧠 질문하고 답변 받기", key="voice_to_llm_submit_button"):
            try:
                with open(temp_path, "rb") as f:
                    files = {"file": (os.path.basename(temp_path), f, uploaded_file.type)}
                    whisper_res = requests.post(
                        "http://localhost:8000/whisper/transcribe",
                        files=files,
                        data={"language": language},
                    )

                if whisper_res.status_code == 200:
                    prompt = whisper_res.json()["result"]
                    st.info(f"📝 인식된 질문: {prompt}", icon="📝")

                    result = generate_text(
                        prompt=prompt,
                        max_new_tokens=max_tokens,
                        temperature=temperature,
                        do_sample=do_sample,
                        extract_after_answer=extract_answer
                    )
                    st.success("응답 생성 완료")
                    st.text_area("📄 응답 결과", result, height=200, key="llama_only_result_output")

                    # GPU 부하로 인한 테스트 불가 상황 
                    # llama_res = requests.post(
                    #     "http://localhost:8000/llama/generate",
                    #     json={
                    #         "prompt": prompt,
                    #         "max_new_tokens": max_tokens,
                    #         "temperature": temperature,
                    #         "do_sample": do_sample,
                    #         "extract_after_answer": extract_answer,
                    #     },
                    # )
                    #
                    # if llama_res.status_code == 200:
                    #     answer = llama_res.json()["result"]
                    #     st.success("✅ 응답 완료")
                    #     st.text_area("📄 LLaMA 응답", answer, height=200, key="voice_to_llm_output")
                    # else:
                    #     st.error(f"LLaMA 오류: {llama_res.text}")
                else:
                    st.error(f"Whisper 오류: {whisper_res.text}")
            except Exception as e:
                st.error(f"예외 발생: {e}")
            finally:
                os.remove(temp_path)
