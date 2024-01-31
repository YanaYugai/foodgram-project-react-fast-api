from tests.test_recipes import client
from tests.utils import test_nonexistent_objects
from tests.example_responses import tags


test_nonexistent_objects('/api/tags/7', client)


def test_get_tags():
    response = client.get('/api/tags/')
    assert response.status_code == 200
    assert response.json == list(tags.values())


def test_get_tag():
    response = client.get('/api/tags/1/')
    assert response.status_code == 200
    assert response.json == tags[1]
