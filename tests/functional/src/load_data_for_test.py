import time

from elasticsearch import Elasticsearch

from testdata.data_to_elastic import movies, genres, persons
from testdata.indexes import movies_index, genres_index, persons_index


async def load_data_for_test(es_client):
    index_data = {'movies': movies, 'genres': genres, 'persons': persons}
    for index, data in index_data.items():
        for d in data:
            es_client.index(index=index, id=d['id'], body=d, doc_type='_doc')
    time.sleep(2)


if __name__ == '__main__':
    es_client = Elasticsearch(f"localhost:9200")
    load_data_for_test(es_client)