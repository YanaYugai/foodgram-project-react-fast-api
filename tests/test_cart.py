import http


def test_add_recipe_correct_credentials(
    client,
    recipe,
):
    recipe_response, headers = recipe
    response = client.post(
        f'/api/recipes/{recipe_response.get("id")}/shopping_cart/',
        headers=headers,
    )
    recipe = response.json()
    assert response.status_code == http.HTTPStatus.CREATED
    assert "name" in recipe
    assert "image" in recipe
    assert "id" in recipe
    assert "cooking_time" in recipe


def test_get_recipe_correct_credentials(
    client,
    cart_with_5_recipes,
):
    response = client.get(
        '/api/recipes/download_shopping_cart/',
        headers=cart_with_5_recipes,
    )
    assert response.status_code == http.HTTPStatus.OK


def test_add_recipe_twice(
    client,
    recipe,
):
    recipe_response, headers = recipe
    response = client.post(
        f'/api/recipes/{recipe_response.get("id")}/shopping_cart/',
        headers=headers,
    )
    response = client.post(
        f'/api/recipes/{recipe_response.get("id")}/shopping_cart/',
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
        f'/api/recipes/{recipe_response.get("id")}/shopping_cart/',
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
        f'/api/recipes/{recipe_response.get("id")}/shopping_cart/',
        headers=headers,
    )
    response = client.delete(
        f'/api/recipes/{recipe_response.get("id")}/shopping_cart/',
        headers=headers,
    )
    assert response.status_code == http.HTTPStatus.NO_CONTENT


def test_delete_recipe_twice(
    client,
    recipe,
):
    recipe_response, headers = recipe
    response = client.post(
        f'/api/recipes/{recipe_response.get("id")}/shopping_cart/',
        headers=headers,
    )
    response = client.delete(
        f'/api/recipes/{recipe_response.get("id")}/shopping_cart/',
        headers=headers,
    )
    response = client.delete(
        f'/api/recipes/{recipe_response.get("id")}/shopping_cart/',
        headers=headers,
    )
    assert response.status_code == http.HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Рецепта нет в корзине.'}


def test_delete_recipe_failure_credentials(
    client,
    recipe,
):
    recipe_response, headers = recipe
    response = client.post(
        f'/api/recipes/{recipe_response.get("id")}/shopping_cart/',
        headers=headers,
    )
    response = client.delete(
        f'/api/recipes/{recipe_response.get("id")}/shopping_cart/',
        headers={"Authorization": "Token invalid_token"},
    )
    assert response.status_code == http.HTTPStatus.UNAUTHORIZED
    assert response.json() == {
        "detail": "Учетные данные не были предоставлены.",
    }
