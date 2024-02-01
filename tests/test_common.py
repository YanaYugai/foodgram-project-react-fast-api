import http

def test_nonexistent_objects(url, client):
    response = client.get(url)
    assert response.status_code == http.HTTPStatus.NOT_FOUND, f'{url} доступен'
    assert response.json() == {"detail": "Страница не найдена."}
