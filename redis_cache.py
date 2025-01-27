from redis.asyncio import Redis

redis = None

async def init_redis():
    global redis
    if not redis:
        redis = await Redis.from_url("redis://127.0.0.1:6379")

async def get_file_id(tiktok_url: str) -> str:
    await init_redis()
    return await redis.get(tiktok_url)

async def set_file_id(tiktok_url: str, file_id: str, expire_seconds: int = 86400):
    await init_redis()
    await redis.set(tiktok_url, file_id, ex=expire_seconds)

async def delete_file_id(tiktok_url: str):
    await init_redis()
    await redis.delete(tiktok_url)

async def clear_redis_cache():
    await init_redis()
    await redis.flushdb()
    return True