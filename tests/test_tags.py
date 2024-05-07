import http


def test_get_tags(client):
    response = client.get('/api/tags/')
    assert response.status_code == http.HTTPStatus.OK


def test_get_tag(client):
    response = client.get('/api/tags/1/')
    assert response.status_code == http.HTTPStatus.OK
