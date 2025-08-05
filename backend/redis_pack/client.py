### 📦 backend/redis_pack/client.py

import os
import redis
from dotenv import load_dotenv

load_dotenv()

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

# 예제 - 단독 실행 시 테스트
if __name__ == "__main__":
    redis_client.set("ping", "pong")
    print("✅ Redis 테스트 결과:", redis_client.get("ping"))
