from http import HTTPStatus

import pytest

from tests.functional.testdata.data_to_elastic import genres


@pytest.mark.asyncio
async def test_genre_list(create_index, make_get_request, read_json_data):
    params = {"page": 1, "size": 50}
    response = await make_get_request(f"/genre/", params=params)
    assert response.status == HTTPStatus.OK
    data = await read_json_data("genrelist.json")
    assert response.body["items"] == data
    assert response.body["total"] == 3
    assert response.body["page"] == 1
    assert response.body["size"] == 50


@pytest.mark.asyncio
async def test_genre_detailed(create_index, make_get_request, read_json_data):
    data = genres[0]
    genre_id = data["id"]
    response = await make_get_request(f"/genre/{genre_id}", params={})
    assert response.status == HTTPStatus.OK
    assert response.body["id"] == data["id"]
    assert response.body["name"] == data["name"]
    assert response.body["description"] == data["description"]


@pytest.mark.asyncio
async def test_get_genre(make_get_request):
    response = await make_get_request("/genre/unknown")
    assert response.status == HTTPStatus.OK
    assert response.status == 404
    assert response.body["detail"] == "genre not found"
