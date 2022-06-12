from abc import ABC, abstractmethod
from typing import Optional

from aioredis import Redis
from fastapi import Depends

redis: Optional[Redis] = None


# Функция понадобится при внедрении зависимостей
async def get_redis() -> Redis:
    return redis


class BaseCache(ABC):
    @abstractmethod
    def set(self, key, data, expire):
        pass

    @abstractmethod
    def get(self, key):
        pass


class RedisCashe(BaseCache):
    def __init__(self, redis_client: Redis = Depends(get_redis)):
        self.redis_client = redis_client

    async def get(self, key: str) -> Optional[dict]:
        return await self.cache.get(key=key)

    async def set(self, key: str, value: str, expire: int):
        await self.cache.set(key=key, value=value, expire=expire)
