import os

import pytest
from starlette import status
from starlette.testclient import TestClient

from config import settings
from database import MongoDB
from main import app
from models.responses.token import Token

def pytest_configure() -> None:
    MongoDB().clear()

@pytest.fixture(scope="session")
def client() -> TestClient:
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="session")
def token_headers(client: TestClient) -> dict:
    register_data = {"email": settings.TEST_EMAIL, "username": settings.TEST_USERNAME, "password": settings.TEST_PASSWORD}
    register_response = client.post("/register", params=register_data)
    assert register_response.status_code == status.HTTP_200_OK

    token_data = {"username": settings.TEST_USERNAME, "password": settings.TEST_PASSWORD}
    token_response = client.post("/token", data=token_data)
    assert token_response.status_code == 200

    token = Token.model_validate(token_response.json())
    return {"Authorization": f"Bearer {token.access_token}"}

@pytest.fixture(scope="session")
def super_user_token_headers(client: TestClient):
    token_data = {"username": os.getenv('SUPERUSER_NAME'), "password": os.getenv('SUPERUSER_PASSWORD')}
    token_response = client.post("/token", data=token_data)
    assert token_response.status_code == 200

    token = Token.model_validate(token_response.json())
    return {"Authorization": f"Bearer {token.access_token}"}