from functools import lru_cache
from typing import Optional

from fastapi import Depends

from db.elastic import get_elastic, AsyncDataProvider
from db.redis import get_redis, RedisCache, BaseCache
from models.data_models import Genre
from services.tools import CacheValue, ServiceMixin


GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class GenreService(ServiceMixin):
    def __init__(self, redis: RedisCache, async_data_provider: AsyncDataProvider):
        self.redis = redis
        self.async_data_provider = async_data_provider
        self._index_name = "genres"

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:

        cache_key = self._build_cache_key([CacheValue(name="genre_id", value=genre_id)])
        genre = await self.redis.get(cache_key)

        if not genre:
            genre_data: Optional[dict] = await self.async_data_provider.get_by_id(
                self._index_name, genre_id
            )
            if not genre_data:
                return None
            genre: Genre = Genre(**genre_data)
            await self.redis.set(
                key=cache_key, value=genre.json(), expire=GENRE_CACHE_EXPIRE_IN_SECONDS
            )
            return genre
        genre = Genre.parse_raw(genre)
        return genre

    async def get_list(self):
        data: list[dict] = await self.async_data_provider.get_all_data(
            index=self._index_name,
            sort="",
            filter="",
        )
        return [Genre(**d) for d in data]


@lru_cache()
def get_genre_service(
    redis: BaseCache = Depends(get_redis),
    async_data_provider: AsyncDataProvider = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, async_data_provider)
