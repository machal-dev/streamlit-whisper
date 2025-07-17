import streamlit as st
import requests
import streamlit.components.v1 as components  # 이미 있다면 생략

API_URL = "http://localhost:8000"
st.set_page_config(page_title="음성 인식", page_icon="🎙️")

def inject_restore_js():
    js_code = """
    <script>
    (async () => {
        console.log("🟦 [JS] /restore 요청 시작");
        const res = await fetch("http://localhost:8000/restore", {
            credentials: "include"
        });
        if (res.ok) {
            const data = await res.json();
            document.cookie = "restored_user_id=" + data.user_id + "; path=/";
            console.log("🟢 [JS] 세션 복원 성공, 쿠키 저장됨: restored_user_id=" + data.user_id);
        } else {
            console.log("🟥 [JS] 세션 복원 실패:", res.status);
            document.cookie = "restored_user_id=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        }
    })();
    </script>
    """
    components.html(js_code, height=0)


def setup_session_listener():
    listener_code = """
    <script>
    window.addEventListener("message", (event) => {
        console.log("📩 [JS Listener] 메시지 수신:", event.data);
        if (event.data.type === "restore_success") {
            window.parent.postMessage({ streamlitSetComponentValue: {
                key: "restored_user_id",
                value: event.data.user_id
            }}, "*");
        } else {
            window.parent.postMessage({ streamlitSetComponentValue: {
                key: "restored_user_id",
                value: null
            }}, "*");
        }
    });
    </script>
    """
    components.html(listener_code, height=0)


# ✅ 최초 1회만 서버 세션 복구 시도
def restore_session_once():
    if "checked_session" not in st.session_state:
        print("🟦 [Client] >>> 앱 시작: restore_session_once() 호출")

        inject_restore_js()
        setup_session_listener()

        st.session_state["checked_session"] = True
        # 아래 라인을 추가해 컴포넌트 값을 세션에서 감지하도록 유도
        components.html("", height=0, key="restored_user")

    restored_user_id = st.session_state.get("restored_user")

    if restored_user_id is not None:
        print(f"✅ [DEBUG] 세션 복원 성공 → 유저 ID: {restored_user_id}")
        st.session_state["logged_in"] = True
        st.rerun()  # 💡 복원 성공 시 앱 전체 재실행 → 로그인 페이지에서 메인으로 이동
    else:
        st.session_state["logged_in"] = False
        print("❌ [DEBUG] 세션 복원 실패 또는 미확인")




def show_main_page():
    print("🟦 [Client] show_main_page() 진입")

    st.title("🎙️ 음성 인식 + 영어 번역")
    st.caption("업로드한 음성을 Whisper 모델로 인식하고 번역합니다.")

    uploaded_file = st.file_uploader(
        "음성 파일 업로드", type=["wav", "mp3", "m4a"],
        help="Limit 200MB per file · WAV, MP3, M4A"
    )

    if uploaded_file:
        st.audio(uploaded_file)
        print("🟢 [Client] 파일 업로드됨:", uploaded_file.name)

    if st.button("🧠 인식 시작"):
        print("🟦 [Client] [버튼] 인식 시작 클릭")

        if uploaded_file:
            try:
                with st.spinner("인식 중..."):
                    print("⏳ [Client] Whisper 전송 시작")
                    files = {"file": uploaded_file.getvalue()}
                    cookies = {"session_token": st.session_state.get("token")}

                    response = requests.post(f"{API_URL}/transcribe", files=files, cookies=cookies)

                    if response.status_code == 200:
                        result = response.json()
                        print("🟢 [Client] Whisper 처리 성공:", result)
                        st.success("인식 완료!")
                        st.write("📝 한글:", result["korean"])
                        st.write("🌐 영어:", result["english"])
                    else:
                        print(f"🟥 [Client] Whisper 처리 실패, 응답코드: {response.status_code}")
                        st.error("인식 실패! 서버 응답 오류")
            except Exception as e:
                print("🟥 [Client] Whisper 요청 중 에러 발생:", e)
                st.error(f"에러 발생: {e}")
        else:
            print("🟡 [Client] 파일 없음")
            st.warning("음성 파일을 먼저 업로드해주세요.")

    if st.button("🔓 로그아웃"):
        print("🔃 [Client] 로그아웃 시도")
        st.session_state.clear()
        st.rerun()


def show_login_page():
    print("🟦 [Client] show_login_page() 진입")

    st.title("🔐 로그인")
    email = st.text_input("이메일", value="")
    password = st.text_input("비밀번호", type="password", value="")

    if st.button("로그인"):
        print(f"🟦 [Client] 로그인 시도: {email}")

        try:
            res = requests.post(
                f"{API_URL}/login",
                json={"email": email, "password": password},
                timeout=3
            )

            if res.status_code == 200:
                token = res.json()["access_token"]
                st.session_state["token"] = token
                st.session_state["logged_in"] = True
                print("🟢 [Client] 로그인 성공, 토큰 발급됨")
                st.success("로그인 성공!")
                st.rerun()
            else:
                print("🟥 [Client] 로그인 실패: 이메일/비밀번호 오류")
                st.error("이메일 또는 비밀번호가 틀렸습니다.")
        except requests.exceptions.RequestException as e:
            print("🟥 [Client] 로그인 요청 실패:", e)
            st.error("❌ 서버에 연결할 수 없습니다.")


# ✅ 항상 맨 처음에 세션 복구 시도 (단 1회)
print("🟦 [Client] >>> 앱 시작: restore_session_once() 호출")
restore_session_once()

# ✅ 상태에 따라 분기
if st.session_state.get("logged_in"):
    print("🟩 [Client] 상태 판단: 로그인됨 → 메인 페이지로")
    show_main_page()
else:
    print("🟥 [Client] 상태 판단: 로그인 안됨 → 로그인 페이지로")
    show_login_page()
