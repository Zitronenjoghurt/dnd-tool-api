from fastapi import APIRouter
from starlette import status

from models.responses.message_response import MessageResponse

router = APIRouter(prefix="/ping", tags=["Miscellaneous"])

@router.get(
    "",
    summary="A simple ping endpoint for testing connection",
    response_description="A response saying 'Pong!'",
    status_code=status.HTTP_200_OK
)
async def ping() -> MessageResponse:
    return MessageResponse.create("Pong!")