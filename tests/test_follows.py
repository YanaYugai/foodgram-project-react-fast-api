import http

from sqlalchemy.orm import Session

from backend.src.crud import services
from backend.src.users.schemas import UserCreation


def test_add_follow(
    client,
    headers,
    clear_tables: Session,
    user_data: UserCreation,
):
    user = services.create_user(session=clear_tables, data=user_data)
    response = client.post(
        f'/api/users/{user.id}/subscribe/',
        headers=headers,
    )
    response_following = response.json()
    assert response.status_code == http.HTTPStatus.CREATED
    assert user.id == response_following['id']
    assert user.email == response_following['email']
    assert user.username == response_following['username']
    assert user.first_name == response_following['first_name']
    assert user.last_name == response_following['last_name']
    assert "is_subscribed" in response_following


def test_add_follow_twice(
    client,
    headers,
    clear_tables: Session,
    user_data: UserCreation,
):
    user = services.create_user(session=clear_tables, data=user_data)
    response = client.post(
        f'/api/users/{user.id}/subscribe/',
        headers=headers,
    )
    response = client.post(
        f'/api/users/{user.id}/subscribe/',
        headers=headers,
    )
    assert response.status_code == http.HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Некорректные данные."}


def test_add_follow_failure_credentials(
    client,
    clear_tables: Session,
    user_data: UserCreation,
):
    user = services.create_user(session=clear_tables, data=user_data)
    response = client.post(
        f'/api/users/{user.id}/subscribe/',
        headers={"Authorization": "Token invalid_token"},
    )
    assert response.status_code == http.HTTPStatus.UNAUTHORIZED
    assert response.json() == {
        "detail": "Учетные данные не были предоставлены.",
    }


def test_add_follow_on_self(
    client,
    token: str,
    clear_tables: Session,
):
    user = services.get_current_user(session=clear_tables, token=token)
    response = client.post(
        f'/api/users/{user.id}/subscribe/',
        headers={"Authorization": f"Token {token}"},
    )
    assert response.status_code == http.HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Некорректные данные."}


def test_delete_follow(client):
    raise NotImplementedError


def test_delete_follow_twice(client):
    raise NotImplementedError


def test_delete_follow_failure_credentials(client):
    raise NotImplementedError


def test_get_follows(client):
    raise NotImplementedError


def test_add_follows_on_me(client):
    raise NotImplementedError
