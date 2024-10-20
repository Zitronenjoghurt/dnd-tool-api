from fastapi import APIRouter, Depends
from starlette import status

from errors.not_found_error import NotFoundError
from models.entities.user import User
from models.responses.error_responses import *
from models.responses.friend_requests_response import FriendRequestsResponse
from repositories.user_repository import UserRepository, get_user_repo
from security.authentication import get_current_user
from services.user_service import UserService, get_user_service

router = APIRouter(prefix="/friend-request", tags=["User"])

@router.get(
    "/",
    summary="Retrieve your friend requests",
    response_model=FriendRequestsResponse,
    response_description="All your open friend requests including information about the requester and the request time",
    status_code=status.HTTP_200_OK,
    responses={401: {"model": AuthenticationErrorResponse}}
)
async def post_friend_request(
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    requests = await user_service.get_friend_requests(current_user)
    return FriendRequestsResponse(requests=requests)

@router.post(
    "/",
    summary="Send a friend request",
    response_description="An empty response",
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": FriendRequestErrorResponse},
        401: {"model": AuthenticationErrorResponse},
        404: {"model": UserNotFoundErrorResponse}
    }
)
async def post_friend_request(
    username: str,
    source_user: User = Depends(get_current_user),
    user_repository: UserRepository = Depends(get_user_repo),
    user_service: UserService = Depends(get_user_service)
):
    target_user = await user_repository.find_by_username(username)
    if not isinstance(target_user, User):
        raise NotFoundError(ErrorCode.USER_NOT_FOUND)
    await user_service.send_friend_request(source_user, target_user)