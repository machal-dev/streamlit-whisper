from fastapi import FastAPI
from backend.llama_pack.router import router as llama_router
from backend.whisper_pack.router import router as whisper_router

app = FastAPI()

# llama
app.include_router(llama_router, prefix="/llama")
# whisper
app.include_router(whisper_router, prefix="/whisper")