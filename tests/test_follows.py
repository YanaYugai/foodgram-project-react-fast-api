import http

from sqlalchemy.orm import Session

from backend.src.crud import services
from backend.src.users.schemas import UserCreation


def test_add_follow_correct(
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
    assert "recipes" in response_following
    assert "recipes_count" in response_following
    assert "is_subscribed" in response_following


def test_get_following_correct(
    client,
    following_with_5_recipes,
):
    user_id, headers = following_with_5_recipes
    subscribtion = client.get(
        '/api/users/subscriptions/?page=1&limit=6',
        headers=headers,
    )
    response_following = subscribtion.json()
    assert subscribtion.status_code == http.HTTPStatus.OK
    assert user_id == response_following["results"][0]['id']
    assert "is_subscribed" in response_following["results"][0]


def test_get_following_failure_credentials(
    client,
    following,
):
    _, headers = following
    subscribtion = client.get(
        '/api/users/subscriptions/',
        headers=headers,
    )
    response = client.get(
        '/api/users/subscriptions/',
        headers={"Authorization": "Token invalid_token"},
    )
    assert subscribtion.status_code == http.HTTPStatus.OK
    assert response.status_code == http.HTTPStatus.UNAUTHORIZED
    assert response.json() == {
        "detail": "Учетные данные не были предоставлены.",
    }


def test_add_follow_twice(
    client,
    following,
):
    user_id, headers = following
    response = client.post(
        f'/api/users/{user_id}/subscribe/',
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


def test_delete_follow(
    client,
    headers,
    following,
):
    user_id, headers = following
    response = client.delete(
        f'/api/users/{user_id}/subscribe/',
        headers=headers,
    )
    assert response.status_code == http.HTTPStatus.NO_CONTENT


def test_delete_follow_twice(
    client,
    following,
):
    user_id, headers = following
    response = client.delete(
        f'/api/users/{user_id}/subscribe/',
        headers=headers,
    )
    response = client.delete(
        f'/api/users/{user_id}/subscribe/',
        headers=headers,
    )
    assert response.status_code == http.HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Пользователь не подписан."}


def test_delete_follow_failure_credentials(
    client,
    following,
):
    user_id, _ = following
    response = client.delete(
        f'/api/users/{user_id}/subscribe/',
        headers={"Authorization": "Token invalid_token"},
    )
    assert response.status_code == http.HTTPStatus.UNAUTHORIZED
    assert response.json() == {
        "detail": "Учетные данные не были предоставлены.",
    }
