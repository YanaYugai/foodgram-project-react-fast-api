from tests.example_responses import recipes
import http


dict_1 = {
    "ingredients": [{"id": 1, "amount": 10}],
    "tags": [1],
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
    "name": "string",
    "text": "string",
    "cooking_time": 1,
}


def test_create_recipe_success(client):
    response = client.post(
        url="/api/recipes/",
        headers={"Authorization": "Token TOKENVALUE"},
        json=dict_1,
    )
    assert response.status_code == http.HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "tags": [
            {
                "id": 1,
                "name": "Обед",
                "color": "#E26C2D",
                "slug": "lunch",
            },
        ],
        "author": {
            "email": "user_1@example.com",
            "id": 0,
            "username": "petya",
            "first_name": "Петя",
            "last_name": "Пупкин",
            "is_subscribed": False,
        },
        "ingredients": [
            {
                "id": 1,
                "name": "Картошка",
                "measurement_unit": "кг",
                "amount": 10,
            },
        ],
        "is_favorited": True,
        "is_in_shopping_cart": True,
        "name": "string",
        "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
        "text": "string",
        "cooking_time": 1,
    }


def test_create_recipe_bad_request(client):
    response = client.post(
        url="/api/recipes/",
        headers={"Authorization": "Token TOKENVALUE"},
        json={
            "tags": [1],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            "name": "string",
            "text": "string",
            "cooking_time": 1,
        },
    )
    assert response.status_code == http.HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Не все данные были представлены"}


def test_create_recipe_failure(client):
    response = client.post(
        url="/api/recipes/",
        headers={"Authorization": "Token invalid_token"},
        json={
            "ingredients": [{"id": 11, "amount": 10}],
            "tags": [2],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            "name": "string",
            "text": "string",
            "cooking_time": 1,
        },
    )
    assert response.status_code == http.HTTPStatus.UNAUTHORIZED
    assert response.json() == {
        "detail": "Учетные данные не были предоставлены.",
    }


def test_get_recipe(client):
    response = client.get('/api/recipes/1')
    assert response.status_code == http.HTTPStatus.OK
    assert response.json() == recipes[1]


def test_update_recipe(client):
    response = client.patch(
        "/api/recipes/1/",
        headers={"Authorization": "Token TOKENVALUE"},
        json={
            "ingredients": [{"id": 1123, "amount": 10}],
            "tags": [3],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            "name": "string",
            "text": "string",
            "cooking_time": 1,
        },
    )
    assert response.status_code == http.HTTPStatus.OK
    assert response.json() == recipes[1]


# TODO: refactoring required
def test_update_recipe_uncorrect_value(client):
    "Невозможно обновить рецепт с переданными некорректными данными"
    json = {
        "ingredients": [{"id": 1123, "amount": 10}],
        "tags": [3],
        "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
        "name": "string",
        "text": "string",
        "cooking_time": 1,
    }
    list_value = list(json.keys())
    for key in list_value:
        value = json[key]
        del json[key]
        response = client.patch(
            "/api/recipes/1/",
            headers={"Authorization": "Token TOKENVALUE"},
            json=json,
        )
        assert (
            response.status_code == http.HTTPStatus.BAD_REQUEST
        ), "Возможно изменить рецепт без необходимого поля"
        assert response.json() == {"detail": "Не все данные были представлены"}
        json[key] = value

    response = client.patch(
        "/api/recipes/1/",
        headers={"Authorization": "Token TOKENVALUE"},
        json={
            "ingredients": [{"id": 112, "amount": 0}],
            "tags": [3],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            "name": "string",
            "text": "string",
            "cooking_time": 0,
        },
    )
    assert (
        response.status_code == http.HTTPStatus.BAD_REQUEST
    ), "Возможно изменить рецепт с некорректным количеством ингридиентов"
    assert response.json() == {"detail": "Не все данные были представлены"}


def test_delete_recipe(client):
    response = client.delete(
        '/api/recipes/1/',
        headers={"Authorization": "Token TOKENVALUE"},
    )
    assert response.status_code == http.HTTPStatus.NO_CONTENT


def test_delete_nonexistent_recipe(client):
    response = client.delete(
        '/api/recipes/100',
        headers={"Authorization": "Token TOKENVALUE"},
    )
    assert response.status_code == http.HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Страница не найдена."}
