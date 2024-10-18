from starlette.testclient import TestClient
from models.responses.message_response import MessageResponse

def test_ping(client: TestClient):
    response = client.get("/ping")
    data = MessageResponse.model_validate(response.json())
    assert data.message == "Pong!"