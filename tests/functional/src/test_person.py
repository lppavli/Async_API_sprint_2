from http import HTTPStatus

import pytest

from tests.functional.testdata.data_to_elastic import persons


@pytest.mark.asyncio
async def test_person_list(create_index, make_get_request, read_json_data):
    params = {"page_number": 1, "page_size": 50}
    response = await make_get_request(f"/person/", params=params)
    data = await read_json_data("personlist.json")
    assert response.status == HTTPStatus.OK
    assert response.body["items"] == data
    assert response.body["total"] == 3
    assert response.body["page"] == 1
    assert response.body["size"] == 50


@pytest.mark.asyncio
async def test_person_detailed(make_get_request, read_json_data):
    data = persons[0]
    person_id = data["id"]
    response = await make_get_request(f"/person/{person_id}", params={})
    assert response.status == HTTPStatus.OK
    assert response.body["id"] == data["id"]
    assert response.body["name"] == data["name"]
    assert [i["id"] for i in data["films"]] == [
        i["id"] for i in response.body["films_ids"]
    ]


@pytest.mark.asyncio
async def test_get_person(make_get_request):
    response = await make_get_request("/person/unknown")
    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body["detail"] == "person not found"


@pytest.mark.asyncio
async def test_person_search(make_get_request, read_json_data):
    params = {"query": "Sarah", "page": 1, "size": 50}
    response = await make_get_request(f"/person/search/?", params=params)
    assert response.status == HTTPStatus.OK
    data = await read_json_data("personsearch.json")
    assert response.body["items"] == data
    assert response.body["total"] == 1
    assert response.body["page"] == 1
    assert response.body["size"] == 50