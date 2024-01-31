from tests.test_recipes import client
from tests.utils import test_nonexistent_objects
from tests.example_responses import users, users_create


# TODO: when db will be ready add assert response.json
def test_add_recipe():
    response = client.post(
        '/api/recipes/1/favorite/',
        headers={"Authorization": "Token TOKENVALUE"},
    )
    assert response.status_code == 201


def test_add_recipe_twice():
    response = client.post(
        '/api/recipes/1/favorite/',
        headers={"Authorization": "Token TOKENVALUE"},
    )
    assert response.status_code == 400
    assert response.json == {
        "errors": "string"
    }


def test_add_recipe_failure_credentials():
    response = client.post(
        '/api/recipes/2/favorite/',
        headers={"Authorization": "Token invalid_token"},
    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Учетные данные не были предоставлены."
    }

def test_delete_recipe():
    response = client.delete(
        '/api/recipes/1/favorite/',
        headers={"Authorization": "Token TOKENVALUE"},
    )
    assert response.status_code == 204


def test_delete_recipe_twice():
    response = client.delete(
        '/api/recipes/1/favorite/',
        headers={"Authorization": "Token TOKENVALUE"},
    )
    assert response.status_code == 400
    assert response.json == {
        "errors": "string"
    }


def test_delete_recipe_failure_credentials():
    response = client.delete(
        '/api/recipes/2/favorite/',
        headers={"Authorization": "Token invalid_token"},
    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Учетные данные не были предоставлены."
    }
