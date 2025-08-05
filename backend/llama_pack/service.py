import logging
from backend.llama_pack.controller import load_model, get_generator

logger = logging.getLogger(__name__)

def generate_text(
    prompt: str,
    max_new_tokens: int = 64,
    temperature: float = 0.7,
    do_sample: bool = True,
    system_prompt: str = None,
    extract_after_answer: bool = True
) -> str:
    """
    LLaMA GPTQ 기반 텍스트 생성 함수
    """
    logger.debug(f"[🧠 LLaMA GPTQ] 프롬프트 수신:\n{prompt}")

    # Lazy 로딩
    load_model()
    generator = get_generator()

    final_prompt = prompt.strip()
    if system_prompt:
        final_prompt = f"{system_prompt.strip()}\n\n{prompt.strip()}"

    outputs = generator(
        final_prompt,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        do_sample=do_sample
    )

    result = outputs[0]["generated_text"]
    logger.debug("[📤 LLaMA GPTQ] 원본 응답:\n%s", result)

    if extract_after_answer and "답:" in result:
        result = result.split("답:", 1)[-1].strip()

    return result
