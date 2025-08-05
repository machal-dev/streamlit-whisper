from fastapi import APIRouter
from pydantic import BaseModel, Field
from backend.llama_pack.service import generate_text
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str = Field(..., description="사용자 프롬프트 (예: '삼국지를 요약해줘')")
    max_new_tokens: int = Field(64, description="생성할 최대 토큰 수")
    temperature: float = Field(0.7, description="창의성 정도 (0~1)")
    do_sample: bool = Field(True, description="샘플링 여부")
    extract_after_answer: bool = Field(True, description="'답:' 이후만 추출할지 여부")

@router.post("/generate")
def llama_generate(req: PromptRequest):
    logger.info("🟦 [API] POST /llama/generate 요청 수신")
    logger.debug(f"[프롬프트] {req.prompt[:100]}...")

    result = generate_text(
        prompt=req.prompt,
        max_new_tokens=req.max_new_tokens,
        temperature=req.temperature,
        do_sample=req.do_sample,
        extract_after_answer=req.extract_after_answer
    )

    logger.info("🟢 [API] LLaMA 응답 생성 완료")
    return {"result": result}
