import asyncio
from typing import List, Optional

from fastapi.params import Depends

from constants.error_codes import ErrorCode
from errors.bad_request_error import BadRequestError
from models.entities.friendship import Friendship, FriendRequest
from models.entities.user import User
from models.responses.friend_request_response import FriendRequestResponse
from repositories.friendship_repository import FriendshipRepository, get_friendship_repo
from repositories.user_repository import UserRepository, get_user_repo
from services.base_service import BaseService


class UserService(BaseService[User]):
    def __init__(self, user_repository: UserRepository, friendship_repository: FriendshipRepository):
        if not hasattr(self, 'initialized'):
            self.user_repository = user_repository
            self.friendship_repository = friendship_repository
        super().__init__(User)

    # The source user sends a friend request to the target user
    async def send_friend_request(self, source: User, target: User):
        if not target.accepts_friend_requests or source.id == target.id or target.has_blocked(source):
            raise BadRequestError(ErrorCode.UNABLE_TO_BEFRIEND)

        friendship = await self.friendship_repository.find_by_including_user_ids([source.id, target.id])
        if isinstance(friendship, Friendship):
            raise BadRequestError(ErrorCode.ALREADY_FRIENDS)
        if target.has_friend_request_from(source):
            raise BadRequestError(ErrorCode.ALREADY_SENT_REQUEST)

        friend_request = FriendRequest(user_id=source.id)
        target.friend_requests.append(friend_request)
        await self.user_repository.save(target)

    async def get_friend_request_response(self, request: FriendRequest) -> Optional[FriendRequestResponse]:
        user = await self.user_repository.find_one_by_id(str(request.user_id))
        if not isinstance(user, User):
            return None
        return FriendRequestResponse(
            user_info=user.get_public_info(),
            created_at=request.created_at
        )

    async def get_friend_requests(self, user: User) -> List[FriendRequestResponse]:
        request_tasks = [self.get_friend_request_response(request) for request in user.friend_requests]
        requests = await asyncio.gather(*request_tasks)
        return [request for request in requests if isinstance(request, FriendRequestResponse)]

    # The source user accepts a friend request from the target user
    async def accept_friend_request(self, source: User, target: User):
        if not source.has_friend_request_from(target):
            raise BadRequestError(ErrorCode.NO_FRIEND_REQUEST_FROM_USER)

        source.delete_friend_request_from(target)
        await self.user_repository.save(source)

        friendship = await self.friendship_repository.find_by_including_user_ids([source.id, target.id])
        if isinstance(friendship, Friendship):
            raise BadRequestError(ErrorCode.ALREADY_FRIENDS)
        if target.has_blocked(source) or source.has_blocked(target) or source.id == target.id:
            raise BadRequestError(ErrorCode.UNABLE_TO_BEFRIEND)

        new_friendship = Friendship(user_ids=[source.id, target.id])
        await self.friendship_repository.save(new_friendship)

async def get_user_service(
    friendship_repository: FriendshipRepository = Depends(get_friendship_repo),
    user_repository: UserRepository = Depends(get_user_repo)
):
    return UserService(user_repository, friendship_repository)