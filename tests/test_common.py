import http
import pytest


@pytest.mark.parametrize("url", ['/api/recipes/100/', '/api/tags/100/', '/api/ingredients/1000/'])
def test_nonexistent_objects(url, client):
    response = client.get(url)
    assert response.status_code == http.HTTPStatus.NOT_FOUND, f'{url} доступен'
    assert response.json() == {"detail": "Страница не найдена."}


@pytest.mark.parametrize("url", ['/api/recipes/download_shopping_cart/', '/api/users/subscriptions/'])
def test_permission_denied(url, client):
    response = client.get(url=url, headers={"Authorization": "Token invalid_token"})
    assert response.status_code == http.HTTPStatus.UNAUTHORIZED, f'{url} доступен'
    assert response.json() == {
        "detail": "Учетные данные не были предоставлены."
    }
