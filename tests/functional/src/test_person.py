import pytest

#TEST_DATA_DIR = Path(__file__).parents[1].joinpath("testdata/expected_response")


@pytest.mark.asyncio
async def test_person_detailed(make_get_request, read_json_data):
    person_id = "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a"
    data = await read_json_data("person_detail.json")
    response = await make_get_request(f'/person/{person_id}', params={})
    assert response.body == data
    assert response.status == 200


@pytest.mark.asyncio
async def test_person_films(make_get_request, read_json_data):
    person_id = "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a"
    data = await read_json_data("person_films.json")
    response = await make_get_request(f'/person/{person_id}/film/', params={})
    assert response.body == data
    assert response.status == 200


@pytest.mark.asyncio
async def test_person_search(make_get_request, read_json_data):
    params = {'query': 'mario', 'page_number': 1, 'page_size': 10}
    data = await read_json_data("person_search.json")
    response = await make_get_request(f'/person/search/?', params=params)
    assert response.body == data
    assert response.status == 200


@pytest.mark.asyncio
async def test_person_list(make_get_request, read_json_data):
    params = {'page_number': 1, 'page_size': 12}
    response = await make_get_request(f'/person/', params=params)
    assert len(response.body) == 12
    assert response.status == 200
