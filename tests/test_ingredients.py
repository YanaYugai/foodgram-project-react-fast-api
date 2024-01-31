from tests.test_recipes import client
from tests.utils import test_nonexistent_objects
from tests.example_responses import ingredients


test_nonexistent_objects('/api/ingredients/2000/', client)


def test_get_ingredients():
    response = client.get('/api/ingredients/')
    assert response.status_code == 200
    assert response.json == list(ingredients.values())


def test_get_tag():
    response = client.get('/api/ingredients/1/')
    assert response.status_code == 200
    assert response.json == ingredients[1]
