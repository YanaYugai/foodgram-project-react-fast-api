from fastapi.testclient import TestClient
from backend.app.main import app
from pytest import fixture


@fixture
def client() -> TestClient:
    return TestClient(app)
