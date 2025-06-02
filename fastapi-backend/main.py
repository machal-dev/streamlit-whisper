from fastapi import FastAPI
from routers import stt

app = FastAPI()
app.include_router(stt.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "FastAPI Whisper Backend Ready"}
