from web.core.redis_ import redis


class RedisService:
    @staticmethod
    async def cache_user_data(user_id: int, data: dict, ttl: int = 3600):
        key = f"user:{user_id}"
        await redis.set(key, data, ex=ttl)

    @staticmethod
    async def get_cached_user_data(user_id: int):
        key = f"user:{user_id}"
        return await redis.get(key)

    @staticmethod
    async def delete_cached_user_data(user_id: int):
        key = f"user:{user_id}"
        await redis.delete(key)
