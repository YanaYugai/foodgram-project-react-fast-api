import http


def test_create_recipe_correct_credentials(
    client,
    headers: dict[str, str],
) -> None:
    response = client.post(
        url="/api/recipes/",
        headers=headers,
        json={
            "ingredients": [
                {"id": 11, "amount": 10},
            ],
            "tags": [1, 2],
            "image": "data:image/png",
            "name": "string",
            "text": "string",
            "cooking_time": 1,
        },
    )
    recipe = response.json()
    assert response.status_code == http.HTTPStatus.CREATED
    assert "tags" in recipe
    assert "author" in recipe
    assert "ingredients" in recipe
    assert "name" in recipe
    assert "image" in recipe
    assert "text" in recipe
    assert "cooking_time" in recipe
    # assert hasattr(recipe, "is_in_shopping_cart")


def test_create_recipe_bad_request(client, headers: dict[str, str]):
    response = client.post(
        url="/api/recipes/",
        headers=headers,
        json={
            "tags": [1],
            "image": "data:image/png;base64,",
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
            "image": "data:image/png;base64,",
            "name": "string",
            "text": "string",
            "cooking_time": 1,
        },
    )
    assert response.status_code == http.HTTPStatus.UNAUTHORIZED
    assert response.json() == {
        "detail": "Учетные данные не были предоставлены.",
    }


def test_get_recipe(client, recipe):
    recipe_response, _ = recipe
    response = client.get(f"/api/recipes/{recipe_response.get('id')}/")
    assert response.status_code == http.HTTPStatus.OK
    assert response.json() == recipe[0]


def test_update_recipe(client, recipe):
    recipe_response, headers = recipe
    response = client.patch(
        f"/api/recipes/{recipe_response.get('id')}/",
        headers=headers,
        json={
            "ingredients": [{"id": 1123, "amount": 10}],
            "tags": [3],
            "image": "data:image/png;base64,",
            "name": "string",
            "text": "string",
            "cooking_time": 1,
        },
    )
    assert response.status_code == http.HTTPStatus.OK
    # assert response.json() == recipes[1]


def test_update_recipe_uncorrect_value(client, recipe):
    "Невозможно обновить рецепт с переданными некорректными данными"
    recipe_response, headers = recipe
    response = client.patch(
        f"/api/recipes/{recipe_response.get('id')}/",
        headers=headers,
        json={
            "ingredients": [{"id": 112, "amount": 0}],
            "tags": [3],
            "image": "data:image/png;base64,",
            "name": "string",
            "text": "string",
            "cooking_time": 0,
        },
    )
    assert (
        response.status_code == http.HTTPStatus.BAD_REQUEST
    ), "Возможно изменить рецепт с некорректным количеством ингридиентов"
    assert response.json() == {"detail": "Не все данные были представлены"}


def test_delete_recipe(client, recipe):
    recipe_response, headers = recipe
    response = client.delete(
        f"/api/recipes/{recipe_response.get('id')}/",
        headers=headers,
    )
    assert response.status_code == http.HTTPStatus.NO_CONTENT


def test_delete_recipe_invalid_token(client, recipe):
    recipe_response, _ = recipe
    response = client.delete(
        f"/api/recipes/{recipe_response.get('id')}/",
        headers={"Authorization": "Token invalid_token"},
    )
    assert response.status_code == http.HTTPStatus.UNAUTHORIZED
    assert response.json() == {
        "detail": "Учетные данные не были предоставлены.",
    }


def test_delete_nonexistent_recipe(client, recipe):
    _, headers = recipe
    response = client.delete(
        '/api/recipes/100',
        headers=headers,
    )
    assert response.status_code == http.HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Страница не найдена."}
