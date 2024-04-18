import http


def test_add_recipe_favorite(
    client,
    recipe,
):
    recipe_response, headers = recipe
    response = client.post(
        f'/api/recipes/{recipe_response.get("id")}/favorite/',
        headers=headers,
    )
    recipe = response.json()
    assert response.status_code == http.HTTPStatus.CREATED
    assert "name" in recipe
    assert "image" in recipe
    assert "id" in recipe
    assert "cooking_time" in recipe


def test_add_recipe_twice(
    client,
    recipe,
):
    recipe_response, headers = recipe
    response = client.post(
        f'/api/recipes/{recipe_response.get("id")}/favorite/',
        headers=headers,
    )
    response = client.post(
        f'/api/recipes/{recipe_response.get("id")}/favorite/',
        headers=headers,
    )
    assert response.status_code == http.HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Некорректные данные.'}


def test_add_recipe_failure_credentials(
    client,
    recipe,
):
    recipe_response, headers = recipe
    response = client.post(
        f'/api/recipes/{recipe_response.get("id")}/favorite/',
        headers={"Authorization": "Token invalid_token"},
    )
    assert response.status_code == http.HTTPStatus.UNAUTHORIZED
    assert response.json() == {
        "detail": "Учетные данные не были предоставлены.",
    }


def test_delete_recipe(
    client,
    recipe,
):
    recipe_response, headers = recipe
    response = client.post(
        f'/api/recipes/{recipe_response.get("id")}/favorite/',
        headers=headers,
    )
    response = client.delete(
        f'/api/recipes/{recipe_response.get("id")}/favorite/',
        headers=headers,
    )
    assert response.status_code == http.HTTPStatus.NO_CONTENT


def test_delete_recipe_twice(
    client,
    recipe,
):
    recipe_response, headers = recipe
    response = client.post(
        f'/api/recipes/{recipe_response.get("id")}/favorite/',
        headers=headers,
    )
    response = client.delete(
        f'/api/recipes/{recipe_response.get("id")}/favorite/',
        headers=headers,
    )
    response = client.delete(
        f'/api/recipes/{recipe_response.get("id")}/favorite/',
        headers=headers,
    )
    assert response.status_code == http.HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Рецепта нет в избранном.'}


def test_delete_recipe_failure_credentials(
    client,
    recipe,
):
    recipe_response, headers = recipe
    response = client.post(
        f'/api/recipes/{recipe_response.get("id")}/favorite/',
        headers=headers,
    )
    response = client.delete(
        f'/api/recipes/{recipe_response.get("id")}/favorite/',
        headers={"Authorization": "Token invalid_token"},
    )
    assert response.status_code == http.HTTPStatus.UNAUTHORIZED
    assert response.json() == {
        "detail": "Учетные данные не были предоставлены.",
    }
