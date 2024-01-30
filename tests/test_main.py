from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.temporary_db import users, recipes


client = TestClient(app)


def test_create_recipe():
    response = client.post(
        "/api/recipes/",
        headers={"Authorization": "Token TOKENVALUE"},
        json={
            "ingredients": [
                {
                    "id": 1123,
                    "amount": 10
                }
            ],
            "tags": [1,2],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            "name": "string",
            "text": "string",
            "cooking_time": 1
        }
    )
    assert response.status_code == 200
    assert response.json() == list(recipes)[:-1]


def test_create_recipe_failure():
    response = client.post(
        "/api/recipes/",
        headers={"Authorization": "Token invalid_token"},
        json={
            "ingredients": [
                {
                    "id": 11,
                    "amount": 10
                }
            ],
            "tags": [2],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            "name": "string",
            "text": "string",
            "cooking_time": 1
        }
    )
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Учетные данные не были предоставлены."
    }


def test_get_recipe():
    response = client.get('/api/recipes/1')
    assert response.status_code == 200
    assert response.json == recipes[1]


def test_update_recipe():
    response = client.patch(
        "/api/recipes/1/",
        headers={"Authorization": "Token TOKENVALUE"},
        json={
            "ingredients": [
                {
                    "id": 1123,
                    "amount": 10
                }
            ],
            "tags": [3],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            "name": "string",
            "text": "string",
            "cooking_time": 1
        }
    )
    assert response.status_code == 200
    assert response.json() == recipes[1]


def test_update_recipe_uncorrect_value():
    "Невозможно обновить рецепт с переданными некорректными данными"
    response = client.patch(
        "/api/recipes/1/",
        headers={"Authorization": "Token TOKENVALUE"},
        json={
            "ingredients": [
                {
                    "id": 112,
                    "amount": 0
                }
            ],
            "tags": [3],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            "name": "string",
            "text": "string",
            "cooking_time": 1
        }
    )
    assert response.status_code == 400, "Возможно изменить рецепт с некорректным количеством ингридиентов"
    assert response.json() == {
            "ingredients": [
                {
                    "id": 112,
                    "amount": [
                        "Убедитесь, что это значение больше либо равно 1."
                    ]
                },
            ],
}
    response = client.patch(
        "/api/recipes/1/",
        headers={"Authorization": "Token TOKENVALUE"},
        json={
            "tags": [3],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            "name": "string",
            "text": "string",
            "cooking_time": 1
        }
    )
    assert response.status_code == 400, "Возможно изменить рецепт без обязательного поля"
    assert response.json() == {
        "ingredients": [
            "Обязательное поле."
        ]
    }


def test_get_recipes():
    response = client.get(
        '/api/recipes/'
    )


