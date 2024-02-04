import http


# TODO: when db will be ready add assert response.json
def test_add_follow(client):
    response = client.post(
        '/api/users/1/subscribe/',
        headers={"Authorization": "Token TOKENVALUE"},
    )
    assert response.status_code == http.HTTPStatus.CREATED


def test_add_follow_twice(client):
    response = client.post(
        '/api/recipes/1/subscribe/',
        headers={"Authorization": "Token TOKENVALUE"},
    )
    assert response.status_code == http.HTTPStatus.BAD_REQUEST
    assert response.json() == {"errors": "string"}


def test_add_follow_failure_credentials(client):
    response = client.post(
        '/api/recipes/2/subscribe/',
        headers={"Authorization": "Token invalid_token"},
    )
    assert response.status_code == http.HTTPStatus.UNAUTHORIZED
    assert response.json() == {
        "detail": "Учетные данные не были предоставлены."
    }


def test_delete_follow(client):
    response = client.delete(
        '/api/recipes/2/subscribe/',
        headers={"Authorization": "Token TOKENVALUE"},
    )
    assert response.status_code == http.HTTPStatus.NO_CONTENT


def test_delete_follow_twice(client):
    response = client.delete(
        '/api/recipes/2/subscribe/',
        headers={"Authorization": "Token TOKENVALUE"},
    )
    assert response.status_code == http.HTTPStatus.BAD_REQUEST
    assert response.json() == {"errors": "string"}


def test_delete_follow_failure_credentials(client):
    response = client.delete(
        '/api/recipes/2/subscribe//1/subscribe/',
        headers={"Authorization": "Token invalid_token"},
    )
    assert response.status_code == http.HTTPStatus.UNAUTHORIZED
    assert response.json() == {
        "detail": "Учетные данные не были предоставлены."
    }


def test_get_follows(client):
    raise NotImplementedError


def test_add_follows_on_me(client):
    raise NotImplementedError