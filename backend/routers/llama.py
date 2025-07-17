from fastapi import APIRouter
from pydantic import BaseModel
from services.llama_service import generate_text

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 64
    temperature: float = 0.7
    do_sample: bool = True

@router.post("/llama/generate")
def llama_generate(req: PromptRequest):
    print("🟦 [API] POST /llama/generate 요청 수신")
    result = generate_text(req.prompt)
    print("🟢 [API] 응답 반환 준비 완료")
    return {"result": result}
