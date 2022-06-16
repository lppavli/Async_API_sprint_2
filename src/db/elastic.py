import abc
from typing import Optional
from elasticsearch import AsyncElasticsearch, NotFoundError


class AsyncDataProvider(abc.ABC):
    @abc.abstractmethod
    async def search(self, index: str, query: str):
        pass

    @abc.abstractmethod
    async def get_all_data(self, index: str, sort: str, filter: str):
        pass

    @abc.abstractmethod
    async def get_by_id(self, index: str, id: str) -> Optional[dict]:
        pass


class AsyncElasticProvider(AsyncDataProvider):
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_by_id(self, index: str, id: str) -> Optional[dict]:
        try:
            doc = await self.elastic.get(index, id)
        except NotFoundError:
            return None
        return doc["_source"]

    async def search(self, index: str, query: str) -> list[dict]:
        body = {"query": {"multi_match": {"query": query, "fuzziness": "auto"}}}
        return await self._search(index, body)

    async def get_all_data(self, index: str, sort: str, filter: str):
        body = {"query": {"bool": {"must": {"match_all": {}}}}}

        if sort:
            body["sort"] = [{f"{sort}": "desc"}, "_score"]

        if filter:
            body["query"]["bool"]["filter"] = {"match": {"genres.name": f"{filter}"}}

        return await self._search(index, body)

    async def _search(self, index: str, body: dict) -> list[dict]:
        response = await self.elastic.search(
            index=index,
            body=body,
        )
        return [d["_source"] for d in response["hits"]["hits"]]


es: Optional[AsyncDataProvider] = None


# Функция понадобится при внедрении зависимостей
async def get_elastic() -> AsyncDataProvider:
    return es
