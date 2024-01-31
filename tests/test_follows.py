from tests.test_recipes import client


# TODO: when db will be ready add assert response.json
def test_add_follow():
    response = client.post(
        '/api/users/1/subscribe/',
        headers={"Authorization": "Token TOKENVALUE"},
    )
    assert response.status_code == 201


def test_add_follow_twice():
    response = client.post(
        '/api/recipes/1/subscribe/',
        headers={"Authorization": "Token TOKENVALUE"},
    )
    assert response.status_code == 400
    assert response.json == {
        "errors": "string"
    }


def test_add_follow_failure_credentials():
    response = client.post(
        '/api/recipes/2/subscribe/',
        headers={"Authorization": "Token invalid_token"},
    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Учетные данные не были предоставлены."
    }


def test_delete_follow():
    response = client.delete(
        '/api/recipes/2/subscribe/',
        headers={"Authorization": "Token TOKENVALUE"},
    )
    assert response.status_code == 204


def test_delete_follow_twice():
    response = client.delete(
        '/api/recipes/2/subscribe/',
        headers={"Authorization": "Token TOKENVALUE"},
    )
    assert response.status_code == 400
    assert response.json == {
        "errors": "string"
    }


def test_delete_follow_failure_credentials():
    response = client.delete(
        '/api/recipes/2/subscribe//1/subscribe/',
        headers={"Authorization": "Token invalid_token"},
    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Учетные данные не были предоставлены."
    }


def test_get_follows():
    raise NotImplementedError


def test_add_follows_on_me():
    raise NotImplementedError
