import pytest
from httpx import AsyncClient

from config import settings
from models.responses.user_info import UserInfoPrivate

@pytest.mark.asyncio
async def test_get_me(client: AsyncClient, token_headers: dict):
    response = await client.get("/users/me", headers=token_headers)
    data = UserInfoPrivate.model_validate(response.json())
    assert data.username == settings.TEST_USERNAME
    assert data.email == settings.TEST_EMAIL
    assert len(data.permissions) == 0