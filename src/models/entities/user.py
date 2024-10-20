from typing import List

from bson import ObjectId

from constants.permissions import GlobalPermission
from errors.global_permission_error import GlobalPermissionError
from models.entities.friendship import FriendRequest
from models.entities.mongo_base_entity import MongoBaseEntity
from models.responses.user_info import UserInfoPublic, UserInfoPrivate


class User(MongoBaseEntity):
    username: str
    email: str
    password_hash: str
    # The registration code that was used to create this user
    # Will be a unique key to ensure one registration key can't create 2 users
    registration_code: str
    global_permissions: List[GlobalPermission] = []
    accepts_friend_requests: bool = True
    friend_requests: List[FriendRequest] = []
    blocked_users: List[ObjectId] = []

    def get_public_info(self) -> UserInfoPublic:
        return UserInfoPublic(username=self.username)

    def get_private_info(self) -> UserInfoPrivate:
        return UserInfoPrivate(
            username=self.username,
            email=self.email,
            permissions=self.global_permissions
        )

    def add_global_permission(self, permission: GlobalPermission):
        if permission not in self.global_permissions:
            self.global_permissions.append(permission)

    def has_global_permissions(self, permissions: List[GlobalPermission]) -> bool:
        if GlobalPermission.SUPER_USER in self.global_permissions:
            return True
        for permission in permissions:
            if not permission in self.global_permissions:
                return False
        return True

    def check_global_permissions(self, permissions: List[GlobalPermission]):
        if GlobalPermission.SUPER_USER in self.global_permissions:
            return
        missing_permissions = []
        for permission in permissions:
            if permission not in self.global_permissions:
                missing_permissions.append(permission)
        if missing_permissions:
            raise GlobalPermissionError(permissions=missing_permissions)

    def has_blocked(self, user: 'User') -> bool:
        if user.id in self.blocked_users:
            return True
        return False

    def has_friend_request_from(self, user: 'User') -> bool:
        return any(request.user_id == user.id for request in self.friend_requests)

    def delete_friend_request_from(self, user: 'User'):
        self.friend_requests = [request for request in self.friend_requests if request.user_id != user.id]