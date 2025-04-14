import asyncio
from redis.asyncio import Redis
from core.settings import settings

redis: Redis = None


async def init_redis():
    global redis

    retries = 10
    while retries:
        try:
            redis = Redis.from_url(
                settings.redis.redis_url,
                encoding="utf-8",
                decode_responses=True
            )
            # Проверка соединения
            await redis.ping()
            print("Redis connected successfully.")
            break
        except Exception as exc:
            retries -= 1
            print(f"REDIS UNAVAILABLE: {exc}. Retrying in 3 seconds...")
            await asyncio.sleep(3)


async def close_redis():
    if redis:
        await redis.close()
        print("Redis connection closed.")
