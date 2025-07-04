from fastapi import FastAPI
from routers import user, auth, stt

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(stt.router)
