from fastapi import FastAPI
from routers import stt

app = FastAPI()

app.include_router(stt.router)
