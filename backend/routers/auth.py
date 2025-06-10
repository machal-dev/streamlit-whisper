from fastapi import APIRouter, HTTPException
from backend.schemas.auth import LoginRequest, LoginResponse
from services.auth_service import authenticate_user, create_access_token

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def login(login_req: LoginRequest):
    if not authenticate_user(login_req.email, login_req.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(data={"sub": login_req.email})
    return {"access_token": token, "token_type": "bearer"}
