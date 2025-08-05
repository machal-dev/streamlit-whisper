# ✅ llama_pack/controller.py
"""
LLaMA 모델 컨트롤러
- 모델 로딩, 언로딩, 상태 확인 (Lazy Loading)
"""

import logging
import torch
from backend.llama_pack import config
from transformers import AutoTokenizer, pipeline
from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig

logger = logging.getLogger(__name__)

# 전역 상태 저장용
_model = None
_tokenizer = None
_generator = None
_is_loaded = False

def load_model():
    global _model, _tokenizer, _generator, _is_loaded

    if _is_loaded:
        logger.info(f"{config.LOG_TAG} 🔄 이미 로딩된 모델 사용")
        return

    logger.info(f"{config.LOG_TAG} 🟡 모델 로딩 시작...")

    _tokenizer = AutoTokenizer.from_pretrained(config.MODEL_ID, use_fast=True)

    quantize_config = BaseQuantizeConfig(
        bits=4,
        group_size=128,
        desc_act=False
    )

    _model = AutoGPTQForCausalLM.from_pretrained(
        config.MODEL_ID,
        quantize_config=quantize_config,
        use_safetensors=True,
        trust_remote_code=True,
        # GPTQ 모델을 불러올 때는 device를 from_pretrained()에 직접 넘기면 안 되고, pipeline() 쪽에서 처리
        # device=config.DEVICE
    )

    _generator = pipeline(
        "text-generation",
        model=_model,
        tokenizer=_tokenizer,
        device=0  # 또는 device_map="auto"
    )

    _is_loaded = True
    logger.info(f"{config.LOG_TAG} ✅ 모델 및 파이프라인 로딩 완료")

def unload_model():
    global _model, _tokenizer, _generator, _is_loaded

    if not _is_loaded:
        logger.info(f"{config.LOG_TAG} 🚫 언로드할 모델이 없습니다.")
        return

    del _model
    del _tokenizer
    del _generator
    torch.cuda.empty_cache()
    _is_loaded = False
    logger.info(f"{config.LOG_TAG} 🧹 모델 언로드 및 GPU 메모리 정리 완료")

def is_model_loaded() -> bool:
    return _is_loaded

def get_generator():
    if not _is_loaded:
        raise RuntimeError("LLaMA 모델이 로드되지 않았습니다. 먼저 load_model()을 호출하세요.")
    return _generator
