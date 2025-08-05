import torch
import logging
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

logger = logging.getLogger(__name__)

logger.info("🟡 [LLaMA 서비스] 모델 초기화 시작...")

MODEL_ID = "meta-llama/Llama-2-7b-chat-hf"

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16,
    device_map="auto",
)

generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
)

logger.info("✅ [LLaMA 서비스] 모델 및 파이프라인 로딩 완료")


def generate_text(
    prompt: str,
    max_new_tokens: int = 64,
    temperature: float = 0.7,
    do_sample: bool = True,
    system_prompt: str = None,
    extract_after_answer: bool = True
) -> str:
    """
    LLaMA 텍스트 생성
    - prompt: 사용자 입력
    - extract_after_answer: '답:' 이후만 추출할지 여부
    """

    logger.debug(f"[🧠 LLaMA] 프롬프트 수신:\n{prompt}")

    final_prompt = prompt.strip()
    if system_prompt:
        final_prompt = system_prompt.strip() + "\n\n" + prompt.strip()

    outputs = generator(
        final_prompt,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        do_sample=do_sample
    )

    result = outputs[0]["generated_text"]

    logger.debug("[🟢 LLaMA] 원본 응답:\n%s", result)

    if extract_after_answer and "답:" in result:
        result = result.split("답:", 1)[-1].strip()

    return result
