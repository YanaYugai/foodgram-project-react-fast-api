import http
import pytest


@pytest.mark.parametrize("url", ['/api/recipes/100/', '/api/tags/100/', '/api/ingredients/1000/'])
def test_nonexistent_objects(url, client):
    response = client.get(url)
    assert response.status_code == http.HTTPStatus.NOT_FOUND, f'{url} доступен'
    assert response.json() == {"detail": "Страница не найдена."}
