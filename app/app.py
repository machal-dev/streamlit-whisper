import streamlit as st
import requests

API_URL = "http://localhost:8000"
st.set_page_config(page_title="음성 인식", page_icon="🎙️")


def is_session_valid():
    try:
        token = st.session_state.get("token")
        if not token:
            return False
        cookies = {"session_token": token}
        res = requests.get(f"{API_URL}/me", cookies=cookies, timeout=2)
        return res.status_code == 200
    except:
        return False


def restore_session():
    try:
        res = requests.get(f"{API_URL}/me", timeout=2)
        if res.status_code == 200:
            st.session_state["logged_in"] = True
            return True
    except:
        pass
    return False


def show_main_page():
    st.title("🎙️ 음성 인식 + 영어 번역")
    st.caption("업로드한 음성을 Whisper 모델로 인식하고 번역합니다.")

    uploaded_file = st.file_uploader(
        "음성 파일 업로드", type=["wav", "mp3", "m4a"],
        help="Limit 200MB per file · WAV, MP3, M4A"
    )

    if uploaded_file:
        st.audio(uploaded_file)

    if st.button("🧠 인식 시작"):
        if uploaded_file:
            try:
                with st.spinner("인식 중..."):
                    files = {"file": uploaded_file.getvalue()}
                    cookies = {"session_token": st.session_state["token"]}
                    response = requests.post(f"{API_URL}/transcribe", files=files, cookies=cookies)

                    if response.status_code == 200:
                        result = response.json()
                        st.success("인식 완료!")
                        st.write("📝 한글:", result["korean"])
                        st.write("🌐 영어:", result["english"])
                    else:
                        st.error("인식 실패! 서버 응답 오류")
            except Exception as e:
                st.error(f"에러 발생: {e}")
        else:
            st.warning("음성 파일을 먼저 업로드해주세요.")

    if st.button("🔓 로그아웃"):
        st.session_state.clear()
        st.rerun()


def show_login_page():
    st.title("🔐 로그인")
    email = st.text_input("이메일", value="")
    password = st.text_input("비밀번호", type="password", value="")

    if st.button("로그인"):
        try:
            res = requests.post(
                f"{API_URL}/login",
                json={"email": email, "password": password},
                timeout=3
            )
            if res.status_code == 200:
                token = res.json()["access_token"]
                st.session_state["token"] = token
                st.success("로그인 성공!")
                st.rerun()
            else:
                st.error("이메일 또는 비밀번호가 틀렸습니다.")
        except requests.exceptions.RequestException:
            st.error("❌ 서버에 연결할 수 없습니다.")


# ✅ 진입 분기
if "token" in st.session_state and is_session_valid():
    show_main_page()
elif "logged_in" in st.session_state:
    show_main_page()
elif restore_session():
    show_main_page()
else:
    st.session_state.clear()
    show_login_page()
