from functools import lru_cache
from typing import Optional

from aioredis import Redis
from fastapi import Depends

from db.elastic import get_elastic, AsyncDataProvider
from db.redis import get_redis, RedisCache
from models.data_models import Film, FilmForPerson
from services.tools import CacheValue, ServiceMixin

from pydantic import BaseModel

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class ListCache(BaseModel):
    __root__: list[str]


class FilmService(ServiceMixin):
    def __init__(self, redis: RedisCache, async_data_provider: AsyncDataProvider):
        self.redis = redis
        self.async_data_provider = async_data_provider
        self._index_name = 'movies'

    async def get_by_id(self, film_id: str) -> Optional[Film]:

        cache_key = self._build_cache_key([CacheValue(name='film_id', value=film_id)])

        film = await self.redis.get(cache_key)
        if not film:
            film_data: Optional[dict] = await self.async_data_provider.get_by_id(self._index_name, film_id)
            if not film_data:
                return None
            film: Film = Film(**film_data)
            await self.redis.set(key=cache_key, value=film.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS)
            return film
        film = Film.parse_raw(film)
        return film

    async def get_all_films(
        self,
        sort: Optional[str],
        filter: Optional[str],
    ) -> list[FilmForPerson]:

        cache_key = self._build_cache_key(
            [
                CacheValue(name='sort', value=sort),
                CacheValue(name='filter', value=filter),
            ]
        )

        if not cache_key:
            cache_key = "all_films"

        films: Optional[list[FilmForPerson]] = await self._films_from_cache(cache_key)

        if not films:
            films_data: list[dict] = await self.async_data_provider.get_all_data(
                index=self._index_name,
                sort=sort,
                filter=filter,
            )
            films: list[FilmForPerson] = [FilmForPerson(**d) for d in films_data]
            await self._put_films_to_cache(cache_key, films)

        return films

    async def search(self, query: str) -> list[FilmForPerson]:
        cache_key = self._build_cache_key([CacheValue(name='query', value=query)])
        # films: list[FilmForPerson] = await self._films_from_cache(cache_key)
        films = await self.redis.get(cache_key)
        if not films:
            films_data: list[dict] = await self.async_data_provider.search(self._index_name, query)
            films: list[FilmForPerson] = [FilmForPerson(**d) for d in films_data]
            data = [f.json() for f in films]
            data_row = ListCache.parse_obj(data).json()
            await self.redis.set(cache_key, data_row, expire=FILM_CACHE_EXPIRE_IN_SECONDS)
            return films

        data_list: ListCache = ListCache.parse_raw(films)
        films: list[FilmForPerson] = [
            FilmForPerson.parse_raw(film_data) for film_data in data_list.__root__
        ]
        return films

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.redis.get(film_id)
        if not data:
            return None
        film = Film.parse_raw(data)
        return film

    async def _films_from_cache(self, cache_key: str) -> Optional[list[FilmForPerson]]:
        data: str = await self.redis.get(cache_key)

        if not data:
            return None

        data_list: ListCache = ListCache.parse_raw(data)
        films: list[FilmForPerson] = [
            FilmForPerson.parse_raw(film_data) for film_data in data_list.__root__
        ]
        return films


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    async_data_provider: AsyncDataProvider = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, async_data_provider)
