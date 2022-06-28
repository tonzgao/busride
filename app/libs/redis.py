from arq import create_pool
from ..settings.arq import settings as redis_settings


async def get_redis():
    redis = await create_pool(redis_settings)
    return redis
