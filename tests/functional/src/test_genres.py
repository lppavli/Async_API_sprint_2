import pytest


@pytest.mark.asyncio
async def test_genre_detailed(make_get_request, read_json_data):
    genre_id = "fb58fd7f-7afd-447f-b833-e51e45e2a778"
    data = await read_json_data("genre_detail.json")
    response = await make_get_request(f"/genre/{genre_id}", params={})
    assert response.body == data
    assert response.status == 200


@pytest.mark.asyncio
async def test_genre_list(make_get_request, read_json_data):
    params = {"page_number": 3, "page_size": 10}
    response = await make_get_request(f"/genre/", params=params)
    assert len(response.body) == 6
    assert response.status == 200
