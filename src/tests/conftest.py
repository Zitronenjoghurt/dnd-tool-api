import asyncio
import os
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status
from config import settings
from database import MongoDB
from main import app, lifespan
from models.responses.generated_registration_codes_response import GeneratedRegistrationCodesResponse
from models.responses.token import Token

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture
async def test_app() -> AsyncGenerator[FastAPI, None]:
    MongoDB().clear()
    async with lifespan(app):
        yield app
        MongoDB().clear()

@pytest_asyncio.fixture
async def client(test_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        yield client

@pytest_asyncio.fixture
async def super_user_token_headers(client: AsyncClient):
    token_data = {"username": os.getenv('SUPERUSER_NAME'), "password": os.getenv('SUPERUSER_PASSWORD')}
    token_response = await client.post("/token", data=token_data)
    assert token_response.status_code == 200

    token = Token.model_validate(token_response.json())
    return {"Authorization": f"Bearer {token.access_token}"}

@pytest_asyncio.fixture
async def token_headers(client: AsyncClient, super_user_token_headers: dict) -> dict:
    registration_code_response = await client.post("registration-code", params={"count": 1}, headers=super_user_token_headers)
    registration_codes = GeneratedRegistrationCodesResponse.model_validate(registration_code_response.json())
    assert len(registration_codes.codes) == 1
    code = registration_codes.codes[0]
    assert isinstance(code, str)

    register_data = {
        "email": settings.TEST_EMAIL,
        "username": settings.TEST_USERNAME,
        "password": settings.TEST_PASSWORD,
        "registration_code": code,
    }
    register_response = await client.post("/register", params=register_data)
    assert register_response.status_code == status.HTTP_200_OK

    token_data = {"username": settings.TEST_USERNAME, "password": settings.TEST_PASSWORD}
    token_response = await client.post("/token", data=token_data)
    assert token_response.status_code == 200

    token = Token.model_validate(token_response.json())
    return {"Authorization": f"Bearer {token.access_token}"}