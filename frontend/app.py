import streamlit as st
import sys, os

# 루트 디렉토리 강제 삽입
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# print("🧭 sys.path =", sys.path)
# print("📁 cwd =", os.getcwd())


# ✅ 이제 import가 정상적으로 작동함
from pages import llama_only, whisper_only, voice_to_llm

# 👉 탭 UI 구성
st.set_page_config(page_title="🧠 AI 유틸리티", layout="wide")
st.title("🧠 AI 유틸리티 데모")

tab1, tab2, tab3 = st.tabs(["🦙 LLaMA Only", "🔊 Whisper Only", "🎙️ Voice → LLaMA"])

with tab1:
    llama_only.render()

with tab2:
    whisper_only.render()

with tab3:
    voice_to_llm.render()
