import logging
import aioredis
import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api.v1 import films, person, genre
from src.core.config import settings
from src.db import elastic, redis
from src.db.redis import RedisCache

app = FastAPI(
    title="Read-only API для онлайн-кинотеатра",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    description="Информация о фильмах, жанрах и людях, участвовавших в создании произведения",
    version="1.0.0",
)


@app.on_event("startup")
async def startup():
    redis_client = await aioredis.create_redis_pool(
        (settings.REDIS_HOST, settings.REDIS_PORT), minsize=10, maxsize=20
    )
    redis.redis = RedisCache(redis_client)
    elastic_client = AsyncElasticsearch(
        hosts=[f"{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}"]
    )
    elastic.es = elastic.AsyncElasticProvider(elastic_client)
    logging.info("Service up")


@app.on_event("shutdown")
async def shutdown():
    redis.redis.close()
    await redis.redis.wait_closed()
    await elastic.es.close()


app.include_router(films.router, prefix="/api/v1/films", tags=["films"])
app.include_router(person.router, prefix="/api/v1/person", tags=["person"])
app.include_router(genre.router, prefix="/api/v1/genre", tags=["genre"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
    )
