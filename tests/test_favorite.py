import http


# TODO: when db will be ready add assert response.json
def test_add_recipe(client):
    response = client.post(
        '/api/recipes/1/favorite/',
        headers={"Authorization": "Token TOKENVALUE"},
    )
    assert response.status_code == http.HTTPStatus.CREATED


def test_add_recipe_twice(client):
    response = client.post(
        '/api/recipes/1/favorite/',
        headers={"Authorization": "Token TOKENVALUE"},
    )
    assert response.status_code == http.HTTPStatus.BAD_REQUEST
    assert response.json() == {"errors": "string"}


def test_add_recipe_failure_credentials(client):
    response = client.post(
        '/api/recipes/2/favorite/',
        headers={"Authorization": "Token invalid_token"},
    )
    assert response.status_code == http.HTTPStatus.UNAUTHORIZED
    assert response.json() == {
        "detail": "Учетные данные не были предоставлены.",
    }


def test_delete_recipe(client):
    response = client.delete(
        '/api/recipes/1/favorite/',
        headers={"Authorization": "Token TOKENVALUE"},
    )
    assert response.status_code == http.HTTPStatus.NO_CONTENT


def test_delete_recipe_twice(client):
    response = client.delete(
        '/api/recipes/1/favorite/',
        headers={"Authorization": "Token TOKENVALUE"},
    )
    assert response.status_code == http.HTTPStatus.BAD_REQUEST
    assert response.json() == {"errors": "string"}


def test_delete_recipe_failure_credentials(client):
    response = client.delete(
        '/api/recipes/2/favorite/',
        headers={"Authorization": "Token invalid_token"},
    )
    assert response.status_code == http.HTTPStatus.UNAUTHORIZED
    assert response.json() == {
        "detail": "Учетные данные не были предоставлены.",
    }


def test_get_favorites(client):
    raise NotImplementedError
