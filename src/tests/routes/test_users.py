from starlette.testclient import TestClient

from config import settings
from models.responses.user_info import UserInfoPrivate

def test_get_me(client: TestClient, token_headers: dict):
    response = client.get("/users/me", headers=token_headers)
    data = UserInfoPrivate.model_validate(response.json())
    assert data.username == settings.TEST_USERNAME
    assert data.email == settings.TEST_EMAIL