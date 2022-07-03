from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_genre_detailed(make_get_request, read_json_data):
    genre_id = "fb58fd7f-7afd-447f-b833-e51e45e2a778"
    data = await read_json_data("genre_detail.json")
    response = await make_get_request(f"/genre/{genre_id}", params={})
    assert response.body == data
    assert response.status == HTTPStatus.OK


@pytest.mark.asyncio
async def test_get_genre(make_get_request):
    response = await make_get_request("/genre/unknown")
    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body["detail"] == "genre not found"


@pytest.mark.asyncio
async def test_genre_list(make_get_request, read_json_data):
    params = {"page": 1, "size": 10}
    response = await make_get_request(f"/genre/", params=params)
    assert response.body["total"] == 10
    assert response.body["page"] == 1
    assert response.body["size"] == 10
