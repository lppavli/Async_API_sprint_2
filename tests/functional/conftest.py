import asyncio
import json
import time
from pathlib import Path

import aiohttp
import pytest

from typing import Optional
from dataclasses import dataclass
from multidict import CIMultiDictProxy
from elasticsearch import AsyncElasticsearch

from settings import settings
from src.load_data_for_test import load_data_for_test
from testdata.data_to_elastic import movies, genres, persons, data_for_elastic
from testdata.indexes import movies_index, persons_index, genres_index

TEST_DATA_DIR = Path(__file__).parent.joinpath("testdata/expected_response")


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope="session", autouse=True)
async def es_client():
    client = AsyncElasticsearch(
        hosts=f"{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}"
    )
    yield client
    await client.close()


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(session):
    async def inner(method: str, params: Optional[dict] = None) -> HTTPResponse:
        params = params or {}
        url = settings.SERVICE_URL + "/api/v1" + method
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture
async def read_json_data(request):
    async def inner(datafilename: str) -> dict:
        jsonpath = Path(TEST_DATA_DIR, datafilename)
        with jsonpath.open() as fp:
            data = json.load(fp)
        return data

    return inner


@pytest.fixture(scope='session')
async def create_index(es_client):
    await es_client.indices.create(index='genres', body=genres_index)
    await es_client.indices.create(index='persons', body=persons_index)
    await es_client.indices.create(index='movies', body=movies_index)
    await es_client.bulk(body=data_for_elastic())
    time.sleep(1)
    yield
    await es_client.indices.delete(index='_all')
    # await es_client.indices.delete(index='_all')
    # # await es_client.indices.delete(index='_all')
    # await es_client.indices.create(index='genres', body=genres_index)
    # await es_client.indices.create(index='persons', body=persons_index)
    # await es_client.indices.create(index='movies', body=movies_index)
    # index_data = {'movies': movies, 'genres': genres, 'persons': persons}
    # for index, data in index_data.items():
    #     for d in data:
    #         await es_client.index(index=index, id=d['id'], body=d, doc_type='_doc')

