from fastapi import FastAPI
from routers import auth, stt

app = FastAPI()

app.include_router(auth.router)
app.include_router(stt.router)
