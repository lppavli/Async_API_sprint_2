from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_person_detailed(make_get_request, read_json_data):
    person_id = "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a"
    data = await read_json_data("person_detail.json")
    response = await make_get_request(f"/person/{person_id}", params={})
    assert response.body == data
    assert response.status == HTTPStatus.OK


@pytest.mark.asyncio
async def test_person_films(make_get_request, read_json_data):
    person_id = "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a"
    data = await read_json_data("person_films.json")
    response = await make_get_request(f"/person/{person_id}/film/", params={})
    assert response.body == data
    assert response.status == HTTPStatus.OK


@pytest.mark.asyncio
async def test_person_search(make_get_request, read_json_data):
    params = {"query": "mario", "page": 1, "size": 50}
    response = await make_get_request(f"/person/search/?", params=params)
    assert response.body["total"] == 10
    assert response.body["page"] == 1
    assert response.body["size"] == 50


@pytest.mark.asyncio
async def test_person_list(make_get_request, read_json_data):
    params = {"page_number": 1, "page_size": 10}
    response = await make_get_request(f"/person/", params=params)
    assert len(response.body["items"]) == 10
    assert response.status == HTTPStatus.OK


@pytest.mark.asyncio
async def test_get_person(make_get_request):
    response = await make_get_request("/person/unknown")
    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body["detail"] == "person not found"
