from fastapi.testclient import TestClient
from backend.main import app
from pytest import fixture


@fixture  # function? module?
def client() -> TestClient:
    return TestClient(app)
