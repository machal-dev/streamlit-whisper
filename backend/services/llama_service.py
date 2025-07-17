from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

# ✅ Meta 승인이 필요 없는 오픈모델
model_id = "NousResearch/Llama-2-7b-chat-hf"

# ✅ 토큰 인증 없이도 동작 (필요시 huggingface-cli login 먼저 해줘야 함)
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    device_map="auto"
)

# ✅ 텍스트 생성 파이프라인 구성
generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device_map="auto"
)

# 🔎 테스트 프롬프트
prompt = "한국의 수도는 어디인가요?\n답:"
outputs = generator(prompt, max_new_tokens=64, do_sample=True, temperature=0.7)

# 🔥 출력
print("🔥 결과:", outputs[0]["generated_text"])
