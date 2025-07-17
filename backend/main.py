from fastapi import FastAPI
from routers import user, auth, stt, llama
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:8501"],  # Streamlit 실행 포트
#     allow_credentials=True,  # ← 이게 있어야 쿠키 허용됨!!
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(stt.router)
app.include_router(llama.router)
