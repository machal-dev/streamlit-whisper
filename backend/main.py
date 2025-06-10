from fastapi import FastAPI
from routers import auth, stt, test

app = FastAPI()

app.include_router(auth.router)
app.include_router(stt.router)
app.include_router(test.router)