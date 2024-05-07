import http


def test_get_ingredients(client):
    response = client.get('/api/ingredients/?name=ягнятина')
    assert response.status_code == http.HTTPStatus.OK


def test_get_tag(client):
    response = client.get('/api/ingredients/1/')
    assert response.status_code == http.HTTPStatus.OK
