from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch

print("🟡 [LLaMA 서비스] 모델 초기화 시작...")

model_id = "meta-llama/Llama-2-7b-chat-hf"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    device_map="auto",
)

print("✅ [LLaMA 서비스] 모델 및 토크나이저 로딩 완료")

# 텍스트 생성 파이프라인
generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
)

print("✅ [LLaMA 서비스] 파이프라인 준비 완료")

def generate_text(prompt: str, max_new_tokens=64, temperature=0.7, do_sample=True) -> str:
    print(f"🧠 [LLaMA] 프롬프트 수신: {prompt}")
    outputs = generator(
        prompt,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        do_sample=do_sample
    )

    result = outputs[0]["generated_text"]
    print(f"🟢 [LLaMA 서비스] 결과 생성 완료")
    return result
