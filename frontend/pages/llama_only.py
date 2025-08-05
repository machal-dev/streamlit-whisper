import streamlit as st
import requests

def render():
    # from backend.llama_pack.service import generate_text

    st.header("🦙 텍스트 기반 LLaMA 생성기")

    # 사용자 입력 프롬프트 UI
    prompt = st.text_area(
        "프롬프트 입력",
        placeholder="예: 삼국지를 요약해줘",
        height=150,
        key="llama_only_prompt_input"
    )
    max_tokens = st.slider(
        "생성할 최대 토큰 수",
        16, 512, 64,
        key="llama_only_max_tokens"
    )
    temperature = st.slider(
        "창의성 (temperature)",
        0.0, 1.0, 0.7,
        key="llama_only_temperature"
    )
    do_sample = st.checkbox(
        "샘플링 사용",
        value=True,
        key="llama_only_do_sample"
    )
    extract_answer = st.checkbox(
        "답: 이후만 추출",
        value=True,
        key="llama_only_extract_answer"
    )

    # 응답 영역
    if st.button("LLaMA 응답 생성", key="llama_only_generate_button"):
        with st.spinner("생성 중..."):
            try:
                # result = generate_text(
                #     prompt=prompt,
                #     max_new_tokens=max_tokens,
                #     temperature=temperature,
                #     do_sample=do_sample,
                #     extract_after_answer=extract_answer
                # )
                # st.success("응답 생성 완료")
                # st.text_area("📄 응답 결과", result, height=200, key="llama_only_result_output")

                result = requests.post(
                        "http://localhost:8000/llama/generate",
                        json={
                            "prompt": prompt,
                            "max_new_tokens": max_tokens,
                            "temperature": temperature,
                            "do_sample": do_sample,
                            "extract_after_answer": extract_answer,
                        },
                    )
                if result.status_code == 200:
                    result_json = result.json()  # ← 응답 본문을 파싱
                    answer = result_json["result"]  # ← 실제 생성된 응답 텍스트
                    st.text_area("📄 응답 결과", answer)

                st.success("응답 생성 완료")
                st.text_area("📄 응답 결과", result, height=200, key="llama_only_result_output")
            except Exception as e:
                st.error(f"오류 발생: {e}")
