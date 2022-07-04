import json

from elasticsearch import Elasticsearch

from testdata.indexes import genres_index, movies_index, persons_index

genres = [
    {"id": "120a21cf-9097-479e-904a-13dd7198c1dd", "name": "Adventure", "description": None,
     "modified": "2021-06-16T20:14:09.309836+00:00"},
    {"id": "b92ef010-5e4c-4fd0-99d6-41b6456272cd", "name": "Fantasy", "description": None,
     "modified": "2021-06-16T20:14:09.309886+00:00"},
    {"id": "1cacff68-643e-4ddd-8f57-84b62538081a", "name": "Drama", "description": None,
     "modified": "2021-06-16T20:14:09.309981+00:00"
     }
]
movies = [
    {
        "id": "5fcc9125-7f11-41ad-8b52-179db5b89e08",
        "title": "Star Wars: Extintion",
        "description": None,
        "type": "movie",
        "creation_date": "2021-06-16T20:14:09.256104+00:00",
        "rating": "6.9",
        "modified": "2021-06-16T20:14:09.256120+00:00",
        "directors": [
            {
                "id": "93d29db7-6a25-437b-a557-1644e9d2ea02",
                "name": "Alejandro Beltrán"
            }
        ],
        "writers": [
            {
                "id": "312d5c13-5cbd-4aea-a062-6e0eac710e73",
                "name": "Ron Marz"
            }
        ],
        "actors": [
            {
                "id": "3d3ae035-8278-47a5-a8f6-c493ccf9ddd9",
                "name": "Jesús Marugán"
            },
            {
                "id": "6483591f-933a-4aca-a42e-76d06df60d1e",
                "name": "Natalia Gimeno"
            },
            {
                "id": "9a5eef64-4d80-4365-a869-83ed7694dbf5",
                "name": "Ángel Beltrán"
            },
            {
                "id": "ab933ce1-78cf-4407-9938-da2f63a5344e",
                "name": "Antonio Marí-Ruano"
            }
        ],
        "genres": [
            {
                "id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff",
                "name": "Action"
            },
            {
                "id": "a886d0ec-c3f3-4b16-b973-dedcf5bfa395",
                "name": "Short"
            },
            {
                "id": "b92ef010-5e4c-4fd0-99d6-41b6456272cd",
                "name": "Fantasy"
            }
        ]
    },
    {
        "id": "c241874f-53d3-411a-8894-37c19d8bf010",
        "title": "Star Wars SC 38 Reimagined",
        "description": "\"Scene 38 ReImagined\" is about the final confrontation between Ben Kenobi and Darth Vader in \"A New Hope\" nearly 20 years after the events of \"Revenge Of The Sith.\" This is a one-off story ...",
        "type": "movie",
        "creation_date": "2021-06-16T20:14:09.256203+00:00",
        "rating": "9.5",
        "modified": "2021-06-16T20:14:09.256219+00:00",
        "directors": [
            {
                "id": "819d6587-4a88-4b25-b734-c894f7ce4ab0",
                "name": "Philip J Silvera"
            }
        ],
        "writers": [],
        "actors": [
            {
                "id": "3683c176-c96e-4850-ba76-3e3a0290bf3f",
                "name": "Dan Brown"
            },
            {
                "id": "b48dc19f-2dff-45bf-b7c8-b4d5fcca83ff",
                "name": "Richard Cetrone"
            }
        ],
        "genres": [
            {
                "id": "6c162475-c7ed-4461-9184-001ef3d9f26e",
                "name": "Sci-Fi"
            },
            {
                "id": "a886d0ec-c3f3-4b16-b973-dedcf5bfa395",
                "name": "Short"
            }
        ]
    },
    {
        "id": "140844e9-221f-4e89-838c-fac4f8ef2a9f",
        "title": "Hedy Lamarr: Secrets of a Hollywood Star",
        "description": None,
        "type": "movie",
        "creation_date": "2021-06-16T20:14:09.256300+00:00",
        "rating": "6.7",
        "modified": "2021-06-16T20:14:09.256315+00:00",
        "directors": [
            {
                "id": "5782e26f-62c8-4071-960d-be03ed030b47",
                "name": "Barbara Obermaier"
            },
            {
                "id": "666325e3-f098-40d3-b6d9-77d551836927",
                "name": "Fosco Dubini"
            },
            {
                "id": "a19557c4-9f2a-4481-b819-b311bb5c1cb4",
                "name": "Donatello Dubini"
            }
        ],
        "writers": [
            {
                "id": "5782e26f-62c8-4071-960d-be03ed030b47",
                "name": "Barbara Obermaier"
            },
            {
                "id": "666325e3-f098-40d3-b6d9-77d551836927",
                "name": "Fosco Dubini"
            }
        ],
        "actors": [
            {
                "id": "12f9fbc9-6146-46c5-ad34-bb70067dc6ba",
                "name": "Jan-Christopher Horak"
            },
            {
                "id": "152fc4e1-3065-436f-a5b9-61123241802a",
                "name": "Hans Janitschek"
            },
            {
                "id": "1ba6b635-642a-4778-8a43-3c93ceba9dd6",
                "name": "Lupita Tovar"
            },
            {
                "id": "90a50973-a345-47be-b912-b0071053418e",
                "name": "Hedy Lamarr"
            }
        ],
        "genres": [
            {
                "id": "6d141ad2-d407-4252-bda4-95590aaf062a",
                "name": "Documentary"
            }
        ]
    }
]
persons = [
    {
        "id": "712cad1d-96a7-45f0-986f-c80c030c6536",
        "name": "Sarah Rochelle",
        "modified": "2021-06-16T20:14:09.403156+00:00",
        "roles": "actor",
        "films": [
            {
                "id": "a9bbc1d8-bb8a-41d2-b61a-d8ddc9b31ede",
                "rating": "1.8",
                "title": "Amy Winehouse: Fallen Star",
                "type": "fw_type"
            }
        ]
    },
    {
        "id": "6b264344-44af-4feb-b0e1-24d07e962c65",
        "name": "Pokey Spears",
        "modified": "2021-06-16T20:14:09.403290+00:00",
        "roles": "actor, director",
        "films": [
            {
                "id": "92dcddff-a70e-497c-92dc-0da12d1d528a",
                "rating": "5.8",
                "title": "Exile: A Star Wars Story",
                "type": "fw_type"
            }
        ]
    },
    {
        "id": "befa69a6-65cd-477a-a3b2-d5adaa18cca7",
        "name": "Bria Roberts",
        "modified": "2021-06-16T20:14:09.403382+00:00",
        "roles": "actor",
        "films": [
            {
                "id": "92dcddff-a70e-497c-92dc-0da12d1d528a",
                "rating": "5.8",
                "title": "Exile: A Star Wars Story",
                "type": "fw_type"
            }
        ]
    }
]


def data_for_elastic():
    json_list = []
    for record in persons:
        index_info = {'index': {'_index': 'persons', '_id': record['id']}}
        json_list.append(index_info)
        json_list.append(record)
    for record in movies:
        index_info = {'index': {'_index': 'movies', '_id': record['id']}}
        json_list.append(index_info)
        json_list.append(record)
    for record in genres:
        index_info = {'index': {'_index': 'genres', '_id': record['id']}}
        json_list.append(index_info)
        json_list.append(record)

    json_list = '\n'.join(json.dumps(j) for j in json_list)
    json_list += '\n'
    return json_list


def main():
    es_client = Elasticsearch(f"localhost:9200")
    es_client.indices.create(index='genres', body=genres_index)
    es_client.indices.create(index='persons', body=persons_index)
    es_client.indices.create(index='movies', body=movies_index)
    index_data = {'movies': movies, 'genres': genres, 'persons': persons}
    for index, data in index_data.items():
        for d in data:
            es_client.index(index=index, id=d['id'], body=d, doc_type='_doc')


if __name__ == '__main__':
    main()
