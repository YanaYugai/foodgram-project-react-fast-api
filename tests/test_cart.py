from tests.test_recipes import client


# TODO: when db will be ready add assert response.json
def test_add_recipe():
    response = client.post(
        '/api/recipes/1/shopping_cart/',
        headers={"Authorization": "Token TOKENVALUE"},
    )
    assert response.status_code == 201


def test_add_recipe_twice():
    response = client.post(
        '/api/recipes/1/shopping_cart/',
        headers={"Authorization": "Token TOKENVALUE"},
    )
    assert response.status_code == 400
    assert response.json == {
        "errors": "string"
    }


def test_add_recipe_failure_credentials():
    response = client.post(
        '/api/recipes/2/shopping_cart/',
        headers={"Authorization": "Token invalid_token"},
    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Учетные данные не были предоставлены."
    }


def test_delete_recipe():
    response = client.delete(
        '/api/recipes/1/shopping_cart/',
        headers={"Authorization": "Token TOKENVALUE"},
    )
    assert response.status_code == 204


def test_delete_recipe_twice():
    response = client.delete(
        '/api/recipes/1/shopping_cart/',
        headers={"Authorization": "Token TOKENVALUE"},
    )
    assert response.status_code == 400
    assert response.json == {
        "errors": "string"
    }


def test_delete_recipe_failure_credentials():
    response = client.delete(
        '/api/recipes/2/shopping_cart/',
        headers={"Authorization": "Token invalid_token"},
    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Учетные данные не были предоставлены."
    }


def test_download_cart_failure_credentials():
    response = client.delete(
        '/api/recipes/download_shopping_cart/',
        headers={"Authorization": "Token invalid_token"},
    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Учетные данные не были предоставлены."
    }
