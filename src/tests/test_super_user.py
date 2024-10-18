import os

from starlette.testclient import TestClient
from models.responses.user_info import UserInfoPrivate

def test_super_user_exists(client: TestClient, super_user_token_headers: dict):
    response = client.get("/users/me", headers=super_user_token_headers)
    data = UserInfoPrivate.model_validate(response.json())
    assert data.username == os.getenv('SUPERUSER_NAME')
    assert data.email == ''