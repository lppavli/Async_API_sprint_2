from http import HTTPStatus

import pytest

from testdata.data_to_elastic import movies


@pytest.mark.asyncio
async def test_film_detailed(create_index, make_get_request):
    data = movies[0]
    film_id = data['id']
    response = await make_get_request(f"/films/{film_id}", params={})
    assert response.body["id"] == data["id"]
    assert response.status == HTTPStatus.OK
    assert response.body['title'] == data['title']
    # assert response.body['rating'] == data['rating']
    assert response.body['genres'] == data['genres']
    assert response.body['actors'] == data['actors']
    assert response.body['writers'] == data['writers']
    assert response.body['directors'] == data['directors']


@pytest.mark.asyncio
async def test_get_film(make_get_request):
    response = await make_get_request("/films/unknown")
    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body["detail"] == "film not found"


@pytest.mark.asyncio
async def test_film_search(make_get_request, read_json_data):
    params = {"query": "star", "page": 1, "size": 50}
    response = await make_get_request(f"/films/search/?", params=params)
    data = await read_json_data("filmsearch.json")
    assert response.body['items'] == data
    assert response.body["total"] == 3
    assert response.body["page"] == 1
    assert response.body["size"] == 50


# @pytest.mark.asyncio
# async def test_film_list(make_get_request):
#     params = {"page": 1, "size": 50, "filter": "Action"}
#     response = await make_get_request(f"/films/", params=params)
#     assert response.body["total"] == 10
#     assert response.body["page"] == 1
#     assert response.body["size"] == 50
#
#
# @pytest.mark.asyncio
# async def test_film_detailed(make_get_request, read_json_data):
#     film_id = "fe12e428-be67-4bb9-9629-4ab1385dc8be"
#     data = await read_json_data("film_detail.json")
#     response = await make_get_request(f"/films/{film_id}", params={})
#     assert response.body == data
#     assert response.status == 200
#
#
# @pytest.mark.asyncio
# async def test_get_film(make_get_request):
#     response = await make_get_request("/films/unknown")
#     assert response.status == 404
#     assert response.body["detail"] == "film not found"
#
#
# @pytest.mark.asyncio
# async def test_film_search(make_get_request):
#     params = {"query": "captain", "page": 1, "size": 50}
#     response = await make_get_request(f"/films/search/?", params=params)
#     assert response.body["total"] == 10
#     assert response.body["page"] == 1
#     assert response.body["size"] == 50
