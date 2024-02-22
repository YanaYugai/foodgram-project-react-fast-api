from http import HTTPStatus
import pytest


@pytest.mark.parametrize(
    "url",
    ['/api/recipes/100/', '/api/tags/100/', '/api/ingredients/1000/'],
)
def test_nonexistent_objects(url, client):
    response = client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND, f'{url} доступен'
    assert response.json() == {"detail": "Страница не найдена."}


@pytest.mark.parametrize(
    "url",
    ['/api/recipes/download_shopping_cart/', '/api/users/subscriptions/'],
)
def test_permission_denied(url, client):
    response = client.get(
        url=url,
        headers={"Authorization": "Token invalid_token"},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED, f'{url} доступен'
    assert response.json() == {
        "detail": "Учетные данные не были предоставлены.",
    }


@pytest.mark.parametrize(
    "url",
    ['/api/users/', 'api/recipes/', '/api/users/subscriptions/'],
)
def test_paginator(url, client):
    raise NotImplementedError


def test_filters(client, url='api/recipes/'):
    raise NotImplementedError
