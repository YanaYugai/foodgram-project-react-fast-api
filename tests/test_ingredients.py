import http

from tests.example_responses import ingredients


def test_get_ingredients(client):
    response = client.get('/api/ingredients/')
    assert response.status_code == http.HTTPStatus.OK
    assert response.json() == list(ingredients.values())


def test_get_tag(client):
    response = client.get('/api/ingredients/1/')
    assert response.status_code == http.HTTPStatus.OK
    assert response.json() == ingredients[1]
