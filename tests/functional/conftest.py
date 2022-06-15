import json
from pathlib import Path

import aiohttp
import aioredis
import pytest

from typing import Optional
from dataclasses import dataclass
from multidict import CIMultiDictProxy
from elasticsearch import AsyncElasticsearch

SERVICE_URL = 'http://127.0.0.1:80'
REDIS_HOST = "localhost"
REDIS_PORT = 6379
TEST_DATA_DIR = Path(__file__).parent.joinpath("testdata/expected_response")


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope='session', autouse=True)
async def es_client():
    client = AsyncElasticsearch(hosts='127.0.0.1:9200')
    yield client
    await client.close()


@pytest.fixture(scope='function')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(session):
    async def inner(method: str, params: Optional[dict] = None) -> HTTPResponse:
        params = params or {}
        url = SERVICE_URL + '/api/v1' + method  # в боевых системах старайтесь так не делать!
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


# @pytest.mark.asyncio
# async def test_search_detailed(es_client, make_get_request):
#     # Заполнение данных для теста
#     await es_client.bulk(...)
#
#     # Выполнение запроса
#     response = await make_get_request('/search', {'search': 'Star Wars'})
#
#     # Проверка результата
#     assert response.status == 200
#     assert len(response.body) == 1
#
#     assert response.body == expected
