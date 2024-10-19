import pytest
from httpx import AsyncClient
from models.responses.message_response import MessageResponse

@pytest.mark.asyncio
async def test_ping(client: AsyncClient):
    response = await client.get("/ping")
    data = MessageResponse.model_validate(response.json())
    assert data.message == "Pong!"