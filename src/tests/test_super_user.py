import os

import pytest
from httpx import AsyncClient
from models.responses.user_info import UserInfoPrivate

@pytest.mark.asyncio
async def test_super_user_exists(client: AsyncClient, super_user_token_headers: dict):
    response = await client.get("/users/me", headers=super_user_token_headers)
    data = UserInfoPrivate.model_validate(response.json())
    assert data.username == os.getenv('SUPERUSER_NAME')
    assert data.email == ''