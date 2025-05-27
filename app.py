import streamlit as st
from modules.ai_utils import hello_ai

st.set_page_config(page_title="AI+Streamlit 실무 프로젝트", layout="wide")
st.title("AI+Streamlit 실무형 프로젝트 예제")

st.image("static/logo.png", width=120)
st.write("실무에 적합한 구조로 시작하는 Streamlit 앱입니다.")

name = st.text_input("이름을 입력하세요:")
if st.button("AI에게 인사받기") and name:
    msg = hello_ai(name)
    st.success(msg)

st.write("왼쪽 상단 ☰ 버튼을 눌러 다른 페이지로 이동해보세요!")
