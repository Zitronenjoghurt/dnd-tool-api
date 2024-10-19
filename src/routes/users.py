from fastapi import APIRouter, Depends
from starlette import status

from models.entities.user import User
from models.responses.error_response import AuthenticationErrorResponse
from models.responses.user_info import UserInfoPrivate
from security.authentication import get_current_user

router = APIRouter(prefix="/users", tags=["User"])

@router.get("/me",
            summary="Get your own private user information",
            response_model=UserInfoPrivate,
            response_description="Your private user information",
            status_code=status.HTTP_200_OK,
            responses={401: {"model": AuthenticationErrorResponse}}
)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user.get_private_info()