from functools import lru_cache
from typing import Optional, List

from aioredis import Redis
from fastapi import Depends
from pydantic import BaseModel

from db.elastic import get_elastic, AsyncDataProvider
from db.redis import get_redis
from models.data_models import Person
from services.tools import CacheValue, ServiceMixin


PERSON_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут
FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class ListCache(BaseModel):
    __root__: List[str]


class PersonService(ServiceMixin):
    def __init__(self, redis: Redis, async_data_provider: AsyncDataProvider):
        self.redis = redis
        self.async_data_provider = async_data_provider
        self._index_name = "persons"

    async def get_by_id(self, person_id: str) -> Optional[Person]:
        cache_key = self._build_cache_key(
            [CacheValue(name="person_id", value=person_id)]
        )
        person = await self._person_from_cache(cache_key)
        if not person:
            person_data: dict = await self.async_data_provider.get_by_id(
                self._index_name, person_id
            )
            if not person_data:
                return None

            person: Person = Person(**person_data)
            await self._put_person_to_cache(cache_key, person)
        return person

    async def get_list(self) -> Optional[List[Person]]:
        doc = await self.async_data_provider.get_all_data(
            index=self._index_name,
            sort="",
            filter="",
        )
        return [Person(**d) for d in doc]

    async def search(self, query: str) -> Optional[List[Person]]:

        cache_key = self._build_cache_key([CacheValue(name="query", value=query)])
        persons: List[Person] = await self._get_list_from_cache(cache_key)
        if not persons:
            doc: list[dict] = await self.async_data_provider.search(
                index=self._index_name,
                query=query,
            )
            persons = [Person(**d) for d in doc]
            await self._put_list_to_cache(cache_key, persons)
        return persons

    async def _get_list_from_cache(self, cache_key: str) -> Optional[List[Person]]:
        data: str = await self.redis.get(cache_key)

        if not data:
            return None

        data_list: ListCache = ListCache.parse_raw(data)
        persons: list[Person] = [
            Person.parse_raw(p_data) for p_data in data_list.__root__
        ]
        return persons

    async def _person_from_cache(self, person_id: str) -> Optional[Person]:
        data = await self.redis.get(person_id)
        if not data:
            return None
        person = Person.parse_raw(data)
        return person

    async def _put_person_to_cache(self, cache_key: str, person: Person):
        await self.redis.set(
            cache_key, person.json(), expire=PERSON_CACHE_EXPIRE_IN_SECONDS
        )

    async def _put_list_to_cache(self, cache_key: str, persons: List[Person]):
        data = [f.json() for f in persons]
        data_row = ListCache.parse_obj(data).json()
        await self.redis.set(cache_key, data_row, expire=FILM_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_person_service(
    redis: Redis = Depends(get_redis),
    async_data_provider: AsyncDataProvider = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, async_data_provider)
