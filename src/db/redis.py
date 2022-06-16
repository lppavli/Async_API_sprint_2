from abc import ABC, abstractmethod
from typing import Optional

from aioredis import Redis


class BaseCache(ABC):
    @abstractmethod
    def set(self, key, data, expire):
        pass

    @abstractmethod
    def get(self, key):
        pass


class RedisCache(BaseCache):
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    async def get(self, key: str) -> Optional[dict]:
        data = await self.redis_client.get(key=key)
        if not data:
            return None
        return data

    async def set(self, key: str, value: str, expire: int):
        await self.redis_client.set(key=key, value=value, expire=expire)


redis: Optional[BaseCache] = None


# Функция понадобится при внедрении зависимостей
async def get_redis() -> BaseCache:
    return redis
