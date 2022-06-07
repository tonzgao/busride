import aioredis  # TODO: update to v2
from ..settings.globals import REDIS_IP, REDIS_PORT


async def get_redis():
    redis = await aioredis.create_pool((REDIS_IP, REDIS_PORT))
    return redis
